"""Weather icon and the forecast chart."""

import plotly.graph_objects as go

from utils import to_unit

HIGH_COLOR = "#eb6834"
LOW_COLOR = "#2a78d6"

_ICONS = [  # checked in order; first match wins
    ("thunder", "⛈️"), ("drizzle", "🌦️"), ("rain", "🌧️"), ("snow", "❄️"),
    ("mist", "🌫️"), ("fog", "🌫️"), ("haze", "🌫️"), ("smoke", "🌫️"),
    ("few clouds", "🌤️"), ("scattered", "⛅"), ("cloud", "☁️"), ("clear", "☀️"),
]


def weather_icon(condition: str) -> str:
    condition = condition.lower()
    return next((icon for key, icon in _ICONS if key in condition), "🌤️")


def forecast_chart(forecast: dict, unit: str) -> go.Figure:
    """High/low temperature lines; each day's label shows its condition icon and chance of rain."""
    days = forecast["days"]
    dates = [d["date"] for d in days]
    details = [[d["condition"].capitalize(), d["rain_chance"]] for d in days]
    hover = "%{y:.0f}°" + unit + "<extra></extra>"

    fig = go.Figure()
    for key, label, color in (("temp_high", "High", HIGH_COLOR), ("temp_low", "Low", LOW_COLOR)):
        fig.add_scatter(
            x=dates,
            y=[to_unit(d[key], unit) for d in days],
            name=label,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=8),
            hovertemplate=f"{label}: " + hover,
        )
    fig.update_xaxes(
        tickvals=dates,
        ticktext=[f"{d}<br>{weather_icon(c)} {r}%" for d, (c, r) in zip(dates, details)],
    )
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12, x=0),
        yaxis=dict(title=f"°{unit}", showgrid=True),
        xaxis=dict(showgrid=False),
    )
    return fig
