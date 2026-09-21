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


# European qualification registry by PL season (football-data season labels).
# Teams that played UCL/UEL/UECL that season, in football-data naming.
EUROPEAN_TEAMS = {
    "2019/20": ["Liverpool", "Man City", "Chelsea", "Tottenham", "Arsenal", "Man United", "Wolves"],
    "2020/21": ["Liverpool", "Man City", "Man United", "Chelsea", "Leicester", "Tottenham", "Arsenal", "Wolves"],
    "2021/22": ["Man City", "Man United", "Liverpool", "Chelsea", "Leicester", "West Ham", "Tottenham"],
    "2022/23": ["Man City", "Liverpool", "Chelsea", "Tottenham", "Arsenal", "Man United", "West Ham"],
    "2023/24": ["Man City", "Arsenal", "Man United", "Newcastle", "Liverpool", "Brighton", "Aston Villa"],
    "2024/25": ["Man City", "Arsenal", "Liverpool", "Aston Villa", "Tottenham", "Chelsea", "Newcastle", "Man United"],
    "2025/26": ["Liverpool", "Arsenal", "Man City", "Chelsea", "Newcastle", "Aston Villa", "Tottenham",
                "Crystal Palace", "Man United", "Brighton", "Nott'm Forest"],
}

# Windows when European competition is active (group/league phase + knockouts).
# Between these: Aug/early-Sep and mid-Dec/mid-Feb = no European midweek football.
def _in_european_window(day_of_year: int) -> bool:
    # ~Sep 15 (258) to ~Dec 15 (349), and ~Feb 15 (46) to ~May 31 (151)
    return 258 <= day_of_year <= 349 or 46 <= day_of_year <= 151


def _parse_fd_date(s):
    """Parse football-data dates: dd/mm/yyyy or dd/mm/yy."""
    import pandas as pd
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return pd.to_datetime(s, format=fmt)
        except Exception:
            continue
    try:
        return pd.to_datetime(s, dayfirst=True, errors="raise")
    except Exception:
        return None


def _team_points(home: bool, result) -> float:
    if result == "D":
        return 1.0
    if (result == "H") == home:
        return 3.0
    return 0.0


