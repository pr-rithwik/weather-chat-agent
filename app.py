"""Streamlit app for the weather chat agent."""

import streamlit as st
from agent import chat
from tools import get_coordinates_from_city


def main():
    """Main Streamlit app."""
    st.title("🌤️ Weather Chat Agent")
    st.caption("Ask me about the weather in your location!")
    
    # Simple city input
    city = st.text_input(
        "📍 Enter your city:",
        placeholder="e.g., London, Paris, Tokyo, Vijayawada",
        help="Type your city name to get started"
    )
    
    if city:
        # Get coordinates from city name
        coords = get_coordinates_from_city(city)
        
        if coords:
            lat, lon = coords
            st.success(f"✅ Location set to **{city}**")
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            st.markdown("---")
            
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
                            response = chat(prompt, lat, lon)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_msg = f"Sorry, I encountered an error: {str(e)}"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            st.error(f"❌ City '{city}' not found. Please check spelling or try another city.")
    else:
        st.info("👆 Enter your city name above to start chatting about weather!")


if __name__ == "__main__":
    main()