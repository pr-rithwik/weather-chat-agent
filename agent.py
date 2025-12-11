"""Core agent logic for handling Claude API and tool orchestration."""

from typing import Tuple
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS, SYSTEM_PROMPT
from tools import WEATHER_TOOL, get_weather


def chat(message: str, latitude: float, longitude: float) -> str:
    """Main entry point for chat interaction."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Initial call to Claude with tool definitions
    response = call_claude_with_tools(client, message, latitude, longitude)
    
    # Handle tool use if Claude requests it
    if response.stop_reason == "tool_use":
        tool_result = execute_tool(response.content)
        final_response = send_tool_result(client, message, response, tool_result, latitude, longitude)
        return extract_text(final_response.content)
    
    return extract_text(response.content)


def call_claude_with_tools(
    client: anthropic.Anthropic,
    message: str,
    latitude: float,
    longitude: float
) -> anthropic.types.Message:
    """Call Claude API with tool definitions."""
    return client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[WEATHER_TOOL],
        messages=[{
            "role": "user",
            "content": f"My location: latitude {latitude}, longitude {longitude}\n\n{message}"
        }]
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
    
    raise ValueError("No tool use block found")


def send_tool_result(
    client: anthropic.Anthropic,
    original_message: str,
    initial_response: anthropic.types.Message,
    tool_result: Tuple[str, str, dict],
    latitude: float,
    longitude: float
) -> anthropic.types.Message:
    """Send tool execution result back to Claude."""
    tool_id, tool_name, result = tool_result
    
    return client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[WEATHER_TOOL],
        messages=[
            {
                "role": "user",
                "content": f"My location: latitude {latitude}, longitude {longitude}\n\n{original_message}"
            },
            {
                "role": "assistant",
                "content": initial_response.content
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": str(result)
                    }
                ]
            }
        ]
    )


def extract_text(content: list) -> str:
    """Extract text from Claude's response content."""
    for block in content:
        if hasattr(block, 'text'):
            return block.text
    return ""