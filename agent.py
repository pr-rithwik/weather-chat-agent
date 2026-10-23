"""The agent loop: Claude decides which tools to call; we run them until it answers."""

import json
from dataclasses import dataclass, field
from functools import lru_cache

import anthropic

from config import (ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_AGENT_STEPS,
                    MAX_TOKENS, SYSTEM_PROMPT)
from tools import TOOLS, run_tool


@dataclass
class ToolCall:
    name: str
    input: dict
    result: dict | str
    is_error: bool


@dataclass
class AgentResult:
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0


@lru_cache(maxsize=1)
def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def build_system_prompt(unit: str, home_city: str = "") -> str:
    """Fill the system prompt with per-session context (rebuilt every turn)."""
    home_city_line = (
        f"The user's home city is {home_city}. Use it when they don't name a place."
        if home_city else
        "If the user doesn't name a place, ask which city they mean."
    )
    return SYSTEM_PROMPT.format(unit=f"°{unit}", home_city_line=home_city_line)


def run_agent(messages: list[dict], system: str, client=None) -> AgentResult:
    """Call Claude, run every tool it asks for, and repeat until it gives a final answer."""
    client = client or get_client()
    messages = list(messages)  # don't modify the caller's history
    result = AgentResult()

    for _ in range(MAX_AGENT_STEPS):
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            tools=TOOLS,
            messages=messages,
        )
        result.input_tokens += response.usage.input_tokens
        result.output_tokens += response.usage.output_tokens

        if response.stop_reason != "tool_use":
            result.text = "".join(b.text for b in response.content if b.type == "text")
            return result

        # Claude may ask for several tools at once; every request needs a result.
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            output, is_error = run_tool(block.name, block.input)
            result.tool_calls.append(ToolCall(block.name, block.input, output, is_error))
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output if is_error else json.dumps(output),
                "is_error": is_error,
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    result.text = "Sorry, that took too many steps. Could you ask a simpler question?"
    return result
