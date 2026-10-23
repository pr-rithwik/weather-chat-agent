# 🌤️ Weather Chat Agent

A conversational weather agent built on Claude's tool use API. Ask about the weather anywhere, in plain English. Claude decides which cities and what kind of data your question needs, fetches it with tools, and answers with practical advice.

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.50+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live_Demo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://weather94.streamlit.app)

---


## What it does

Ask things like:

- *"Should I carry an umbrella in Hyderabad today?"* → current weather for one city
- *"Goa or Mumbai for a beach trip this weekend?"* → forecasts for both cities, compared
- *"What does 80% humidity feel like?"* → no data needed, so no tool call

Claude answers first, then adds a few tips based on the data. Every reply shows the data the agent actually fetched as cards (current conditions) and charts (5-day forecast).

---

## How the agent works

```
user message ─► Claude (system prompt + tools + recent history)
                   │
                   ├─ no tool needed ─────────────────────► answer
                   │
                   └─ tool_use: get_forecast("Goa"), get_forecast("Mumbai")
                          │   run every requested tool
                          ▼
                      tool_result(s) ─► Claude ─► (more tools? loop) ─► answer
```

- **Claude chooses the actions.** It picks the tool and the city. Nothing is pre-fetched by the UI.
- **Multi-step loop.** The agent keeps running tools until Claude gives a final answer, capped at `MAX_AGENT_STEPS`.
- **Parallel tool calls.** If Claude asks for several tools at once (e.g. two cities), all of them run and their results go back together.
- **Errors go back to Claude.** "City not found" or a timeout is returned as an error tool result, so Claude can explain or ask for clarification instead of the app crashing.

---

## Key technical decisions

**City-name tools, geocoded inside.** Claude passes a city name; the tool converts it to coordinates with OpenWeatherMap's Geocoding API. The model never has to supply coordinates it can't know.

**Insights from the same LLM call.** Tips come from Claude's own reasoning over the fetched data, in the same turn. No hard-coded rules and no extra API call.

**Context in the system prompt.** The temperature unit and the user's home city (optional) are added to the system prompt each turn, so changing them takes effect immediately.

**Bounded history.** Only the last `MAX_HISTORY_MESSAGES` messages are sent, so cost per turn doesn't keep growing.

**Real cost tracking.** The sidebar adds up the exact token counts Claude returns for every call in the loop.

**Caching.** Geocoding is cached for 24 h, forecasts for 30 min and current weather for 10 min. Repeat questions don't hit the API again.

**City-local times.** Sunrise, sunset and forecast days use the city's own time zone, not the server's.

---

## Stack

| Layer | Choice |
|---|---|
| UI | Streamlit |
| AI | Claude Sonnet 5.5 (tool use) |
| Weather data | OpenWeatherMap (geocoding, current, 5-day forecast) |
| Charts | Plotly |
| Testing | pytest with mocked HTTP |
| Deployment | Streamlit Cloud |

---

## Project structure

```
weather-chat-agent/
├── app.py           # Entry point: session state and the chat flow
├── ui.py            # Streamlit rendering: sidebar, messages, weather cards
├── agent.py         # Agent loop: Claude + tool execution + token usage
├── tools.py         # Tool schemas and the dispatcher Claude's requests run through
├── weather_api.py   # OpenWeatherMap client with caching
├── charts.py        # Forecast chart and weather icons
├── utils.py         # History trimming, cost, unit conversion
├── config.py        # Keys, model, limits and the system prompt
├── tests/
│   └── test_tools.py
├── CHAT_GUIDE.md    # What you can ask the agent
└── requirements.txt
```

---

## Running locally

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

## Limitations

- Forecast is daily, up to 5 days. No hourly breakdown or historical weather.
- Chat history lives in the browser session and resets on refresh.
