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
GEOCODING_API_URL = "https://api.openweathermap.org/geo/1.0/direct"

# System prompt
SYSTEM_PROMPT = """You are a helpful weather assistant. When users ask about weather, 
use the get_weather tool to provide accurate, current weather information. 
Be conversational and friendly."""