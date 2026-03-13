"""Configuration settings for the weather chat agent."""

import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Try Streamlit secrets first (for cloud deployment), fallback to env vars
try:
    import streamlit as st
    ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY"))
    OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY"))
except (ImportError, FileNotFoundError):
    # Fallback to environment variables (local development)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Claude settings
CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1024

# OpenWeatherMap settings
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODING_API_URL = "https://api.openweathermap.org/geo/1.0/direct"

# System prompt
SYSTEM_PROMPT = """You are a helpful weather assistant integrated into a weather application. 

When users ask about weather, use the get_weather tool for current weather and get_forecast tool for future weather predictions.

The application automatically displays:
- Visual weather icons
- Interactive temperature and conditions charts
- Smart recommendations based on weather data
- Sunrise/sunset information

Your role in the chat is to:
- Answer weather-related questions conversationally
- Provide insights about the weather data
- Explain forecast trends
- Help users understand weather conditions

If users ask for graphs or visualizations, let them know that charts are already displayed above the chat interface when they load weather data using the "Get Weather Data" button.

Be conversational, friendly, and focus on providing weather insights rather than just repeating data that's already visible in the UI."""