"""OpenWeatherMap client: geocoding, current weather and 5-day forecast (metric units)."""

from collections import Counter
from datetime import datetime, timedelta, timezone
from statistics import mean

import requests

from config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL, REQUEST_TIMEOUT

# Cache with Streamlit when available; plain functions otherwise (e.g. scripts).
try:
    import streamlit as st
    cache = st.cache_data
except ImportError:
    def cache(**_):
        return lambda func: func


class WeatherAPIError(Exception):
    """An error with a message safe to show to the user or the model."""


def _get(path: str, **params) -> dict | list:
    """GET an OpenWeatherMap endpoint and return parsed JSON."""
    try:
        response = requests.get(
            f"{OPENWEATHER_BASE_URL}{path}",
            params={**params, "appid": OPENWEATHER_API_KEY},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise WeatherAPIError("The weather service timed out. Please try again.")
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 401:
            raise WeatherAPIError("The weather service rejected the API key.")
        raise WeatherAPIError(f"The weather service returned an error ({status}).")
    except requests.RequestException:
        raise WeatherAPIError("Could not reach the weather service.")


def _city_time(timestamp: int, utc_offset: int) -> datetime:
    """Convert a UTC timestamp to the city's local time."""
    return datetime.fromtimestamp(timestamp, tz=timezone(timedelta(seconds=utc_offset)))


@cache(ttl=86400)
def geocode(city: str) -> tuple[float, float, str]:
    """Return (lat, lon, display name) for a city name."""
    results = _get("/geo/1.0/direct", q=city, limit=1)
    if not results:
        raise WeatherAPIError(f"City '{city}' not found. Try adding a country code, e.g. 'Paris, FR'.")
    place = results[0]
    name = ", ".join(part for part in (place.get("name"), place.get("country")) if part)
    return place["lat"], place["lon"], name


@cache(ttl=600)
def current_weather(city: str) -> dict:
    """Current conditions for a city, with sunrise/sunset in the city's local time."""
    lat, lon, name = geocode(city)
    data = _get("/data/2.5/weather", lat=lat, lon=lon, units="metric")
    offset = data["timezone"]
    sunrise, sunset = data["sys"]["sunrise"], data["sys"]["sunset"]
    return {
        "city": name,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["description"],
        "sunrise": _city_time(sunrise, offset).strftime("%I:%M %p"),
        "sunset": _city_time(sunset, offset).strftime("%I:%M %p"),
        "daylight_hours": round((sunset - sunrise) / 3600, 1),
    }


@cache(ttl=1800)
def forecast(city: str) -> dict:
    """5-day daily forecast for a city, with days split by the city's local date."""
    lat, lon, name = geocode(city)
    data = _get("/data/2.5/forecast", lat=lat, lon=lon, units="metric")
    offset = data["city"]["timezone"]

    by_day: dict = {}
    for slot in data["list"]:  # 3-hour slots
        by_day.setdefault(_city_time(slot["dt"], offset).date(), []).append(slot)

    days = [_summarise_day(day, slots) for day, slots in sorted(by_day.items())[:5]]
    return {"city": name, "days": days}


def _summarise_day(day, slots: list) -> dict:
    """Reduce a day's 3-hour slots to one daily summary."""
    temps = [s["main"]["temp"] for s in slots]
    conditions = Counter(s["weather"][0]["description"] for s in slots)
    return {
        "date": day.strftime("%a %d %b"),
        "temp_high": round(max(temps), 1),
        "temp_low": round(min(temps), 1),
        "condition": conditions.most_common(1)[0][0],
        "rain_chance": round(max(s.get("pop", 0) for s in slots) * 100),
        "humidity": round(mean(s["main"]["humidity"] for s in slots)),
        "wind_speed": round(mean(s["wind"]["speed"] for s in slots), 1),
    }
