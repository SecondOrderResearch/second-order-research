"""Ingest Sofascore JSON stats into the warehouse."""

from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from src.config import RAW_DIR, DB_PATH
from src.pipeline.storage import Storage
from src.logging_config import setup_logging

logger = setup_logging("ingestion_sofascore")

SOFARECORE_DIR = RAW_DIR / "sofascore"


def ingest_sofascore_json(filepath: Path) -> int:
    """Ingest a single Sofascore JSON stats file."""
    storage = Storage(DB_PATH)
    
    try:
        data = json.loads(filepath.read_text(encoding='utf-8'))
        logger.info(f"Read {len(data)} records from {filepath.name}")
        
        # Extract season from filename (e.g., EPL_2425_stats.json -> 2024/25)
        parts = filepath.stem.split('_')
        season = "Unknown"
        if len(parts) >= 2:
            season_code = parts[1]
            if len(season_code) == 4:
                season = f"20{season_code[:2]}/{season_code[2:]}"
        
        records = []
        for match in data:
            record = {
                "match_id": match.get("id", f"{season}_{filepath.stem}_{len(records)}"),
                "season": season,
                "home_team": match.get("homeTeam", {}).get("name", ""),
                "away_team": match.get("awayTeam", {}).get("name", ""),
                "home_goals": match.get("homeScore", {}).get("current", None),
                "away_goals": match.get("awayScore", {}).get("current", None),
                "home_xg": None,
                "away_xg": None,
                "home_shots": None,
                "away_shots": None,
                "home_corners": None,
                "away_corners": None,
                "home_possession": None,
                "away_possession": None,
                "source_file": filepath.name,
            }
            
            # Extract statistics if available
            stats = match.get("statistics", [])
            for stat_group in stats:
                if stat_group.get("period") == "ALL":
                    for stat in stat_group.get("groups", []):
                        for item in stat.get("statisticsItems", []):
                            name = item.get("name", "")
                            home_val = item.get("home", "0")
                            away_val = item.get("away", "0")
                            
                            if name == "Expected goals":
                                record["home_xg"] = float(home_val) if home_val else None
                                record["away_xg"] = float(away_val) if away_val else None
                            elif name == "Total shots":
                                record["home_shots"] = int(home_val) if home_val else None
                                record["away_shots"] = int(away_val) if away_val else None
                            elif name == "Corner kicks":
                                record["home_corners"] = int(home_val) if home_val else None
                                record["away_corners"] = int(away_val) if away_val else None
                            elif name == "Ball possession":
                                record["home_possession"] = float(home_val.replace('%', '')) if home_val else None
                                record["away_possession"] = float(away_val.replace('%', '')) if away_val else None
            
            records.append(record)
        
        if records:
            records_df = pd.DataFrame(records)
            storage.insert_df("sofascore_data", records_df, if_exists="append")
            logger.info(f"Inserted {len(records)} records from {filepath.name}")
        
        return len(records)
        
    except Exception as e:
        logger.error(f"Failed to ingest {filepath.name}: {e}")
        return 0
    finally:
        storage.close()


def ingest_all_sofascore() -> int:
    """Ingest all Sofascore JSON files."""
    if not SOFARECORE_DIR.exists():
        logger.warning(f"Directory not found: {SOFARECORE_DIR}")
        return 0
    
    total = 0
    json_files = sorted(SOFARECORE_DIR.glob("*.json"))
    logger.info(f"Found {len(json_files)} JSON files")
    
    for filepath in json_files:
        count = ingest_sofascore_json(filepath)
        total += count
    
    logger.info(f"Total Sofascore records ingested: {total}")
    return total


if __name__ == "__main__":
    ingest_all_sofascore()
