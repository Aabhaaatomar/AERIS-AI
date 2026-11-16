"""
AERIS AI - City Comparison View
Side-by-side comparative benchmarking of air quality metrics and health advisories.
"""
import streamlit as st
import pandas as pd
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
                <strong>Dominant Pollutant:</strong> {data_a['dominant_pollutant']}<br>
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
                <strong>Dominant Pollutant:</strong> {data_b['dominant_pollutant']}<br>
                {cat_b['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Multi-City Benchmark Bar Chart across Top Indian Metros
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;">
        📊 Major Indian Metropolitan Index Benchmark
    </div>
    """, unsafe_allow_html=True)

    bench_cities = config.INDIAN_CITIES[:8]
    bench_vals = [live_service.get_city_aqi(c)["aqi"] for c in bench_cities]
    fig_comp = create_city_comparison_bar(bench_cities, bench_vals, "Metropolitan AQI Overview")
    st.plotly_chart(fig_comp, use_container_width=True)

    # Detailed Head-to-Head Pollutant Table
    st.markdown(f"""
    <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.6rem;">
        🔬 Head-to-Head Pollutant Concentrations
    </div>
    """, unsafe_allow_html=True)

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
