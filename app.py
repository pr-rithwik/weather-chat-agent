"""Weather Chat Agent: a Streamlit chat app where Claude fetches weather data with tools."""

from dataclasses import asdict

import anthropic
import streamlit as st

import ui
from agent import build_system_prompt, run_agent
from config import MAX_HISTORY_MESSAGES
from utils import trim_history


def init_state() -> None:
    if "messages" not in st.session_state:
        ui.reset_session()


def ask_agent(prompt: str, unit: str, home_city: str) -> None:
    """Send the prompt (with recent history) to the agent and store the reply."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    ui.message(st.session_state.messages[-1], unit, len(st.session_state.messages) - 1)

    # Claude only needs the text of past turns; fetched data stays in the UI.
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

    with st.chat_message("assistant"), st.spinner("Checking the weather..."):
        try:
            result = run_agent(trim_history(history, MAX_HISTORY_MESSAGES),
                               build_system_prompt(unit, home_city))
        except anthropic.APIError as e:
            st.session_state.messages.pop()  # let the user retry the same question
            st.error(f"Claude is unavailable right now ({type(e).__name__}). Please try again.")
            return

    st.session_state.input_tokens += result.input_tokens
    st.session_state.output_tokens += result.output_tokens
    st.session_state.messages.append({
        "role": "assistant",
        "content": result.text or "_(no reply)_",
        "tool_calls": [asdict(c) for c in result.tool_calls if not c.is_error],
    })
    st.rerun()


def main() -> None:
    st.set_page_config(page_title="Weather Chat Agent", page_icon="🌤️")
    init_state()

    unit, home_city = ui.sidebar()
    st.title("🌤️ Weather Chat Agent")

    clicked = ui.welcome() if not st.session_state.messages else None
    for index, msg in enumerate(st.session_state.messages):
        ui.message(msg, unit, index)

    prompt = st.chat_input("Ask about the weather anywhere...") or clicked
    if prompt:
        ask_agent(prompt, unit, home_city)


if __name__ == "__main__":
    main()
