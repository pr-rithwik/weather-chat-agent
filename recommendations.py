"""Weather recommendations and insights."""

from typing import Dict, List
from datetime import datetime


def get_weather_recommendations(weather_data: Dict) -> List[str]:
    """Generate smart recommendations based on current weather."""
    recommendations = []
    
    temp = weather_data["temperature"]
    condition = weather_data["condition"].lower()
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    feels_like = weather_data["feels_like"]
    
    # Temperature-based recommendations
    if temp > 30:
        recommendations.append("🌡️ It's very hot! Stay hydrated and seek shade")
        recommendations.append("🧴 Apply sunscreen if going outside (SPF 30+)")
    elif temp > 25:
        recommendations.append("☀️ Warm day ahead! Light clothing recommended")
    elif temp < 5:
        recommendations.append("🧥 Bundle up! It's quite cold outside")
        recommendations.append("🧤 Don't forget gloves and warm layers")
    elif temp < 10:
        recommendations.append("🧣 Wear a jacket or sweater, it's chilly")
    
    # Feels-like temperature
    if abs(feels_like - temp) > 5:
        if feels_like > temp:
            recommendations.append(f"🌡️ Feels like {feels_like:.0f}°C (warmer than actual)")
        else:
            recommendations.append(f"🌡️ Feels like {feels_like:.0f}°C (cooler than actual)")
    
    # Condition-based recommendations
    if any(word in condition for word in ["rain", "drizzle", "shower"]):
        recommendations.append("☂️ Bring an umbrella! Rain expected")
        recommendations.append("👟 Wear waterproof footwear")
    
    if "thunderstorm" in condition or "storm" in condition:
        recommendations.append("⛈️ Thunderstorm alert! Stay indoors if possible")
        recommendations.append("⚠️ Avoid open areas and tall objects")
    
    if "snow" in condition:
        recommendations.append("❄️ Snowy weather! Drive carefully")
        recommendations.append("🚗 Allow extra travel time")
    
    if any(word in condition for word in ["fog", "mist", "haze"]):
        recommendations.append("🌫️ Low visibility! Drive with caution")
        recommendations.append("🚦 Use fog lights if driving")
    
    if "clear" in condition or "sunny" in condition:
        if temp > 15 and temp < 28:
            recommendations.append("⛰️ Great day for outdoor activities!")
        recommendations.append("😎 Don't forget your sunglasses")
    
    # Humidity-based recommendations
    if humidity > 80:
        recommendations.append("💧 High humidity! May feel muggy")
    elif humidity < 30:
        recommendations.append("💧 Low humidity! Keep skin moisturized")
    
    # Wind-based recommendations
    if wind_speed > 10:
        recommendations.append("💨 Very windy! Secure loose objects")
    elif wind_speed > 7:
        recommendations.append("🍃 Windy conditions! Hold onto your hat")
    
    # Time-based recommendations
    hour = datetime.now().hour
    if 6 <= hour <= 9 and "clear" in condition:
        recommendations.append("🌅 Beautiful morning for a walk or jog!")
    elif 17 <= hour <= 20 and temp > 15 and temp < 25:
        recommendations.append("🌆 Pleasant evening weather!")
    
    # Default if no specific recommendations
    if not recommendations:
        recommendations.append("✅ Weather conditions are moderate today")
    
    return recommendations


