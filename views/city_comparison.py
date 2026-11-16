"""
AERIS AI - City Comparison View (Phase 1 UI Layout)
"""
import streamlit as st
import pandas as pd
import config
from components.metric_cards import render_hero_banner, render_metric_card
from components.charts import create_city_comparison_bar
from utils.helpers import get_aqi_category

# Sample comparative dataset for cities
CITY_SAMPLE_PROFILES = {
    "Delhi": {"aqi": 342, "pm25": 242.5, "pm10": 395.0, "no2": 78.4, "so2": 24.1, "co": 3.2, "status": "Very Poor"},
    "Mumbai": {"aqi": 138, "pm25": 52.0, "pm10": 142.0, "no2": 36.2, "so2": 14.5, "co": 1.1, "status": "Moderate"},
    "Bengaluru": {"aqi": 64, "pm25": 32.0, "pm10": 68.0, "no2": 22.4, "so2": 9.1, "co": 0.8, "status": "Satisfactory"},
    "Kolkata": {"aqi": 215, "pm25": 115.0, "pm10": 225.0, "no2": 52.0, "so2": 19.8, "co": 2.1, "status": "Poor"},
    "Hyderabad": {"aqi": 98, "pm25": 45.0, "pm10": 92.0, "no2": 28.5, "so2": 11.2, "co": 0.9, "status": "Satisfactory"},
    "Chennai": {"aqi": 82, "pm25": 38.0, "pm10": 79.0, "no2": 21.0, "so2": 10.5, "co": 0.7, "status": "Satisfactory"},
    "Ahmedabad": {"aqi": 260, "pm25": 140.0, "pm10": 280.0, "no2": 58.0, "so2": 22.0, "co": 2.5, "status": "Poor"},
    "Pune": {"aqi": 112, "pm25": 58.0, "pm10": 120.0, "no2": 31.0, "so2": 12.0, "co": 1.0, "status": "Moderate"}
}

def render_city_comparison_view():
    """Render the City Comparison interface."""
    render_hero_banner(
        title="Cross-City Atmospheric Comparison",
        subtitle="Side-by-side comparative benchmarking of air quality metrics and health advisories.",
        badge_text="COMPARATIVE RADAR",
        badge_color="#10B981"
    )

    col1, col2 = st.columns(2)
    cities = list(CITY_SAMPLE_PROFILES.keys())
    
    with col1:
        city_a = st.selectbox("Select Primary City", options=cities, index=0)
    with col2:
        city_b = st.selectbox("Select Secondary City", options=cities, index=1)

    data_a = CITY_SAMPLE_PROFILES[city_a]
    data_b = CITY_SAMPLE_PROFILES[city_b]
    
    cat_a = get_aqi_category(data_a["aqi"])
    cat_b = get_aqi_category(data_b["aqi"])

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Side-by-side comparative cards
    card_col1, card_col2 = st.columns(2)
    
    with card_col1:
        st.markdown(f"""
        <div style="
            background: #192630;
            border: 2px solid {cat_a['color']}66;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.4);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; font-size: 1.35rem; color: #F8FAFC;">{city_a}</h3>
                <span style="
                    background: {cat_a['badge_bg']};
                    color: {cat_a['color']};
                    border: 1px solid {cat_a['color']};
                    padding: 0.2rem 0.6rem;
                    border-radius: 20px;
                    font-size: 0.75rem;
                    font-weight: 700;
                ">{cat_a['icon']} {cat_a['label']}</span>
            </div>
            <div style="font-size: 2.75rem; font-weight: 800; color: {cat_a['color']}; margin-top: 0.5rem; line-height: 1;">
                {data_a['aqi']} <span style="font-size: 0.9rem; color: #94A3B8; font-weight: 500;">AQI</span>
            </div>
            <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #94A3B8;">
                {cat_a['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card_col2:
        st.markdown(f"""
        <div style="
            background: #192630;
            border: 2px solid {cat_b['color']}66;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 4px 14px rgba(0,0,0,0.4);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; font-size: 1.35rem; color: #F8FAFC;">{city_b}</h3>
                <span style="
                    background: {cat_b['badge_bg']};
                    color: {cat_b['color']};
                    border: 1px solid {cat_b['color']};
                    padding: 0.2rem 0.6rem;
                    border-radius: 20px;
                    font-size: 0.75rem;
                    font-weight: 700;
                ">{cat_b['icon']} {cat_b['label']}</span>
            </div>
            <div style="font-size: 2.75rem; font-weight: 800; color: {cat_b['color']}; margin-top: 0.5rem; line-height: 1;">
                {data_b['aqi']} <span style="font-size: 0.9rem; color: #94A3B8; font-weight: 500;">AQI</span>
            </div>
            <div style="margin-top: 0.75rem; font-size: 0.8rem; color: #94A3B8;">
                {cat_b['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Comparative Bar Chart Across All Major Metros
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;">
        📊 Metropolitan Index Benchmark
    </div>
    """, unsafe_allow_html=True)

    chart_cities = list(CITY_SAMPLE_PROFILES.keys())
    chart_vals = [CITY_SAMPLE_PROFILES[c]["aqi"] for c in chart_cities]
    fig_comp = create_city_comparison_bar(chart_cities, chart_vals, "Metropolitan AQI Overview")
    st.plotly_chart(fig_comp, use_container_width=True)

    # Detailed Head-to-Head Pollutant Table
    st.markdown(f"""
    <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.6rem;">
        🔬 Head-to-Head Pollutant Concentrations
    </div>
    """, unsafe_allow_html=True)

    table_data = [
        {"Pollutant": "PM2.5 (Fine Particulate)", "Safe Limit": "60 µg/m³", city_a: f"{data_a['pm25']} µg/m³", city_b: f"{data_b['pm25']} µg/m³", "Cleaner City": city_a if data_a['pm25'] < data_b['pm25'] else city_b},
        {"Pollutant": "PM10 (Coarse Particulate)", "Safe Limit": "100 µg/m³", city_a: f"{data_a['pm10']} µg/m³", city_b: f"{data_b['pm10']} µg/m³", "Cleaner City": city_a if data_a['pm10'] < data_b['pm10'] else city_b},
        {"Pollutant": "NO₂ (Nitrogen Dioxide)", "Safe Limit": "80 µg/m³", city_a: f"{data_a['no2']} µg/m³", city_b: f"{data_b['no2']} µg/m³", "Cleaner City": city_a if data_a['no2'] < data_b['no2'] else city_b},
        {"Pollutant": "SO₂ (Sulfur Dioxide)", "Safe Limit": "80 µg/m³", city_a: f"{data_a['so2']} µg/m³", city_b: f"{data_b['so2']} µg/m³", "Cleaner City": city_a if data_a['so2'] < data_b['so2'] else city_b},
        {"Pollutant": "CO (Carbon Monoxide)", "Safe Limit": "4.0 mg/m³", city_a: f"{data_a['co']} mg/m³", city_b: f"{data_b['co']} mg/m³", "Cleaner City": city_a if data_a['co'] < data_b['co'] else city_b},
    ]

    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True
    )
