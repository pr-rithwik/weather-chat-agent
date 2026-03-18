# 🌤️ Weather Chat Agent

A conversational weather agent built on Claude's function calling API. Ask natural language questions about current conditions or the week ahead — Claude decides when to fetch data, reasons over it, and responds in context.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.39+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![Live Demo](https://img.shields.io/badge/Live_Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://weather94.streamlit.app)

---

## Demo

![Demo](assets/demo.gif)

---

## What it does

Type something like *"should I bring a jacket tonight?"* or *"which day this week is best for hiking?"* — Claude fetches live weather or forecast data as needed, factors in feels-like temperature, humidity, wind, and conditions together, and gives you a direct answer rather than a list of numbers.

The app also renders a visual dashboard alongside the chat: current conditions with sunrise/sunset, interactive 5-day temperature and humidity charts, and contextual recommendations. The chat remembers the full conversation, so follow-up questions work naturally.

---

## Key Technical Decisions

**Function calling over prompt engineering** — Claude is given tool schemas for `get_weather` and `get_forecast` and decides autonomously when to call them. A question like *"is it going to rain?"* triggers a forecast fetch while *"what does 80% humidity feel like?"* doesn't hit the API at all.

**Stateful conversation** — each chat turn passes the full message history to Claude, not just the current message. Location context is injected once into the first user message rather than repeated on every turn, keeping the token count lean.

**Caching at the right granularity** — geocoding results cache for 1 hour (coordinates don't change), forecasts for 30 minutes, current weather for 10 minutes. This avoids redundant API calls when the dashboard and chat both need the same data.

**Test-safe imports** — `@st.cache_data` is guarded behind a try/except so `tools.py` can be imported in pytest without a running Streamlit context. This was a real issue once the caching layer was added.

---

## Stack

| Layer | Choice |
|---|---|
| UI | Streamlit |
| AI | Claude Sonnet 4 (function calling) |
| Weather data | OpenWeatherMap (current + forecast) |
| Charts | Plotly |
| Testing | pytest with mocking |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
weather-chat-agent/
├── app.py              # Streamlit UI and session state
├── agent.py            # Agentic loop — Claude + tool orchestration
├── tools.py            # API calls, tool schemas, caching
├── charts.py           # Plotly chart generation
├── recommendations.py  # Contextual weather tips and forecast insights
├── config.py           # Settings and system prompt
├── utils.py            # Token estimation and cost tracking
├── tests/
│   └── test_tools.py
├── CHAT_GUIDE.md       # What you can ask the agent
└── requirements.txt
```

---

## Running Locally

```bash
git clone https://github.com/pr-rithwik/weather-chat-agent.git
cd weather-chat-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your API keys
streamlit run app.py
```

```bash
# Tests
pytest tests/ -v
```

You'll need an [Anthropic API key](https://console.anthropic.com/) and a free [OpenWeatherMap key](https://openweathermap.org/api).

---

## Cost

The sidebar tracks token usage and estimated cost per session. See current Claude Sonnet pricing at [Anthropic's pricing page](https://www.anthropic.com/pricing). OpenWeatherMap's free tier covers 1,000 calls/day — well above what the caching layer allows through.
