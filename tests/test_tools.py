"""Unit tests for tools module."""

import pytest
from unittest.mock import patch, Mock
from tools import get_coordinates_from_city, get_weather


class TestGetCoordinatesFromCity:
    """Tests for city to coordinates conversion."""
    
    @patch('tools.requests.get')
    def test_valid_city_returns_coordinates(self, mock_get):
        """Test that a valid city returns lat/lon coordinates."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = [
            {"lat": 51.5074, "lon": -0.1278, "name": "London"}
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test
        result = get_coordinates_from_city("London")
        
        # Assert
        assert result is not None
        assert result == (51.5074, -0.1278)
    
    @patch('tools.requests.get')
    def test_invalid_city_returns_none(self, mock_get):
        """Test that an invalid city returns None."""
        # Mock API response with empty list
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test
        result = get_coordinates_from_city("InvalidCityXYZ123")
        
        # Assert
        assert result is None
    
    @patch('tools.requests.get')
    def test_api_timeout_returns_none(self, mock_get):
        """Test that API timeout is handled gracefully."""
        # Mock timeout exception
        mock_get.side_effect = Exception("Timeout")
        
        # Test
        result = get_coordinates_from_city("London")
        
        # Assert
        assert result is None


class TestGetWeather:
    """Tests for weather data fetching."""
    
    @patch('tools.requests.get')
    def test_valid_coordinates_returns_weather(self, mock_get):
        """Test that valid coordinates return weather data."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "main": {
                "temp": 15.5,
                "feels_like": 14.2,
                "humidity": 65
            },
            "weather": [
                {"description": "partly cloudy"}
            ],
            "wind": {
                "speed": 3.5
            },
            "name": "London"
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Test
        result = get_weather(51.5074, -0.1278)
        
        # Assert
        assert result is not None
        assert result["temperature"] == 15.5
        assert result["condition"] == "partly cloudy"
        assert result["location"] == "London"
    
    @patch('tools.requests.get')
    def test_api_error_raises_exception(self, mock_get):
        """Test that API errors are properly raised."""
        # Mock HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        
        # Test
        with pytest.raises(Exception):
            get_weather(51.5074, -0.1278)


# Run tests with: pytest tests/test_tools.py -v