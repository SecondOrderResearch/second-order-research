from geopy.distance import geodesic
from typing import Tuple

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in km."""
    return geodesic((lat1, lon1), (lat2, lon2)).km

def travel_distance_km(home_lat: float, home_lon: float, away_lat: float, away_lon: float) -> float:
    """Return haversine distance from away team home to match venue."""
    return haversine_km(away_lat, away_lon, home_lat, home_lon)
