"""Chart generation utilities using Plotly."""

import plotly.graph_objects as go
from typing import Dict, List


def get_weather_icon(condition: str) -> str:
    """Map weather conditions to emoji icons."""
    condition_lower = condition.lower()
    
    icon_map = {
        # Clear/Sunny
        "clear": "☀️",
        "sunny": "☀️",
        
        # Clouds
        "clouds": "☁️",
        "cloudy": "☁️",
        "overcast": "☁️",
        "partly cloudy": "⛅",
        "few clouds": "🌤️",
        "scattered clouds": "⛅",
        "broken clouds": "☁️",
        
        # Rain
        "rain": "🌧️",
        "drizzle": "🌦️",
        "light rain": "🌦️",
        "moderate rain": "🌧️",
        "heavy rain": "🌧️",
        "shower": "🌧️",
        
        # Thunderstorm
        "thunderstorm": "⛈️",
        "storm": "⛈️",
        
        # Snow
        "snow": "❄️",
        "light snow": "🌨️",
        "heavy snow": "❄️",
        
        # Other
        "mist": "🌫️",
        "fog": "🌫️",
        "haze": "🌫️",
        "dust": "🌫️",
        "smoke": "🌫️",
        "tornado": "🌪️",
    }
    
    # Check for matches
    for key, icon in icon_map.items():
        if key in condition_lower:
            return icon
    
    # Default
    return "🌤️"


def create_temperature_chart(forecast_data: List[Dict], temp_unit: str = "C") -> go.Figure:
    """Create an interactive temperature forecast chart."""
    dates = [day["date"] for day in forecast_data]
    highs = [day["temp_high"] for day in forecast_data]
    lows = [day["temp_low"] for day in forecast_data]
    
    # Convert to Fahrenheit if needed
    if temp_unit == "F":
        highs = [c * 9/5 + 32 for c in highs]
        lows = [c * 9/5 + 32 for c in lows]
    
    fig = go.Figure()
    
    # Add high temperature line
    fig.add_trace(go.Scatter(
        x=dates,
        y=highs,
        mode='lines+markers',
        name='High',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>High: %{y:.1f}°' + temp_unit + '<extra></extra>'
    ))
    
    # Add low temperature line
    fig.add_trace(go.Scatter(
        x=dates,
        y=lows,
        mode='lines+markers',
        name='Low',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=10),
        hovertemplate='<b>%{x}</b><br>Low: %{y:.1f}°' + temp_unit + '<extra></extra>'
    ))
    
    # Add shaded area between high and low
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=highs + lows[::-1],
        fill='toself',
        fillcolor='rgba(78, 205, 196, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'📊 5-Day Temperature Forecast',
            font=dict(size=20, color='#2C3E50')
        ),
        xaxis=dict(
            title='',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title=f'Temperature (°{temp_unit})',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial, sans-serif', size=12),
        margin=dict(l=50, r=50, t=80, b=50),
        height=400
    )
    
    return fig


def create_conditions_chart(forecast_data: List[Dict]) -> go.Figure:
    """Create a chart showing weather conditions over time."""
    dates = [day["date"] for day in forecast_data]
    conditions = [day["condition"] for day in forecast_data]
    humidity = [day["humidity"] for day in forecast_data]
    wind = [day["wind_speed"] for day in forecast_data]
    
    # Create subplots
    fig = go.Figure()
    
    # Add humidity bars
    fig.add_trace(go.Bar(
        x=dates,
        y=humidity,
        name='Humidity %',
        marker=dict(color='#95E1D3'),
        hovertemplate='<b>%{x}</b><br>Humidity: %{y}%<extra></extra>'
    ))
    
    # Add wind speed line
    fig.add_trace(go.Scatter(
        x=dates,
        y=wind,
        name='Wind (m/s)',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='#F38181', width=2),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Wind: %{y:.1f} m/s<extra></extra>'
    ))
    
    # Update layout with dual y-axis
    fig.update_layout(
        title=dict(
            text='💨 Humidity & Wind Forecast',
            font=dict(size=20, color='#2C3E50')
        ),
        xaxis=dict(title=''),
        yaxis=dict(
            title='Humidity (%)',
            side='left',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis2=dict(
            title='Wind Speed (m/s)',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial, sans-serif', size=12),
        margin=dict(l=50, r=50, t=80, b=50),
        height=350,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9