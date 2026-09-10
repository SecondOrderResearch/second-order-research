"""Ingest existing raw football-data.co.uk CSVs into the warehouse."""

from __future__ import annotations

import pandas as pd
from pathlib import Path
from src.config import RAW_DIR, DB_PATH, LEAGUES
from src.pipeline.storage import Storage
from src.logging_config import setup_logging

logger = setup_logging("ingestion_football_data")

FOOTBALL_DATA_DIR = RAW_DIR / "football-data"


def ingest_football_data_csv(filepath: Path) -> int:
    """Ingest a single football-data.co.uk CSV file."""
    storage = Storage(DB_PATH)
    
    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig', on_bad_lines='skip')
        logger.info(f"Read {len(df)} rows from {filepath.name}")
        
        # Normalize column names
        df.columns = [c.strip() for c in df.columns]
        
        # Extract season from filename (e.g., E0_2425.csv -> 2024/25)
        parts = filepath.stem.split('_')
        if len(parts) >= 2:
            season_code = parts[1]
            if len(season_code) == 4:
                year_start = int(season_code[:2])
                year_end = int(season_code[2:])
                season = f"20{year_start}/{year_end}"
            else:
                season = "Unknown"
        else:
            season = "Unknown"
        
        # Determine division
        div = parts[0] if parts else "Unknown"
        division_map = {"E0": "Premier League", "E1": "Championship", "E2": "League One", "E3": "League Two", "SC0": "Scottish Premiership"}
        division = division_map.get(div, div)
        
        # Standardize column mapping
        records = []
        for _, row in df.iterrows():
            record = {
                "match_id": f"{season.replace('/', '')}_{div}_{row.name}",
                "competition": division,
                "season": season,
                "match_date": row.get("Date", ""),
                "kickoff_time": row.get("Time", ""),
                "home_team": row.get("HomeTeam", ""),
                "away_team": row.get("AwayTeam", ""),
                "home_goals": row.get("FTHG", None),
                "away_goals": row.get("FTAG", None),
                "result": row.get("FTR", ""),
                "home_shots": row.get("HS", None),
                "away_shots": row.get("AS", None),
                "home_shots_on_target": row.get("HST", None),
                "away_shots_on_target": row.get("AST", None),
                "home_corners": row.get("HC", None),
                "away_corners": row.get("AC", None),
                "home_fouls": row.get("HF", None),
                "away_fouls": row.get("AF", None),
                "home_yellows": row.get("HY", None),
                "away_yellows": row.get("AY", None),
                "home_reds": row.get("HR", None),
                "away_reds": row.get("AR", None),
                "referee": row.get("Referee", ""),
                "source_file": filepath.name,
            }
            records.append(record)
        
        if records:
            records_df = pd.DataFrame(records)
            storage.insert_df("football_data", records_df, if_exists="append")
            logger.info(f"Inserted {len(records)} records from {filepath.name}")
        
        return len(records)
        
    except Exception as e:
        logger.error(f"Failed to ingest {filepath.name}: {e}")
        return 0
    finally:
        storage.close()


def ingest_all_football_data() -> int:
    """Ingest all football-data.co.uk CSVs."""
    if not FOOTBALL_DATA_DIR.exists():
        logger.warning(f"Directory not found: {FOOTBALL_DATA_DIR}")
        return 0
    
    total = 0
    csv_files = sorted(FOOTBALL_DATA_DIR.glob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files")
    
    for filepath in csv_files:
        count = ingest_football_data_csv(filepath)
        total += count
    
    logger.info(f"Total records ingested: {total}")
    return total


if __name__ == "__main__":
    ingest_all_football_data()
