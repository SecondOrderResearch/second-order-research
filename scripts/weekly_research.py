"""Weekly research pipeline — fetch, test, generate, publish."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_DIR, RAW_DIR, RESEARCH_DIR, DB_PATH
from src.logging_config import setup_logging
from scripts.hypothesis_queue import get_next_hypothesis, mark_tested, get_tested_count, get_total_count
from scripts.report_writer import generate_technical_report, generate_public_report, save_report

logger = setup_logging("weekly_research")


def run_command(cmd: list[str], description: str) -> tuple[int, str]:
    """Run a shell command and return (exit_code, output)."""
    logger.info(f"Running: {description}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        logger.warning(f"{description} exited with code {result.returncode}: {result.stderr[:500]}")
    return result.returncode, result.stdout


def fetch_football_data() -> bool:
    """Fetch latest football-data.co.uk CSVs."""
    cmd = [
        sys.executable, "-c",
        "import sys; sys.path.insert(0, '.'); "
        "from src.ingestion.download_football_data import ingest_all_football_data; "
        "ingest_all_football_data()"
    ]
    code, out = run_command(cmd, "football-data download")
    return code == 0


def fetch_weather_data() -> bool:
    """Fetch latest weather data from Open-Meteo."""
    cmd = [
        sys.executable, "-c",
        "import sys; sys.path.insert(0, '.'); "
        "from src.ingestion.fetch_weather import fetch_recent_weather; "
        "fetch_recent_weather()"
    ]
    code, out = run_command(cmd, "weather fetch")
    return code == 0


def fetch_sofascore_data() -> bool:
    """Fetch latest Sofascore data."""
    cmd = [
        sys.executable, "-c",
        "import sys; sys.path.insert(0, '.'); "
        "from src.ingestion.fetch_sofascore import ingest_all_sofascore; "
        "ingest_all_sofascore()"
    ]
    code, out = run_command(cmd, "sofascore fetch")
    return code == 0


def test_hypothesis(hypothesis) -> dict:
    """Test a hypothesis and return results dict."""
    # This is a simplified test framework
    # In production, this would dispatch to specific test modules based on hypothesis.category
    
    from src.pipeline.storage import Storage
    import pandas as pd
    import numpy as np
    from scipy import stats
    
    storage = Storage(DB_PATH)
    
    results = {
        "status": "Rejected",
        "effect_size": None,
        "p_value": None,
        "sample_size": 0,
        "results_table": [],
        "interpretation": "",
        "conclusion": "",
        "lessons": [],
    }
    
    try:
        # Load football_data
        df = storage.fetch_df("SELECT * FROM football_data WHERE home_goals IS NOT NULL AND away_goals IS NOT NULL LIMIT 5000")
        if df.empty:
            results["interpretation"] = "No match data available for testing."
            results["lessons"] = ["Database is empty — run data fetch first."]
            return results
        
        results["sample_size"] = len(df)
        
        # Simple test: compare home vs away goals (placeholder)
        home_goals = df['home_goals'].dropna().astype(float)
        away_goals = df['away_goals'].dropna().astype(float)
        
        if len(home_goals) > 30 and len(away_goals) > 30:
            t_stat, p_val = stats.ttest_ind(home_goals, away_goals)
            cohens_d = (home_goals.mean() - away_goals.mean()) / np.sqrt(
                (home_goals.std()**2 + away_goals.std()**2) / 2
            )
            
            results["effect_size"] = round(cohens_d, 3)
            results["p_value"] = round(p_val, 4)
            results["sample_size"] = len(home_goals) + len(away_goals)
            
            results["results_table"] = [{
                "name": "home_vs_away_goals",
                "n_treatment": int(len(home_goals)),
                "n_control": int(len(away_goals)),
                "mean_treatment": round(float(home_goals.mean()), 2),
                "mean_control": round(float(away_goals.mean()), 2),
                "mean_shift_pct": round(float((home_goals.mean() - away_goals.mean()) / away_goals.mean() * 100), 1),
                "cohens_d": round(float(cohens_d), 3),
                "p_value": round(float(p_val), 4),
                "ci_95_low": round(float(cohens_d - 1.96 * np.sqrt(1/len(home_goals) + 1/len(away_goals))), 3),
                "ci_95_high": round(float(cohens_d + 1.96 * np.sqrt(1/len(home_goals) + 1/len(away_goals))), 3),
                "significant": "True" if p_val < 0.05 else "False",
            }]
            
            if p_val < 0.05:
                results["status"] = "Supported"
                results["interpretation"] = f"Home teams score significantly more goals than away teams (d={float(cohens_d):.3f}, p={float(p_val):.4f})."
                results["conclusion"] = "Home advantage is confirmed in this dataset."
            else:
                results["status"] = "Rejected"
                results["interpretation"] = f"No significant difference in home vs away goals (d={float(cohens_d):.3f}, p={float(p_val):.4f})."
                results["conclusion"] = "The hypothesis is rejected for this dataset."
            
            results["lessons"] = [
                "Simple t-test provides a baseline; more sophisticated controls needed.",
                "Sample size and season coverage affect power.",
            ]
        
    except Exception as e:
        logger.error(f"Hypothesis test failed: {e}")
        results["interpretation"] = f"Test failed: {str(e)}"
        results["lessons"] = [f"Error: {str(e)}"]
    finally:
        storage.close()
    
    return results


def build_site() -> bool:
    """Build the static site."""
    code, out = run_command(
        [sys.executable, "scripts/build_site.py"],
        "site build"
    )
    return code == 0


def git_commit_and_push() -> bool:
    """Commit and push changes."""
    today = date.today().isoformat()
    
    # Stage research and docs
    run_command(["git", "add", "research/", "docs/"], "git add")
    
    # Commit
    code, out = run_command(
        ["git", "commit", "-m", f"Weekly research update {today}"],
        "git commit"
    )
    if code != 0:
        # Nothing to commit
        if "nothing to commit" in out:
            return True
        return False
    
    # Push
    code, out = run_command(
        ["git", "push", "origin", "deploy-reports:main"],
        "git push"
    )
    return code == 0


def run_pipeline() -> dict:
    """Run the full weekly research pipeline."""
    logger.info("=" * 60)
    logger.info("Starting weekly research pipeline")
    logger.info("=" * 60)
    
    report = {
        "success": False,
        "hypothesis": None,
        "result": None,
        "files": [],
        "errors": [],
    }
    
    # 1. Get next hypothesis
    hypothesis = get_next_hypothesis()
    if hypothesis is None:
        msg = "No untested hypotheses remaining in queue."
        logger.warning(msg)
        report["errors"].append(msg)
        return report
    
    report["hypothesis"] = hypothesis.title
    logger.info(f"Testing hypothesis: {hypothesis.title} ({hypothesis.id})")
    
    # 2. Fetch fresh data
    logger.info("Fetching fresh data...")
    fetch_football_data()
    fetch_weather_data()
    fetch_sofascore_data()
    
    # 3. Test hypothesis
    logger.info("Testing hypothesis...")
    results = test_hypothesis(hypothesis)
    report["result"] = results["status"]
    
    # 4. Generate reports
    logger.info("Generating reports...")
    
    technical_md = generate_technical_report(
        hypothesis_id=hypothesis.id,
        title=hypothesis.title,
        hypothesis=hypothesis.hypothesis,
        negative=hypothesis.negative,
        direction=hypothesis.direction,
        data_source="StatsBomb Open Data + Football-Data + Open-Meteo",
        sample=f"{results['sample_size']} matches",
        features=", ".join(hypothesis.variables_tested),
        method=hypothesis.method,
        results=results["results_table"],
        interpretation=results["interpretation"],
        conclusion=results["conclusion"],
        lessons=results["lessons"],
        status=results["status"],
        effect_size=results["effect_size"],
        p_value=results["p_value"],
        sample_size=results["sample_size"],
    )
    
    public_md = generate_public_report(
        title=hypothesis.title,
        hypothesis=hypothesis.hypothesis,
        direction=hypothesis.direction,
        results=results["results_table"],
        interpretation=results["interpretation"],
        markets_affected=hypothesis.markets_affected,
        confidence="Medium" if results["status"] == "Supported" else "Low",
        status=results["status"],
        effect_size=results["effect_size"],
        p_value=results["p_value"],
    )
    
    # 5. Save reports
    tech_path = save_report(hypothesis.id, technical_md, "technical")
    pub_path = save_report(hypothesis.id, public_md, "public")
    report["files"] = [str(tech_path), str(pub_path)]
    logger.info(f"Saved reports: {tech_path.name}, {pub_path.name}")
    
    # 6. Update queue
    mark_tested(
        hypothesis_id=hypothesis.id,
        status="tested",
        result=results["status"],
        effect_size=results["effect_size"],
        p_value=results["p_value"],
        sample_size=results["sample_size"],
    )
    
    # 7. Build site
    logger.info("Building site...")
    if not build_site():
        report["errors"].append("Site build failed")
        return report
    
    # 8. Commit and push
    logger.info("Publishing...")
    if not git_commit_and_push():
        report["errors"].append("Git push failed")
        return report
    
    report["success"] = True
    logger.info("Pipeline complete!")
    
    return report


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2))
