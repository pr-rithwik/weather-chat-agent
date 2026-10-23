"""Unit tests for the weather API client and tool dispatcher (HTTP is mocked)."""

from unittest.mock import Mock, patch

import pytest
import requests
import streamlit as st

from tools import run_tool
from weather_api import WeatherAPIError, current_weather, forecast, geocode

LONDON = [{"lat": 51.5, "lon": -0.12, "name": "London", "country": "GB"}]


@pytest.fixture(autouse=True)
def clear_cache():
    st.cache_data.clear()
    yield


def response(json_data=None, error=None):
    """A fake requests.Response."""
    resp = Mock()
    resp.json.return_value = json_data
    resp.raise_for_status = Mock(side_effect=error)
    return resp


class TestGeocode:
    @patch("weather_api.requests.get")
    def test_valid_city_returns_coordinates(self, mock_get):
        mock_get.return_value = response(LONDON)
        assert geocode("London") == (51.5, -0.12, "London, GB")

    @patch("weather_api.requests.get")
    def test_unknown_city_raises(self, mock_get):
        mock_get.return_value = response([])
        with pytest.raises(WeatherAPIError, match="not found"):
            geocode("NoSuchCity")

    @patch("weather_api.requests.get")
    def test_timeout_raises(self, mock_get):
        mock_get.side_effect = requests.Timeout()
        with pytest.raises(WeatherAPIError, match="timed out"):
            geocode("London")


class TestCurrentWeather:
    @patch("weather_api.requests.get")
    def test_returns_weather_in_city_local_time(self, mock_get):
        mock_get.side_effect = [
            response(LONDON),
            response({
                "main": {"temp": 15.5, "feels_like": 14.2, "humidity": 65},
                "weather": [{"description": "few clouds"}],
                "wind": {"speed": 3.5},
                "sys": {"sunrise": 1700000000, "sunset": 1700030000},
                "timezone": 3600,  # UTC+1
            }),
        ]
        result = current_weather("London")
        assert result["city"] == "London, GB"
        assert result["temperature"] == 15.5
        assert result["sunrise"] == "11:13 PM"  # 22:13 UTC + 1h
        assert result["daylight_hours"] == 8.3

    @patch("weather_api.requests.get")
    def test_bad_api_key_raises(self, mock_get):
        error = requests.HTTPError(response=Mock(status_code=401))
        mock_get.side_effect = [response(LONDON), response(error=error)]
        with pytest.raises(WeatherAPIError, match="API key"):
            current_weather("London")


class TestForecast:
    @patch("weather_api.requests.get")
    def test_groups_slots_into_at_most_five_days(self, mock_get):
        slots = [{
            "dt": 1702800000 + i * 10800,  # every 3 hours
            "main": {"temp": 10 + i % 8, "humidity": 70},
            "weather": [{"description": "light rain"}],
            "wind": {"speed": 3.0},
            "pop": 0.4,
        } for i in range(40)]
        mock_get.side_effect = [response(LONDON),
                                response({"city": {"timezone": 0}, "list": slots})]

        result = forecast("London")
        assert result["city"] == "London, GB"
        assert len(result["days"]) == 5
        assert result["days"][0]["rain_chance"] == 40

    def test_tool_errors_are_returned_not_raised(self):
        with patch("weather_api.requests.get", return_value=response([])):
            result, is_error = run_tool("get_forecast", {"city": "NoSuchCity"})
        assert is_error and "not found" in result