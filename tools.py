"""Tool definitions and implementations for the weather agent."""

from typing import Dict, Optional, Tuple, List
import requests
import streamlit as st
from config import OPENWEATHER_API_KEY, WEATHER_API_URL, GEOCODING_API_URL, FORECAST_API_URL


# Current weather tool schema
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

# Weather forecast tool schema
FORECAST_TOOL = {
    "name": "get_forecast",
    "description": "Get 5-day weather forecast for a specific location. Use this when users ask about future weather, this week, upcoming days, or tomorrow.",
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


@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_weather(latitude: float, longitude: float) -> Dict[str, any]:
    """Fetch current weather data from OpenWeatherMap API."""
    try:
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
    except requests.exceptions.Timeout:
        raise Exception("Weather service is taking too long to respond. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("Weather service authentication failed. Please contact support.")
        raise Exception(f"Weather service error: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Unable to fetch weather data: {str(e)}")


@st.cache_data(ttl=1800)  # Cache for 30 minutes (forecasts change less frequently)
def get_forecast(latitude: float, longitude: float) -> Dict[str, any]:
    """Fetch 5-day weather forecast from OpenWeatherMap API."""
    try:
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "cnt": 40  # 5 days * 8 readings per day (3-hour intervals)
        }
        
        response = requests.get(FORECAST_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Group forecasts by day
        daily_forecasts = {}
        for item in data["list"]:
            from datetime import datetime
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    "date": datetime.fromtimestamp(item["dt"]).strftime("%A, %B %d"),
                    "temps": [],
                    "conditions": [],
                    "humidity": [],
                    "wind_speed": []
                }
            
            daily_forecasts[date]["temps"].append(item["main"]["temp"])
            daily_forecasts[date]["conditions"].append(item["weather"][0]["description"])
            daily_forecasts[date]["humidity"].append(item["main"]["humidity"])
            daily_forecasts[date]["wind_speed"].append(item["wind"]["speed"])
        
        # Compute daily averages
        forecast_list = []
        for date_key in sorted(daily_forecasts.keys())[:5]:  # Only 5 days
            day_data = daily_forecasts[date_key]
            forecast_list.append({
                "date": day_data["date"],
                "temp_high": round(max(day_data["temps"]), 1),
                "temp_low": round(min(day_data["temps"]), 1),
                "temp_avg": round(sum(day_data["temps"]) / len(day_data["temps"]), 1),
                "condition": max(set(day_data["conditions"]), key=day_data["conditions"].count),
                "humidity": round(sum(day_data["humidity"]) / len(day_data["humidity"])),
                "wind_speed": round(sum(day_data["wind_speed"]) / len(day_data["wind_speed"]), 1)
            })
        
        return {
            "location": data["city"]["name"],
            "forecast": forecast_list
        }
    except requests.exceptions.Timeout:
        raise Exception("Forecast service is taking too long to respond. Please try again.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise Exception("Forecast service authentication failed. Please contact support.")
        raise Exception(f"Forecast service error: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Unable to fetch forecast data: {str(e)}")


@st.cache_data(ttl=3600)  # Cache city coordinates for 1 hour
def get_coordinates_from_city(city: str) -> Optional[Tuple[float, float]]:
    """Convert city name to coordinates using OpenWeatherMap Geocoding API."""
    try:
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
    except requests.exceptions.Timeout:
        raise Exception("Location service timed out. Please try again.")
    except Exception:
        return None