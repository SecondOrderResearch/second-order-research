"""Fetch recent weather data from Open-Meteo."""

from __future__ import annotations

import requests
import pandas as pd
from pathlib import Path
from src.config import OPEN_METEO_BASE_URL, RAW_DIR, DATA_DIR, DB_PATH
from src.logging_config import setup_logging

logger = setup_logging("fetch_weather")

OPEN_METEO_DIR = RAW_DIR / "open-meteo"


def fetch_recent_weather() -> None:
    """Fetch recent weather data for major UK stadium locations."""
    # Major UK stadiums (lat, lon)
    stadiums = [
        (51.5074, -0.1278),  # London
        (53.4808, -2.2426),  # Manchester
        (52.4862, -1.8904),  # Birmingham
        (53.8008, -1.5491),  # Leeds
        (51.4545, -2.5879),  # Bristol
        (53.9576, -1.0827),  # York
        (55.9533, -3.1883),  # Edinburgh
        (55.8642, -4.2518),  # Glasgow
    ]
    
    OPEN_METEO_DIR.mkdir(parents=True, exist_ok=True)
    
    for i, (lat, lon) in enumerate(stadiums):
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": "2025-08-01",
                "end_date": "2025-12-31",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
                "timezone": "Europe/London"
            }
            
            response = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if "daily" in data:
                    df = pd.DataFrame(data["daily"])
                    df["latitude"] = lat
                    df["longitude"] = lon
                    filepath = OPEN_METEO_DIR / f"weather_{lat}_{lon}.csv"
                    df.to_csv(filepath, index=False)
                    logger.info(f"Fetched weather for {lat},{lon}")
            else:
                logger.warning(f"Weather API returned {response.status_code} for {lat},{lon}")
                
        except Exception as e:
            logger.error(f"Failed to fetch weather for {lat},{lon}: {e}")


if __name__ == "__main__":
    fetch_recent_weather()
