"""Streamlit rendering: sidebar, chat messages and the weather data the agent fetched."""

import streamlit as st

from charts import forecast_chart, weather_icon
from utils import cost_usd, to_unit

EXAMPLE_PROMPTS = [
    "Should I carry an umbrella in Hyderabad today?",
    "Goa or Mumbai for a beach trip this weekend?",
    "Which day this week is best for a run in Bengaluru?",
    "What does 80% humidity actually feel like?",
]


def sidebar() -> tuple[str, str]:
    """Settings and session stats. Returns (unit, home_city)."""
    with st.sidebar:
        st.header("Settings")
        unit = st.radio("Temperature", ["C", "F"], format_func=lambda u: f"°{u}", horizontal=True)
        home_city = st.text_input("Your city (optional)", placeholder="e.g. Hyderabad",
                                  help="Used when you don't name a city.")

        st.header("This session")
        tokens_in, tokens_out = st.session_state.input_tokens, st.session_state.output_tokens
        st.metric("Cost", f"${cost_usd(tokens_in, tokens_out):.4f}")
        st.caption(f"{tokens_in:,} input / {tokens_out:,} output tokens")

        if st.session_state.messages and st.button("New chat", width="stretch"):
            reset_session()
            st.rerun()
    return unit, home_city.strip()


def reset_session() -> None:
    st.session_state.messages = []
    st.session_state.input_tokens = 0
    st.session_state.output_tokens = 0


def welcome() -> str | None:
    """Intro and example prompts. Returns a prompt if one was clicked."""
    st.markdown("Ask about the weather anywhere. I'll fetch live data when I need it.")
    columns = st.columns(2)
    for i, prompt in enumerate(EXAMPLE_PROMPTS):
        if columns[i % 2].button(prompt, width="stretch"):
            return prompt
    return None


def message(msg: dict, unit: str, index: int) -> None:
    """A chat message, plus the weather data the agent used for it.

    `index` is the message's position in the chat; it keeps widget keys unique
    when the same city's data appears more than once.
    """
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for call_index, call in enumerate(msg.get("tool_calls", [])):
            if call["name"] == "get_current_weather":
                current_card(call["result"], unit)
            elif call["name"] == "get_forecast":
                forecast_card(call["result"], unit, key=f"forecast-{index}-{call_index}")


def current_card(data: dict, unit: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{weather_icon(data['condition'])} {data['city']}** · now · "
                    f"{data['condition'].capitalize()}")
        temp, feels, humidity, wind = st.columns(4)
        temp.metric("Temp", f"{to_unit(data['temperature'], unit):.0f}°{unit}")
        feels.metric("Feels like", f"{to_unit(data['feels_like'], unit):.0f}°{unit}")
        humidity.metric("Humidity", f"{data['humidity']}%")
        wind.metric("Wind", f"{data['wind_speed']:.1f} m/s")
        st.caption(f"Sunrise {data['sunrise']} · Sunset {data['sunset']} · "
                   f"{data['daylight_hours']} h daylight (local time)")


def forecast_card(data: dict, unit: str, key: str) -> None:
    with st.container(border=True):
        st.markdown(f"**📅 {data['city']}** · 5-day forecast")
        st.plotly_chart(forecast_chart(data, unit), width="stretch", key=key)