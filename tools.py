"""Tools Claude can call: their schemas and a dispatcher that runs them."""

from weather_api import WeatherAPIError, current_weather, forecast


def _city_tool(name: str, description: str) -> dict:
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, optionally with a country code, e.g. 'Hyderabad' or 'Paris, FR'.",
                }
            },
            "required": ["city"],
        },
    }


TOOLS = [
    _city_tool(
        "get_current_weather",
        "Get the weather right now in a city: temperature, feels-like, humidity, wind, "
        "condition, sunrise and sunset.",
    ),
    _city_tool(
        "get_forecast",
        "Get a 5-day daily forecast for a city: high/low temperature, condition, chance of rain, "
        "humidity and wind. Use for today's outlook, tomorrow, the weekend or this week.",
    ),
]

_FUNCTIONS = {
    "get_current_weather": current_weather,
    "get_forecast": forecast,
}


def run_tool(name: str, tool_input: dict) -> tuple[dict | str, bool]:
    """Run a tool by name. Returns (result, is_error); errors become messages for Claude."""
    func = _FUNCTIONS.get(name)
    if func is None:
        return f"Unknown tool: {name}", True
    try:
        return func(**tool_input), False
    except WeatherAPIError as e:
        return str(e), True
    except TypeError:
        return f"Invalid input for {name}: {tool_input}", True
    except (KeyError, IndexError, ValueError):
        return "The weather service returned unexpected data.", True
