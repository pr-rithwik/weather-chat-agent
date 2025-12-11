"""Streamlit app for the weather chat agent."""

import streamlit as st
from agent import chat
from tools import get_coordinates_from_city, get_coordinates_from_ip
from config import OPENWEATHER_API_KEY

# Debug: Check if API key is loaded (remove after fixing)
if OPENWEATHER_API_KEY:
    st.sidebar.success(f"✅ API Key loaded: {OPENWEATHER_API_KEY[:8]}...")
else:
    st.sidebar.error("❌ API Key NOT loaded")


def get_location() -> tuple[float, float, str]:
    """Get user location from either city input or IP detection."""
    location_method = st.radio(
        "How would you like to provide your location?",
        ["Auto-detect from IP", "Enter city name", "Enter coordinates"],
        horizontal=True
    )
    
    if location_method == "Enter city name":
        city = st.text_input("Enter your city:", placeholder="e.g., London, Paris, Tokyo")
        if city:
            coords = get_coordinates_from_city(city)
            if coords:
                return coords[0], coords[1], f"📍 {city}"
            else:
                st.error("City not found. Please try another name or use coordinates.")
                return None, None, None
        return None, None, None
    elif location_method == "Enter coordinates":
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude", value=51.5074, format="%.4f")
        with col2:
            lon = st.number_input("Longitude", value=-0.1278, format="%.4f")
        return lat, lon, f"📍 {lat}, {lon}"
    else:
        coords = get_coordinates_from_ip()
        if coords and coords[0] and coords[1]:
            return coords[0], coords[1], "📍 Auto-detected location"
        else:
            st.error("Could not detect location. Please use another method.")
            return None, None, None


def main():
    """Main Streamlit app."""
    st.title("🌤️ Weather Chat Agent")
    st.caption("Ask me about the weather in your location!")
    
    # Get location
    lat, lon, location_display = get_location()
    
    if lat and lon:
        st.success(location_display)
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the weather..."):
            # Display user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = chat(prompt, lat, lon)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        st.info("👆 Please provide your location to start chatting!")


if __name__ == "__main__":
    main()