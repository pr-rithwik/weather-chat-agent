"""Tool definitions and implementations for the weather agent."""

from typing import Dict, Optional, Tuple
import requests
from config import OPENWEATHER_API_KEY, WEATHER_API_URL, GEOCODING_API_URL


# Tool schema for Claude
WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Get current weather information for a specific location using coordinates",
    "input_schema": {
        "type": "object",
        "properties": {
            "latitude": {
                "type": "number",
                "description": "Latitude of the location"
            },
            "longitude": {
                "type": "number",
                "description": "Longitude of the location"
            }
        },
        "required": ["latitude", "longitude"]
    }
}


def get_weather(latitude: float, longitude: float) -> Dict[str, any]:
    """Fetch current weather data from OpenWeatherMap API."""
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    
    response = requests.get(WEATHER_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "condition": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "location": data["name"]
    }


def get_coordinates_from_city(city: str) -> Optional[Tuple[float, float]]:
    """Convert city name to coordinates using OpenWeatherMap Geocoding API."""
    params = {
        "q": city,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }
    
    response = requests.get(GEOCODING_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if not data:
        return None
    
    return data[0]["lat"], data[0]["lon"]