"""Core agent logic for handling Claude API and tool orchestration."""

from typing import Tuple, List, Dict
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, SYSTEM_PROMPT
from tools import WEATHER_TOOL, FORECAST_TOOL, get_weather, get_forecast


def chat(message: str, latitude: float, longitude: float, history: List[Dict] = None) -> str:
    """Main entry point for chat interaction."""
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        history = history or []

        response = call_claude_with_tools(client, message, latitude, longitude, history)

        if response.stop_reason == "tool_use":
            try:
                tool_result = execute_tool(response.content)
                final_response = send_tool_result(client, message, response, tool_result, latitude, longitude, history)
                return extract_text(final_response.content)
            except Exception as tool_error:
                return f"I tried to fetch weather data but encountered an error: {str(tool_error)}"

        return extract_text(response.content)
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


def build_messages(message: str, latitude: float, longitude: float, history: List[Dict]) -> list:
    """Build full message list for Claude, threading conversation history.

    Location is injected only into the first user message so it's available
    for the whole conversation without repeating it on every turn.
    """
    messages = []

    for i, msg in enumerate(history):
        if i == 0 and msg["role"] == "user":
            messages.append({
                "role": "user",
                "content": f"My location: latitude {latitude}, longitude {longitude}\n\n{msg['content']}"
            })
        else:
            messages.append(msg)

    if not history:
        # First ever message — prepend location
        messages.append({
            "role": "user",
            "content": f"My location: latitude {latitude}, longitude {longitude}\n\n{message}"
        })
    else:
        messages.append({"role": "user", "content": message})

    return messages


def call_claude_with_tools(
    client: anthropic.Anthropic,
    message: str,
    latitude: float,
    longitude: float,
    history: List[Dict]
) -> anthropic.types.Message:
    """Call Claude API with tool definitions and full conversation history."""
    return client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[WEATHER_TOOL, FORECAST_TOOL],
        messages=build_messages(message, latitude, longitude, history)
    )


def execute_tool(content: list) -> Tuple[str, str, dict]:
    """Execute the tool requested by Claude."""
    for block in content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            tool_id = block.id

            if tool_name == "get_weather":
                result = get_weather(**tool_input)
                return tool_id, tool_name, result
            elif tool_name == "get_forecast":
                result = get_forecast(**tool_input)
                return tool_id, tool_name, result

    raise ValueError("No tool use block found")


def send_tool_result(
    client: anthropic.Anthropic,
    original_message: str,
    initial_response: anthropic.types.Message,
    tool_result: Tuple[str, str, dict],
    latitude: float,
    longitude: float,
    history: List[Dict]
) -> anthropic.types.Message:
    """Send tool execution result back to Claude, preserving history."""
    tool_id, tool_name, result = tool_result

    messages = build_messages(original_message, latitude, longitude, history)
    messages.append({"role": "assistant", "content": initial_response.content})
    messages.append({
        "role": "user",
        "content": [{
            "type": "tool_result",
            "tool_use_id": tool_id,
            "content": str(result)
        }]
    })

    return client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[WEATHER_TOOL, FORECAST_TOOL],
        messages=messages
    )


def extract_text(content: list) -> str:
    """Extract text from Claude's response content."""
    for block in content:
        if hasattr(block, 'text'):
            return block.text
    return ""