"""Small helpers: history trimming, cost and unit conversion."""

from config import PRICE_PER_MTOK


def trim_history(messages: list[dict], max_messages: int) -> list[dict]:
    """Keep the last N messages; the first one sent to Claude must be from the user."""
    trimmed = messages[-max_messages:]
    while trimmed and trimmed[0]["role"] != "user":
        trimmed = trimmed[1:]
    return trimmed


def cost_usd(input_tokens: int, output_tokens: int) -> float:
    return (input_tokens * PRICE_PER_MTOK["input"]
            + output_tokens * PRICE_PER_MTOK["output"]) / 1_000_000


def to_unit(celsius: float, unit: str) -> float:
    return celsius * 9 / 5 + 32 if unit == "F" else celsius
