"""Utility functions for the weather chat agent."""

from typing import Dict


def estimate_token_count(text: str) -> int:
    """Estimate token count (rough approximation: 1 token ≈ 4 characters)."""
    return len(text) // 4


def calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """Calculate approximate cost for Claude API call.
    
    Claude Sonnet 4 pricing (as of Dec 2024):
    - Input: $3 per 1M tokens
    - Output: $15 per 1M tokens
    """
    input_cost = (input_tokens / 1_000_000) * 3.0
    output_cost = (output_tokens / 1_000_000) * 15.0
    return input_cost + output_cost


def format_cost(cost: float) -> str:
    """Format cost in a readable way."""
    if cost < 0.01:
        return f"${cost:.4f}"
    return f"${cost:.2f}"


def get_session_stats() -> Dict[str, any]:
    """Get statistics for the current session."""
    import streamlit as st
    
    if 'total_input_tokens' not in st.session_state:
        st.session_state.total_input_tokens = 0
    if 'total_output_tokens' not in st.session_state:
        st.session_state.total_output_tokens = 0
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    
    total_cost = calculate_cost(
        st.session_state.total_input_tokens,
        st.session_state.total_output_tokens
    )
    
    return {
        'messages': st.session_state.message_count,
        'input_tokens': st.session_state.total_input_tokens,
        'output_tokens': st.session_state.total_output_tokens,
        'total_cost': total_cost
    }


def update_session_stats(input_text: str, output_text: str):
    """Update session statistics after API call."""
    import streamlit as st
    
    input_tokens = estimate_token_count(input_text)
    output_tokens = estimate_token_count(output_text)
    
    st.session_state.total_input_tokens = st.session_state.get('total_input_tokens', 0) + input_tokens
    st.session_state.total_output_tokens = st.session_state.get('total_output_tokens', 0) + output_tokens
    st.session_state.message_count = st.session_state.get('message_count', 0) + 1