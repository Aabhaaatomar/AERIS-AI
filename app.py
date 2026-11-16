"""
=============================================================================
AERIS AI - Intelligent Air Quality Assistant
Main Application Entry Point
=============================================================================
"""
import streamlit as st
import sys
from pathlib import Path

# Add current directory to Python path for seamless imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import config
from utils.helpers import apply_custom_css, init_session_state
from components.sidebar import render_sidebar
from views.assistant import render_assistant_view
from views.live_aqi import render_live_aqi_view
from views.historical_analysis import render_historical_analysis_view
from views.prediction import render_prediction_view
from views.city_comparison import render_city_comparison_view
from views.about import render_about_view

def main():
    # 1. Page Configuration (must be first Streamlit call)
    st.set_page_config(
        page_title=f"{config.APP_NAME} - {config.APP_TAGLINE}",
        page_icon="🌬️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. State & Styling Setup
    init_session_state()
    apply_custom_css()

    # 3. Sidebar Navigation
    render_sidebar()

    # 4. View Routing (Chatbot Assistant is default)
    current_page = st.session_state.get("current_page", "assistant")

    if current_page == "assistant":
        render_assistant_view()
    elif current_page == "live_aqi":
        render_live_aqi_view()
    elif current_page == "historical":
        render_historical_analysis_view()
    elif current_page == "prediction":
        render_prediction_view()
    elif current_page == "city_comparison":
        render_city_comparison_view()
    elif current_page == "about":
        render_about_view()
    else:
        render_assistant_view()

if __name__ == "__main__":
    main()
