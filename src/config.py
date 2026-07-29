import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
EXPORTS_DIR = DATA_DIR / "exports"
RESEARCH_DIR = BASE_DIR / "research"
SCRIPTS_DIR = BASE_DIR / "scripts"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Database
DB_PATH = WAREHOUSE_DIR / "second_order_research.db"
DB_URL = f"sqlite:///{DB_PATH}"

# API keys (set in .env or environment)
FOOTBALL_DATA_ORG_API_KEY = os.getenv("FOOTBALL_DATA_ORG_API_KEY", "")
OPEN_METEO_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "")

# Leagues and competitions
LEAGUES = {
    "Premier League": {"id": "PL", "country": "England"},
    "Championship": {"id": "EL1", "country": "England"},
    "League One": {"id": "EL2", "country": "England"},
    "League Two": {"id": "EL3", "country": "England"},
    "Scottish Premiership": {"id": "SPL", "country": "Scotland"},
}

SEASONS = ["2022/23", "2023/24", "2024/25"]

# Feature engineering
REST_CONGESTION_SHORT = 3  # days
REST_CONGESTION_LONG = 7  # days
TRAVEL_SHORT_KM = 300
TRAVEL_LONG_KM = 800
WIND_HIGH_KPH = 30
HUMIDITY_HIGH_PCT = 80
PRECIP_MM_HEAVY = 5
MIN_SAMPLE_SIZE = 30

# Hypothesis registry config
HYPOTHESIS_REGISTRY_PATH = RESEARCH_DIR / "hypotheses.yaml"

# Logging
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