def get_forecast_insights(forecast_data: List[Dict]) -> List[str]:
    """Generate insights from forecast data."""
    insights = []
    
    if not forecast_data:
        return insights
    
    # Temperature trend
    temps = [day["temp_avg"] for day in forecast_data]
    if len(temps) >= 3:
        if all(temps[i] < temps[i+1] for i in range(len(temps)-1)):
            insights.append("📈 Temperatures rising throughout the week")
        elif all(temps[i] > temps[i+1] for i in range(len(temps)-1)):
            insights.append("📉 Temperatures dropping throughout the week")
    
    # Temperature range
    max_temp = max(day["temp_high"] for day in forecast_data)
    min_temp = min(day["temp_low"] for day in forecast_data)
    temp_range = max_temp - min_temp
    
    if temp_range > 15:
        insights.append(f"🌡️ Large temperature variation this week ({min_temp:.0f}°C to {max_temp:.0f}°C)")
    
    # Rain forecast
    rain_days = sum(1 for day in forecast_data if "rain" in day["condition"].lower())
    if rain_days >= 3:
        insights.append(f"🌧️ Rainy week ahead ({rain_days} days with rain)")
    elif rain_days == 0:
        insights.append("☀️ No rain expected this week!")
    
    # Warmest/Coldest day
    warmest_day = max(forecast_data, key=lambda x: x["temp_high"])
    coldest_day = min(forecast_data, key=lambda x: x["temp_low"])
    
    insights.append(f"🔥 Warmest: {warmest_day['date'].split(',')[0]} ({warmest_day['temp_high']:.0f}°C)")
    insights.append(f"❄️ Coldest: {coldest_day['date'].split(',')[0]} ({coldest_day['temp_low']:.0f}°C)")
    
    # Wind insights
    windy_days = sum(1 for day in forecast_data if day["wind_speed"] > 7)
    if windy_days >= 2:
        insights.append(f"💨 {windy_days} windy days expected")
    
    return insights


def format_sunrise_sunset(
    sunrise_timestamp: int, 
    sunset_timestamp: int, 
    location_timezone_offset: int = 0,
    user_timezone_offset: int = None
) -> Dict[str, str]:
    """Format sunrise and sunset times in location's timezone and optionally user's timezone.
    
    Args:
        sunrise_timestamp: UTC timestamp for sunrise
        sunset_timestamp: UTC timestamp for sunset
        location_timezone_offset: Location's offset from UTC in seconds
        user_timezone_offset: User's timezone offset in seconds (optional)
    """
    from datetime import datetime, timezone, timedelta
    
    # Location's timezone
    location_tz = timezone(timedelta(seconds=location_timezone_offset))
    sunrise_local = datetime.fromtimestamp(sunrise_timestamp, tz=location_tz)
    sunset_local = datetime.fromtimestamp(sunset_timestamp, tz=location_tz)
    
    # Get timezone abbreviation
    location_tz_name = get_timezone_name(location_timezone_offset)
    
    # Format location times
    sunrise_str = sunrise_local.strftime("%I:%M %p")
    sunset_str = sunset_local.strftime("%I:%M %p")
    
    # Add user's timezone if different
    if user_timezone_offset is not None and user_timezone_offset != location_timezone_offset:
        user_tz = timezone(timedelta(seconds=user_timezone_offset))
        sunrise_user = datetime.fromtimestamp(sunrise_timestamp, tz=user_tz)
        sunset_user = datetime.fromtimestamp(sunset_timestamp, tz=user_tz)
        
        user_tz_name = get_timezone_name(user_timezone_offset)
        
        sunrise_str += f" {location_tz_name} ({sunrise_user.strftime('%I:%M %p')} {user_tz_name})"
        sunset_str += f" {location_tz_name} ({sunset_user.strftime('%I:%M %p')} {user_tz_name})"
    else:
        sunrise_str += f" {location_tz_name}"
        sunset_str += f" {location_tz_name}"
    
    return {
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "daylight_hours": f"{(sunset_timestamp - sunrise_timestamp) / 3600:.1f} hours"
    }


def get_timezone_name(offset_seconds: int) -> str:
    """Get a readable timezone name from offset in seconds."""
    hours = offset_seconds / 3600
    
    # Common timezone names
    tz_names = {
        19800: "IST",    # UTC+5:30 (India)
        0: "GMT",        # UTC+0 (London)
        3600: "CET",     # UTC+1 (Central Europe)
        -18000: "EST",   # UTC-5 (US East Coast)
        -28800: "PST",   # UTC-8 (US West Coast)
        32400: "JST",    # UTC+9 (Japan)
        36000: "AEST",   # UTC+10 (Australia East)
        -10800: "BRT",   # UTC-3 (Brazil)
    }
    
    if offset_seconds in tz_names:
        return tz_names[offset_seconds]
    
    # Generic format for unknown timezones
    sign = "+" if hours >= 0 else ""
    if hours % 1 == 0:
        return f"UTC{sign}{int(hours)}"
    else:
        h = int(hours)
        m = int(abs(hours % 1) * 60)
        return f"UTC{sign}{h}:{m:02d}"