def test_hypothesis(hypothesis) -> dict:
    """Test a hypothesis and return results dict.

    Dispatches to id-specific tests. Falls back to a generic home-vs-away
    goals contrast when no specific test exists, and clearly labels the
    report as such.
    """
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
        "data_source": "football-data.co.uk (football_data table)",
        "sample_desc": "",
        "features": ", ".join(hypothesis.variables_tested),
    }

    try:
        if hypothesis.id == "post-european-fatigue":
            # Team-match panel: one row per team per match, PL seasons with kickoff data
            df = storage.fetch_df(
                "SELECT season, match_date, home_team, away_team, home_goals, away_goals, result "
                "FROM football_data "
                "WHERE competition = 'Premier League' "
                "AND home_goals IS NOT NULL AND away_goals IS NOT NULL "
                "AND season IN ('2019/20','2020/21','2021/22','2022/23','2023/24','2024/25','2025/26')"
            )
            rows = []
            for _, r in df.iterrows():
                dt = _parse_fd_date(r["match_date"])
                if dt is None:
                    continue
                euro_window = _in_european_window(dt.dayofyear)
                season_euro = EUROPEAN_TEAMS.get(r["season"], [])
                for team, is_home in ((r["home_team"], True), (r["away_team"], False)):
                    gf = r["home_goals"] if is_home else r["away_goals"]
                    ga = r["away_goals"] if is_home else r["home_goals"]
                    rows.append({
                        "season": r["season"],
                        "team": team,
                        "is_home": is_home,
                        "euro_team": team in season_euro,
                        "in_window": euro_window,
                        "points": _team_points(is_home, r["result"]),
                        "gd": int(gf) - int(ga),
                        "goals_for": int(gf),
                    })
            panel = pd.DataFrame(rows)
            n_matches = len(df)
            results["sample_desc"] = (
                f"{n_matches} PL matches 2019/20–2025/26 ({len(panel)} team-match rows); "
                "European participants identified per season"
            )
            results["sample_size"] = n_matches

            euro = panel[panel["euro_team"]]
            non_euro = panel[~panel["euro_team"]]

            def welch(name, a, b):
                if len(a) < 30 or len(b) < 30:
                    return None
                t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)
                pooled_sd = np.sqrt((a.std() ** 2 + b.std() ** 2) / 2)
                d = (a.mean() - b.mean()) / pooled_sd if pooled_sd > 0 else 0.0
                shift = ((a.mean() - b.mean()) / b.mean() * 100) if b.mean() != 0 else 0.0
                se = np.sqrt(a.var() / len(a) + b.var() / len(b))
                return {
                    "name": name,
                    "n_treatment": int(len(a)),
                    "n_control": int(len(b)),
                    "mean_treatment": round(float(a.mean()), 3),
                    "mean_control": round(float(b.mean()), 3),
                    "mean_shift_pct": round(float(shift), 1),
                    "cohens_d": round(float(d), 3),
                    "p_value": round(float(p_val), 4),
                    "ci_95_low": round(float(a.mean() - b.mean() - 1.96 * se), 3),
                    "ci_95_high": round(float(a.mean() - b.mean() + 1.96 * se), 3),
                    "significant": "True" if p_val < 0.0125 else "False",  # Bonferroni 4 contrasts
                }

            contrasts = [
                # C1: European teams' points during European windows vs outside them
                welch("C1_euro_teams_in_vs_out_of_window_points",
                      euro[euro["in_window"]]["points"], euro[~euro["in_window"]]["points"]),
                # C2: European teams' goal difference in vs out of window
                welch("C2_euro_teams_in_vs_out_of_window_gd",
                      euro[euro["in_window"]]["gd"], euro[~euro["in_window"]]["gd"]),
                # C3 (placebo): non-European teams in vs out of window — should be null
                welch("C3_placebo_non_euro_in_vs_out_of_window_points",
                      non_euro[non_euro["in_window"]]["points"], non_euro[~non_euro["in_window"]]["points"]),
                # C4: European vs non-European teams during windows (raw gap, context)
                welch("C4_euro_vs_non_euro_in_window_points",
                      euro[euro["in_window"]]["points"], non_euro[non_euro["in_window"]]["points"]),
            ]
            contrasts = [c for c in contrasts if c is not None]
            results["results_table"] = contrasts

            c1 = next((c for c in contrasts if c["name"].startswith("C1_")), None)
            c3 = next((c for c in contrasts if c["name"].startswith("C3_")), None)
            c1_sig = c1 is not None and c1["significant"] == "True"
            placebo_clean = c3 is None or c3["significant"] == "False"

            if c1_sig and placebo_clean:
                results["status"] = "Supported"
                results["effect_size"] = c1["cohens_d"]
                results["p_value"] = c1["p_value"]
                results["interpretation"] = (
                    f"European participants' league points drop from {c1['mean_control']} outside European "
                    f"windows to {c1['mean_treatment']} during them ({c1['mean_shift_pct']}%, d={c1['cohens_d']}, "
                    f"p={c1['p_value']}), while the non-European placebo shows no such dip. The fatigue effect "
                    f"is specific to teams carrying midweek European fixtures."
                )
                results["conclusion"] = (
                    "Post-European weekend fatigue is supported: European teams lose measurable league points "
                    "during European windows, and the placebo control rules out a generic calendar effect. "
                    "Fade European sides' league handicaps during congested European months."
                )
            elif c1_sig and not placebo_clean:
                results["status"] = "Rejected"
                results["effect_size"] = c1["cohens_d"]
                results["p_value"] = c1["p_value"]
                results["interpretation"] = (
                    f"European teams' points dip during European windows ({c1['mean_shift_pct']}%, "
                    f"p={c1['p_value']}), BUT the non-European placebo dips too. The effect appears to be "
                    f"a general within-season pattern (e.g. winter form), not European fatigue specifically."
                )
                results["conclusion"] = (
                    "Rejected: the points dip during European windows is not specific to European teams — "
                    "the placebo control fails, so this cannot be traded as a European-fatigue edge."
                )
            else:
                results["status"] = "Rejected"
                results["interpretation"] = (
                    f"Across {n_matches} PL matches, European teams' points during European windows do not "
                    f"differ significantly from outside them after correction. Midweek European football "
                    f"alone does not measurably dent league performance in this sample."
                )
                results["conclusion"] = (
                    "The post-European fatigue hypothesis is rejected for this dataset — squad rotation "
                    "appears to absorb the congestion at this level."
                )
            results["lessons"] = [
                "European qualification is proxied by a per-season registry, not fixture lists; deep UCL/UEL runs are not distinguished from early exits.",
                "The placebo contrast (non-European teams, same windows) is the key falsification device — without it, seasonal form drift masquerades as fatigue.",
                "Window boundaries (Sep 15 / Dec 15 / Feb 15) approximate the European calendar; a fixture-level join would sharpen the treatment definition.",
            ]
        elif hypothesis.id == "early-kickoff-disadvantage":
            df = storage.fetch_df(
                "SELECT kickoff_time, home_goals, away_goals, result "
                "FROM football_data "
                "WHERE kickoff_time IS NOT NULL AND kickoff_time != '' "
                "AND home_goals IS NOT NULL AND away_goals IS NOT NULL"
            )
            results["sample_desc"] = f"{len(df)} matches with kickoff time recorded"
            results["sample_size"] = len(df)

            def to_minutes(t):
                try:
                    h, m = str(t).split(":")
                    return int(h) * 60 + int(m)
                except Exception:
                    return None

            df["ko_min"] = df["kickoff_time"].map(to_minutes)
            df = df.dropna(subset=["ko_min"])
            df["total_goals"] = df["home_goals"].astype(float) + df["away_goals"].astype(float)
            df["home_win"] = (df["result"] == "H").astype(float)

            early = df[df["ko_min"] < 750]   # before 12:30
            late = df[df["ko_min"] >= 750]   # 12:30 and after

            contrasts = []
            for name, t_vals, c_vals in [
                ("C1_early_vs_late_total_goals", early["total_goals"], late["total_goals"]),
                ("C2_early_vs_late_home_win_rate", early["home_win"], late["home_win"]),
            ]:
                if len(t_vals) > 30 and len(c_vals) > 30:
                    t_stat, p_val = stats.ttest_ind(t_vals, c_vals, equal_var=False)
                    pooled_sd = np.sqrt((t_vals.std() ** 2 + c_vals.std() ** 2) / 2)
                    d = (t_vals.mean() - c_vals.mean()) / pooled_sd if pooled_sd > 0 else 0.0
                    shift = ((t_vals.mean() - c_vals.mean()) / c_vals.mean() * 100) if c_vals.mean() != 0 else 0.0
                    se = np.sqrt(t_vals.var() / len(t_vals) + c_vals.var() / len(c_vals))
                    contrasts.append({
                        "name": name,
                        "n_treatment": int(len(t_vals)),
                        "n_control": int(len(c_vals)),
                        "mean_treatment": round(float(t_vals.mean()), 3),
                        "mean_control": round(float(c_vals.mean()), 3),
                        "mean_shift_pct": round(float(shift), 1),
                        "cohens_d": round(float(d), 3),
                        "p_value": round(float(p_val), 4),
                        "ci_95_low": round(float(t_vals.mean() - c_vals.mean() - 1.96 * se), 3),
                        "ci_95_high": round(float(t_vals.mean() - c_vals.mean() + 1.96 * se), 3),
                        "significant": "True" if p_val < 0.025 else "False",
                    })

            results["results_table"] = contrasts
            sig = [c for c in contrasts if c["significant"] == "True"]
            if sig:
                results["status"] = "Supported"
                best = max(sig, key=lambda c: abs(c["cohens_d"]))
                results["effect_size"] = best["cohens_d"]
                results["p_value"] = best["p_value"]
                results["interpretation"] = (
                    f"Across {len(df)} matches with kickoff times, early kickoffs (before 12:30) show "
                    f"measurable differences from later kickoffs. Significant contrast: {best['name']} "
                    f"({best['mean_shift_pct']}% shift, d={best['cohens_d']}, p={best['p_value']})."
                )
                results["conclusion"] = "The early-kickoff effect is supported in this sample; effect sizes should guide stake sizing."
            else:
                results["status"] = "Rejected"
                results["interpretation"] = (
                    f"Across {len(df)} matches, no contrast between early (<12:30) and late kickoffs "
                    f"reached significance after correction. Any early-kickoff effect is too small to trade on its own."
                )
                results["conclusion"] = "The early-kickoff disadvantage hypothesis is rejected for this dataset."
            results["lessons"] = [
                "Kickoff time is only recorded in recent football-data seasons; older seasons lack Time columns.",
                "Early kickoffs are disproportionately televised matches involving big clubs — selection bias is a real confound.",
            ]
        else:
            # Generic fallback — clearly labelled as a baseline contrast, NOT the named hypothesis
            df = storage.fetch_df(
                "SELECT home_goals, away_goals FROM football_data "
                "WHERE home_goals IS NOT NULL AND away_goals IS NOT NULL LIMIT 5000"
            )
            results["sample_desc"] = (
                f"{len(df)} matches (generic home-vs-away baseline; "
                "hypothesis-specific test not yet implemented)"
            )
            results["sample_size"] = len(df)
            home_goals = df["home_goals"].dropna().astype(float)
            away_goals = df["away_goals"].dropna().astype(float)
            if len(home_goals) > 30 and len(away_goals) > 30:
                t_stat, p_val = stats.ttest_ind(home_goals, away_goals, equal_var=False)
                pooled_sd = np.sqrt((home_goals.std() ** 2 + away_goals.std() ** 2) / 2)
                cohens_d = (home_goals.mean() - away_goals.mean()) / pooled_sd if pooled_sd > 0 else 0.0
                results["effect_size"] = round(float(cohens_d), 3)
                results["p_value"] = round(float(p_val), 4)
                results["sample_size"] = int(len(home_goals) + len(away_goals))
                results["results_table"] = [{
                    "name": "home_vs_away_goals_baseline",
                    "n_treatment": int(len(home_goals)),
                    "n_control": int(len(away_goals)),
                    "mean_treatment": round(float(home_goals.mean()), 2),
                    "mean_control": round(float(away_goals.mean()), 2),
                    "mean_shift_pct": round(float((home_goals.mean() - away_goals.mean()) / away_goals.mean() * 100), 1),
                    "cohens_d": round(float(cohens_d), 3),
                    "p_value": round(float(p_val), 4),
                    "ci_95_low": round(float(cohens_d - 1.96 * np.sqrt(1 / len(home_goals) + 1 / len(away_goals))), 3),
                    "ci_95_high": round(float(cohens_d + 1.96 * np.sqrt(1 / len(home_goals) + 1 / len(away_goals))), 3),
                    "significant": "True" if p_val < 0.05 else "False",
                }]
                results["status"] = "Supported" if p_val < 0.05 else "Rejected"
                results["interpretation"] = (
                    f"NOTE: this is a generic home-vs-away goals baseline, not a test of '{hypothesis.title}'. "
                    f"A hypothesis-specific test module is required before this result is meaningful. "
                    f"Baseline: home teams average {home_goals.mean():.2f} goals vs {away_goals.mean():.2f} away."
                )
                results["conclusion"] = (
                    "Baseline contrast only — hypothesis-specific test not yet implemented. "
                    "Treat this entry as a pipeline smoke-test, not research evidence."
                )
                results["lessons"] = [
                    f"Implement a dedicated test module for hypothesis '{hypothesis.id}' before publishing.",
                    "The generic baseline exists only to keep the pipeline exercised.",
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
    
    # Stage research, docs, AND the hypothesis queue state so progress persists
    run_command(["git", "add", "research/", "docs/", "scripts/hypothesis_queue.py"], "git add")
    
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
        ["git", "push", "origin", "HEAD:main"],
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
    today = date.today().isoformat()
    
    technical_md = generate_technical_report(
        hypothesis_id=hypothesis.id,
        title=hypothesis.title,
        hypothesis=hypothesis.hypothesis,
        negative=hypothesis.negative,
        direction=hypothesis.direction,
        data_source=results.get("data_source", "football-data.co.uk"),
        sample=results.get("sample_desc") or f"{results['sample_size']} matches",
        features=results.get("features", ", ".join(hypothesis.variables_tested)),
        method=hypothesis.method,
        results=results["results_table"],
        interpretation=results["interpretation"],
        conclusion=results["conclusion"],
        lessons=results["lessons"],
        status=results["status"],
        effect_size=results["effect_size"],
        p_value=results["p_value"],
        sample_size=results["sample_size"],
        published=today,
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
        published=today,
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
