"""Streamlit app for the weather chat agent."""

import streamlit as st
from agent import chat
from tools import get_coordinates_from_city
from utils import get_session_stats, update_session_stats, format_cost


def main():
    """Main Streamlit app."""
    st.title("🌤️ Weather Chat Agent")
    st.caption("Ask me about the weather in your location!")
    
    # Sidebar with statistics
    with st.sidebar:
        st.header("📊 Session Stats")
        stats = get_session_stats()
        st.metric("Messages", stats['messages'])
        st.metric("Estimated Cost", format_cost(stats['total_cost']))
        st.caption(f"Tokens: {stats['input_tokens']:,} in / {stats['output_tokens']:,} out")
        
        if stats['messages'] > 0:
            st.divider()
            if st.button("🔄 Reset Session"):
                for key in ['messages', 'total_input_tokens', 'total_output_tokens', 'message_count']:
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
    
    # Simple city input with validation
    city = st.text_input(
        "📍 Enter your city:",
        placeholder="e.g., London, Paris, Tokyo, Vijayawada",
        help="Type your city name to get started",
        max_chars=50
    )
    
    if city:
        # Validate input
        city = city.strip()
        if len(city) < 2:
            st.warning("⚠️ Please enter at least 2 characters")
            return
        
        if not city.replace(" ", "").replace("-", "").isalpha():
            st.warning("⚠️ City name should only contain letters")
            return
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
                            
                            # Track costs
                            update_session_stats(prompt, response)
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