"""Streamlit app for the weather chat agent with Phase 2.5 features."""

import streamlit as st
from agent import chat
from tools import get_coordinates_from_city, get_weather, get_forecast
from utils import get_session_stats, update_session_stats, format_cost
from charts import get_weather_icon, create_temperature_chart, create_conditions_chart, celsius_to_fahrenheit
from recommendations import get_weather_recommendations, get_forecast_insights, format_sunrise_sunset


def initialize_session_state():
    """Initialize session state variables."""
    if 'recent_cities' not in st.session_state:
        st.session_state.recent_cities = []
    if 'temp_unit' not in st.session_state:
        st.session_state.temp_unit = "C"
    if 'current_weather_data' not in st.session_state:
        st.session_state.current_weather_data = None
    if 'current_forecast_data' not in st.session_state:
        st.session_state.current_forecast_data = None
    if 'current_city' not in st.session_state:
        st.session_state.current_city = None
    if 'current_coordinates' not in st.session_state:
        st.session_state.current_coordinates = None
    if 'user_timezone_offset' not in st.session_state:
        # Default to IST (UTC+5:30 = 19800 seconds) for India
        # User can change this in settings
        st.session_state.user_timezone_offset = 19800


def add_to_recent_cities(city: str):
    """Add city to recent cities list (max 5)."""
    if city not in st.session_state.recent_cities:
        st.session_state.recent_cities.insert(0, city)
        st.session_state.recent_cities = st.session_state.recent_cities[:5]


def display_current_weather(weather_data: dict, temp_unit: str):
    """Display current weather information with icon."""
    icon = get_weather_icon(weather_data["condition"])
    temp = weather_data["temperature"]
    feels_like = weather_data["feels_like"]
    
    # Convert temperatures if needed
    if temp_unit == "F":
        temp = celsius_to_fahrenheit(temp)
        feels_like = celsius_to_fahrenheit(feels_like)
    
    # Display in columns
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        st.markdown(f"<div style='font-size: 80px; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {temp:.1f}°{temp_unit}")
        st.caption(f"Feels like {feels_like:.1f}°{temp_unit}")
    
    with col3:
        st.markdown(f"**{weather_data['condition'].title()}**")
        st.caption(f"💧 Humidity: {weather_data['humidity']}%")
        st.caption(f"💨 Wind: {weather_data['wind_speed']} m/s")
    
    # Sunrise/Sunset
    if "sunrise" in weather_data and "sunset" in weather_data:
        location_timezone_offset = weather_data.get("timezone_offset", 0)
        user_timezone_offset = st.session_state.get("user_timezone_offset")
        
        sun_times = format_sunrise_sunset(
            weather_data["sunrise"], 
            weather_data["sunset"],
            location_timezone_offset,
            user_timezone_offset
        )
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌅 Sunrise", sun_times["sunrise"])
        with col2:
            st.metric("🌇 Sunset", sun_times["sunset"])
        with col3:
            st.metric("☀️ Daylight", sun_times["daylight_hours"])


def display_recommendations(weather_data: dict):
    """Display weather recommendations."""
    recommendations = get_weather_recommendations(weather_data)
    
    if recommendations:
        st.markdown("### 💡 Recommendations")
        for rec in recommendations[:5]:  # Show top 5
            st.info(rec)


def display_forecast_charts(forecast_data: list, temp_unit: str):
    """Display forecast charts."""
    if forecast_data:
        st.markdown("### 📊 5-Day Forecast")
        
        # Temperature chart
        temp_fig = create_temperature_chart(forecast_data, temp_unit)
        st.plotly_chart(temp_fig, use_container_width=True)
        
        # Conditions chart
        conditions_fig = create_conditions_chart(forecast_data)
        st.plotly_chart(conditions_fig, use_container_width=True)
        
        # Forecast insights
        insights = get_forecast_insights(forecast_data)
        if insights:
            st.markdown("### 🔍 Forecast Insights")
            for insight in insights:
                st.success(insight)


