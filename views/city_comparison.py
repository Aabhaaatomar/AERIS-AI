"""
AERIS AI - City Comparison View
Side-by-side comparative benchmarking of air quality metrics and health advisories.
Built using native Streamlit containers and components.
"""
import streamlit as st
import pandas as pd
import textwrap
import config
from services.live_aqi_service import LiveAQIService
from services.recommendation_service import RecommendationService
from components.metric_cards import render_hero_banner, render_metric_card
from components.charts import create_city_comparison_bar
from utils.helpers import get_aqi_category

@st.cache_resource
def get_live_service():
    return LiveAQIService()

def render_city_comparison_view():
    """Render the City Comparison interface."""
    live_service = get_live_service()

    render_hero_banner(
        title="Cross-City Atmospheric Comparison",
        subtitle="Side-by-side comparative benchmarking of air quality metrics and health advisories.",
        badge_text="COMPARATIVE RADAR",
        badge_color="#10B981"
    )

    col1, col2 = st.columns(2)
    cities = config.INDIAN_CITIES
    
    with col1:
        city_a = st.selectbox("Select Primary City", options=cities, index=0)
    with col2:
        city_b = st.selectbox("Select Secondary City", options=cities, index=1)

    data_a = live_service.get_city_aqi(city_a)
    data_b = live_service.get_city_aqi(city_b)
    
    cat_a = get_aqi_category(data_a["aqi"])
    cat_b = get_aqi_category(data_b["aqi"])

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Side-by-side comparative cards using native Streamlit containers
    card_col1, card_col2 = st.columns(2)
    
    with card_col1:
        with st.container(border=True):
            hdr_left, hdr_right = st.columns([0.62, 0.38])
            with hdr_left:
                st.caption("PRIMARY STATION")
                st.markdown(f"### {city_a}")
            with hdr_right:
                st.html(
                    f"<div style='text-align: right; margin-top: 6px;'>"
                    f"<span style='background-color: {cat_a['badge_bg']}; color: {cat_a['color']}; "
                    f"border: 1px solid {cat_a['color']}; padding: 4px 10px; border-radius: 16px; "
                    f"font-weight: 700; font-size: 0.82rem; display: inline-block;'>"
                    f"{cat_a['icon']} {cat_a['label']}</span></div>"
                )
            
            st.metric(
                label="Air Quality Index",
                value=f"{data_a['aqi']} AQI",
                delta=cat_a['label'],
                delta_color="normal" if data_a['aqi'] <= 100 else "inverse"
            )
            st.markdown(f"**Dominant Factor:** `{data_a['dominant_pollutant']}`")
            st.caption(cat_a['description'])

    with card_col2:
        with st.container(border=True):
            hdr_left, hdr_right = st.columns([0.62, 0.38])
            with hdr_left:
                st.caption("BENCHMARK STATION")
                st.markdown(f"### {city_b}")
            with hdr_right:
                st.html(
                    f"<div style='text-align: right; margin-top: 6px;'>"
                    f"<span style='background-color: {cat_b['badge_bg']}; color: {cat_b['color']}; "
                    f"border: 1px solid {cat_b['color']}; padding: 4px 10px; border-radius: 16px; "
                    f"font-weight: 700; font-size: 0.82rem; display: inline-block;'>"
                    f"{cat_b['icon']} {cat_b['label']}</span></div>"
                )
            
            st.metric(
                label="Air Quality Index",
                value=f"{data_b['aqi']} AQI",
                delta=cat_b['label'],
                delta_color="normal" if data_b['aqi'] <= 100 else "inverse"
            )
            st.markdown(f"**Dominant Factor:** `{data_b['dominant_pollutant']}`")
            st.caption(cat_b['description'])

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Multi-City Benchmark Bar Chart across Top Indian Metros
    st.subheader("📊 Major Indian Metropolitan Index Benchmark")

    bench_cities = config.INDIAN_CITIES[:8]
    bench_vals = [live_service.get_city_aqi(c)["aqi"] for c in bench_cities]
    fig_comp = create_city_comparison_bar(bench_cities, bench_vals, "Metropolitan AQI Overview")
    st.plotly_chart(fig_comp, use_container_width=True)

    # Detailed Head-to-Head Pollutant Table
    st.subheader("🔬 Head-to-Head Pollutant Concentrations")

    p_a = data_a["pollutants"]
    p_b = data_b["pollutants"]

    table_data = []
    for p_name in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]:
        val_a = p_a.get(p_name, {}).get("value", 0.0)
        val_b = p_b.get(p_name, {}).get("value", 0.0)
        unit = p_a.get(p_name, {}).get("unit", "µg/m³")
        limit = p_a.get(p_name, {}).get("limit", 0)
        cleaner = city_a if val_a < val_b else city_b
        table_data.append({
            "Pollutant": p_name,
            "CPCB Limit": f"{limit} {unit}",
            city_a: f"{val_a:.1f} {unit}",
            city_b: f"{val_b:.1f} {unit}",
            "Cleaner Station": cleaner
        })

    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True
    )
