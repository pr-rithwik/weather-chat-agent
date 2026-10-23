"""App settings: API keys, model, limits and the system prompt."""

import os

from dotenv import load_dotenv

load_dotenv()


def _secret(name: str) -> str | None:
    """Read a key from Streamlit secrets (cloud), falling back to env vars (local)."""
    try:
        import streamlit as st
        return st.secrets.get(name) or os.getenv(name)
    except Exception:
        return os.getenv(name)


ANTHROPIC_API_KEY = _secret("ANTHROPIC_API_KEY")
OPENWEATHER_API_KEY = _secret("OPENWEATHER_API_KEY")

# Claude
CLAUDE_MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 1024
MAX_AGENT_STEPS = 5          # max tool rounds per user message
MAX_HISTORY_MESSAGES = 20    # messages sent to Claude per turn

# USD per million tokens. Check https://platform.claude.com/docs/en/about-claude/pricing
PRICE_PER_MTOK = {"input": 2.0, "output": 10.0}

# OpenWeatherMap
OPENWEATHER_BASE_URL = "https://api.openweathermap.org"
REQUEST_TIMEOUT = 10

SYSTEM_PROMPT = """You are a weather assistant in a chat app.

How to work:
- Use get_current_weather for conditions right now and get_forecast for anything in the next 5 days.
- Fetch data for every city the question needs. For comparisons, fetch each city.
- Never guess weather numbers. Only use data returned by the tools.
- If a tool returns an error (for example, city not found), say so and ask the user to clarify.
- General questions that need no live data (e.g. "what does 80% humidity feel like?") need no tool.

How to answer:
- Answer the question directly first, then give up to 3 short, practical tips based on the data.
- Be concise. The app shows the fetched data as cards and charts under your reply, so don't list every number.
- Give temperatures in {unit} and wind in m/s.

{home_city_line}"""