def main():
    """Main Streamlit app."""
    st.set_page_config(page_title="Weather Chat Agent", page_icon="🌤️", layout="wide")
    
    initialize_session_state()
    
    st.title("🌤️ Weather Chat Agent")
    st.caption("Ask me about the weather in your location!")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Temperature unit toggle
        temp_unit = st.radio(
            "Temperature Unit:",
            ["°C", "°F"],
            index=0 if st.session_state.temp_unit == "C" else 1,
            horizontal=True
        )
        st.session_state.temp_unit = "C" if temp_unit == "°C" else "F"
        
        # User timezone selector
        st.subheader("🌍 Your Timezone")
        
        timezone_options = {
            "India (IST, UTC+5:30)": 19800,
            "UK (GMT, UTC+0)": 0,
            "Central Europe (CET, UTC+1)": 3600,
            "US East (EST, UTC-5)": -18000,
            "US West (PST, UTC-8)": -28800,
            "Japan (JST, UTC+9)": 32400,
            "Australia East (AEST, UTC+10)": 36000,
        }
        
        # Find current selection
        current_offset = st.session_state.user_timezone_offset
        current_label = next(
            (label for label, offset in timezone_options.items() if offset == current_offset),
            "India (IST, UTC+5:30)"
        )
        
        selected_tz = st.selectbox(
            "Select your timezone:",
            list(timezone_options.keys()),
            index=list(timezone_options.keys()).index(current_label)
        )
        
        st.session_state.user_timezone_offset = timezone_options[selected_tz]
        st.caption("💡 Times will show in both location's and your timezone")
        
        st.divider()
        
        # Recent cities
        if st.session_state.recent_cities:
            st.subheader("📍 Recent Cities")
            selected_recent = st.selectbox(
                "Quick select:",
                [""] + st.session_state.recent_cities,
                key="recent_selector"
            )
        
        st.divider()
        
        # Session statistics
        st.header("📊 Session Stats")
        stats = get_session_stats()
        st.metric("Messages", stats['messages'])
        st.metric("Estimated Cost", format_cost(stats['total_cost']))
        st.caption(f"Tokens: {stats['input_tokens']:,} in / {stats['output_tokens']:,} out")
        
        if stats['messages'] > 0:
            st.divider()
            if st.button("🔄 Reset Session"):
                for key in ['messages', 'total_input_tokens', 'total_output_tokens', 'message_count', 
                           'current_weather_data', 'current_forecast_data', 'current_city', 'current_coordinates']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            # Export conversation
            st.divider()
            if st.button("💾 Export Chat"):
                from datetime import datetime
                conversation_text = f"Weather Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                for msg in st.session_state.messages:
                    role = "You" if msg["role"] == "user" else "Assistant"
                    conversation_text += f"{role}: {msg['content']}\n\n"
                
                st.download_button(
                    label="📄 Download as TXT",
                    data=conversation_text,
                    file_name=f"weather_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
        
        # Info section
        st.divider()
        st.caption("💡 **Try asking:**")
        st.caption("• 'What's the weather like?'")
        st.caption("• 'Should I bring an umbrella?'")
        st.caption("• 'What's the forecast for this week?'")
        st.caption("• 'Will it rain tomorrow?'")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # City input with validation
        city_input = st.text_input(
            "📍 Enter your city:",
            value=st.session_state.get("recent_selector", "") if st.session_state.get("recent_selector") else "",
            placeholder="e.g., London, Paris, Tokyo, Hyderabad",
            help="Type your city name to get started",
            max_chars=50,
            key="city_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("🔍 Get Weather Data", use_container_width=True):
            if city_input:
                city = city_input.strip()
                
                # Validate input
                if len(city) < 2:
                    st.warning("⚠️ Please enter at least 2 characters")
                elif not city.replace(" ", "").replace("-", "").isalpha():
                    st.warning("⚠️ City name should only contain letters, spaces, or hyphens")
                else:
                    # Get coordinates
                    try:
                        coords = get_coordinates_from_city(city)
                        
                        if coords:
                            lat, lon = coords
                            add_to_recent_cities(city)
                            
                            # Fetch weather and forecast data
                            with st.spinner("Fetching weather data..."):
                                try:
                                    weather_data = get_weather(lat, lon)
                                    forecast_data = get_forecast(lat, lon)
                                    
                                    # Store all data in session state
                                    st.session_state.current_weather_data = weather_data
                                    st.session_state.current_forecast_data = forecast_data["forecast"]
                                    st.session_state.current_city = city
                                    st.session_state.current_coordinates = (lat, lon)
                                    
                                    st.success(f"✅ Weather data loaded for **{city}**")
                                except Exception as e:
                                    st.error(f"❌ Error fetching weather: {str(e)}")
                        else:
                            st.error(f"❌ City '{city}' not found. Please check spelling or try: City, Country")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Display weather data if available
    if st.session_state.current_weather_data:
        st.markdown("---")
        
        # Current weather display
        display_current_weather(st.session_state.current_weather_data, st.session_state.temp_unit)
        
        # Recommendations
        st.markdown("---")
        display_recommendations(st.session_state.current_weather_data)
        
        # Forecast charts
        if st.session_state.current_forecast_data:
            st.markdown("---")
            display_forecast_charts(st.session_state.current_forecast_data, st.session_state.temp_unit)
        
        # Chat interface
        st.markdown("---")
        st.markdown("### 💬 Chat with Weather Assistant")
        
        # Use stored coordinates for chat (ensures consistency with displayed data)
        if st.session_state.current_coordinates:
            lat, lon = st.session_state.current_coordinates
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Ask about the weather..."):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Get agent response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = chat(prompt, lat, lon, history=st.session_state.messages[:-1])
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                            # Track costs
                            update_session_stats(prompt, response)
                        except Exception as e:
                            error_msg = f"Sorry, I encountered an error: {str(e)}"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        # Initial state - no city selected
        st.info("👆 Enter a city name and click 'Get Weather Data' to start!")
        
        # Show example
        with st.expander("📖 How to use"):
            st.markdown("""
            **Step 1:** Enter your city name (e.g., "London", "Hyderabad", "New York") in the input box
            
            **Step 2:** Click "Get Weather Data" to load weather information
            
            **Step 3:** View current weather, recommendations, and 5-day forecast
            
            **Step 4:** Chat with the AI assistant for weather insights
            
            **Features:**
            - 🌡️ Current weather with sunrise/sunset times
            - 📊 Interactive 5-day forecast charts
            - 💡 Smart weather recommendations
            - 💬 AI-powered weather chat
            - 🌍 Temperature in °C or °F
            - 📍 Quick access to recent cities
            """)


if __name__ == "__main__":
    main()