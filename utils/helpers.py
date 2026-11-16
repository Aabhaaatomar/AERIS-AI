"""
AERIS AI - Utility & Helper Functions
"""
import os
import streamlit as st
from pathlib import Path
import config

def load_env_file():
    """Load key-value pairs from .env file into os.environ if present."""
    env_file = config.BASE_DIR / ".env"
    if env_file.exists():
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and k not in os.environ:
                        os.environ[k] = v
        except Exception:
            pass

def get_active_api_key(provider: str = "gemini") -> str:
    """Retrieve the API key from session state, Streamlit secrets, or environment."""
    # 1. UI session state input
    if "api_key" in st.session_state and st.session_state.api_key:
        return st.session_state.api_key.strip()
    
    # 2. Streamlit secrets
    try:
        if provider == "gemini":
            if "GEMINI_API_KEY" in st.secrets:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
            elif "GOOGLE_API_KEY" in st.secrets:
                return str(st.secrets["GOOGLE_API_KEY"]).strip()
        elif provider == "openai":
            if "OPENAI_API_KEY" in st.secrets:
                return str(st.secrets["OPENAI_API_KEY"]).strip()
    except Exception:
        pass

    # 3. Environment variables
    if provider == "gemini":
        return (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()
    elif provider == "openai":
        return (os.environ.get("OPENAI_API_KEY") or "").strip()
    return ""

def apply_custom_css():
    """Inject the dark theme SaaS CSS styling into Streamlit."""
    css_path = config.ASSETS_DIR / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background-color: #0B0F14; color: #F8FAFC; }
        </style>
        """, unsafe_allow_html=True)

def get_aqi_category(aqi_value):
    """
    Determine CPCB AQI Category, color, and description from numerical AQI.
    """
    try:
        val = float(aqi_value)
    except (ValueError, TypeError):
        return {
            "label": "Unknown",
            "color": "#94A3B8",
            "badge_bg": "rgba(148, 163, 184, 0.15)",
            "description": "Invalid or missing AQI measurement.",
            "icon": "❓"
        }

    if val <= 50:
        return config.AQI_CATEGORIES["Good"]
    elif val <= 100:
        return config.AQI_CATEGORIES["Satisfactory"]
    elif val <= 200:
        return config.AQI_CATEGORIES["Moderate"]
    elif val <= 300:
        return config.AQI_CATEGORIES["Poor"]
    elif val <= 400:
        return config.AQI_CATEGORIES["Very Poor"]
    else:
        return config.AQI_CATEGORIES["Severe"]

def init_session_state():
    """Initialize necessary Streamlit session state variables."""
    load_env_file()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "assistant"
        
    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = None
        
    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = os.environ.get("LLM_PROVIDER", "gemini")
        
    if "llm_model" not in st.session_state:
        st.session_state.llm_model = os.environ.get("LLM_MODEL", "gemini-1.5-flash")

    # API key check
    active_key = get_active_api_key(st.session_state.llm_provider)
    if "api_key" not in st.session_state:
        st.session_state.api_key = active_key
        
    if "demo_mode" not in st.session_state:
        # If API key is available, start with live LLM; otherwise demo mode
        st.session_state.demo_mode = not bool(active_key)
