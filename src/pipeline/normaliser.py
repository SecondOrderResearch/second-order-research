import re
from typing import Dict

# Manual override table for names that normalisers get wrong
OVERRIDES = {
    "Manchester Utd": "Manchester United",
    "Man Utd": "Manchester United",
    "Man City": "Manchester City",
    "Tottenham": "Tottenham Hotspur",
    "Spurs": "Tottenham Hotspur",
    "West Ham": "West Ham United",
    "Wolves": "Wolverhampton Wanderers",
    "Newcastle": "Newcastle United",
    "Nottm Forest": "Nottingham Forest",
    "Sheff Utd": "Sheffield United",
    "Sheff Wed": "Sheffield Wednesday",
    "Brighton": "Brighton & Hove Albion",
    "Hove Albion": "Brighton & Hove Albion",
}

def normalise_team_name(name: str) -> str:
    if not name:
        return name
    name = name.strip()
    return OVERRIDES.get(name, name)

def build_alias_map(raw_names: list[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for raw in raw_names:
        norm = normalise_team_name(raw)
        mapping[raw] = norm
    return mapping
