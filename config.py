"""
AERIS AI - Configuration Module
Intelligent Air Quality Assistant
"""
from pathlib import Path
import os

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# App Branding
APP_NAME = "AERIS AI"
APP_TAGLINE = "Understand Your Air. Breathe Smarter."
APP_VERSION = "1.0.0"
APP_PHASE = "Phase 1 - UI & Foundation"

# Design System - Dark AI Dashboard Palette
COLORS = {
    "background": "#0B0F14",
    "sidebar": "#101820",
    "secondary_background": "#141E27",
    "cards": "#192630",
    "primary_accent": "#10B981",    # Emerald
    "secondary_accent": "#22D3EE",  # Cyan
    "main_text": "#F8FAFC",
    "secondary_text": "#94A3B8",
    "border": "#293946",
    "surface_hover": "#223342",
}

# CPCB Indian AQI Standard Categories
AQI_CATEGORIES = {
    "Good": {
        "range": (0, 50),
        "color": "#10B981",
        "badge_bg": "rgba(16, 185, 129, 0.15)",
        "label": "Good",
        "description": "Minimal health impact. Air quality is considered satisfactory.",
        "icon": "🌱"
    },
    "Satisfactory": {
        "range": (51, 100),
        "color": "#84CC16",
        "badge_bg": "rgba(132, 204, 22, 0.15)",
        "label": "Satisfactory",
        "description": "Minor breathing discomfort to sensitive people.",
        "icon": "🍃"
    },
    "Moderate": {
        "range": (101, 200),
        "color": "#EAB308",
        "badge_bg": "rgba(234, 179, 8, 0.15)",
        "label": "Moderate",
        "description": "Breathing discomfort to people with lungs, asthma and heart diseases.",
        "icon": "⚠️"
    },
    "Poor": {
        "range": (201, 300),
        "color": "#F97316",
        "badge_bg": "rgba(249, 115, 22, 0.15)",
        "label": "Poor",
        "description": "Breathing discomfort to most people on prolonged exposure.",
        "icon": "😷"
    },
    "Very Poor": {
        "range": (301, 400),
        "color": "#EF4444",
        "badge_bg": "rgba(239, 68, 68, 0.15)",
        "label": "Very Poor",
        "description": "Respiratory illness on prolonged exposure. Significant risk.",
        "icon": "🛑"
    },
    "Severe": {
        "range": (401, 500),
        "color": "#991B1B",
        "badge_bg": "rgba(153, 27, 27, 0.25)",
        "label": "Severe",
        "description": "Affects healthy people and seriously impacts those with existing diseases.",
        "icon": "☣️"
    }
}

# Navigation Items
NAV_ITEMS = [
    {"id": "assistant", "label": "AI Assistant", "icon": "💬", "badge": "Primary"},
    {"id": "live_aqi", "label": "Live AQI", "icon": "📡", "badge": "Real-time"},
    {"id": "historical", "label": "Historical Analysis", "icon": "📈", "badge": "Insights"},
    {"id": "prediction", "label": "AQI Prediction", "icon": "🧠", "badge": "ML Model"},
    {"id": "city_comparison", "label": "City Comparison", "icon": "⚖️", "badge": "Benchmark"},
    {"id": "about", "label": "About AERIS AI", "icon": "ℹ️", "badge": "System"},
]

# Suggested Questions for Chatbot
SUGGESTED_QUESTIONS = [
    "What is the current AQI in Delhi?",
    "Is the air quality safe today?",
    "Compare Delhi and Mumbai air quality.",
    "What is PM2.5?",
    "Why is pollution increasing?",
    "Predict AQI using pollutant values.",
    "What precautions should I take today?"
]

# Supported Indian Cities for Quick Reference
INDIAN_CITIES = [
    "Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai",
    "Hyderabad", "Ahmedabad", "Pune", "Lucknow", "Patna",
    "Jaipur", "Chandigarh", "Bhopal", "Visakhapatnam", "Guwahati"
]

# Pollutant Standards (CPCB 24-hr avg acceptable limits in µg/m³, CO in mg/m³)
POLLUTANT_STANDARDS = {
    "PM2.5": {"limit": 60, "unit": "µg/m³", "name": "Fine Particulate Matter (2.5 µm)"},
    "PM10": {"limit": 100, "unit": "µg/m³", "name": "Respirable Particulate Matter (10 µm)"},
    "NO2": {"limit": 80, "unit": "µg/m³", "name": "Nitrogen Dioxide"},
    "SO2": {"limit": 80, "unit": "µg/m³", "name": "Sulfur Dioxide"},
    "CO": {"limit": 4.0, "unit": "mg/m³", "name": "Carbon Monoxide"},
    "O3": {"limit": 100, "unit": "µg/m³", "name": "Ozone (8-hour)"}
}
