"""
AERIS AI - Live AQI View
Real-time environmental monitoring dashboard across Indian urban centers.
"""
import streamlit as st
import datetime
import config
from services.live_aqi_service import LiveAQIService
from services.recommendation_service import RecommendationService
from components.metric_cards import render_hero_banner, render_aqi_badge, render_metric_card, render_pollutant_card
from components.charts import create_aqi_gauge, create_pollutant_comparison_chart

# Initialize singleton service instance
@st.cache_resource
def get_live_service():
    return LiveAQIService(cache_ttl_seconds=900)

def render_live_aqi_view():
    """Render the Live AQI monitoring interface."""
    live_service = get_live_service()

    render_hero_banner(
        title="Live Air Quality Telemetry",
        subtitle="Real-time environmental monitoring across major Indian urban centers.",
        badge_text="TELEMETRY RADAR",
        badge_color="#22D3EE"
    )

    # City Search and Selection Bar
    col_sel, col_custom, col_btn = st.columns([0.45, 0.35, 0.20])
    with col_sel:
        selected_city = st.selectbox(
            "Select Indian Metropolitan Center",
            options=config.INDIAN_CITIES,
            index=0,
            help="Select an Indian city to view current atmospheric measurements."
        )
    with col_custom:
        custom_city = st.text_input(
            "Or Search Any City",
            placeholder="e.g. Noida, Gurgaon, Surat...",
            help="Enter any city name for geocoded atmospheric telemetry."
        )
    with col_btn:
        st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
        refresh_clicked = st.button("🔄 Refresh Data", use_container_width=True, type="secondary")

    # Determine target city
    target_city = custom_city.strip() if custom_city.strip() else selected_city

    # Fetch city telemetry from service
    city_info = live_service.get_city_aqi(target_city, force_refresh=refresh_clicked)
    aqi_val = city_info["aqi"]

    # Connection & Telemetry Status Notice
    if city_info["is_live"]:
        st.markdown(f"""
        <div style="
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 10px;
            padding: 0.65rem 1rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="display:inline-block; width:9px; height:9px; border-radius:50%; background:#10B981;"></span>
                <span style="font-size: 0.85rem; color: #10B981; font-weight: 700;">LIVE TELEMETRY STREAM ACTIVE</span>
                <span style="font-size: 0.8rem; color: #94A3B8;">• Source: {city_info['source']}</span>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Last Sync: <strong style="color: #F8FAFC;">{city_info['timestamp']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="
            background: rgba(34, 211, 238, 0.08);
            border: 1px solid rgba(34, 211, 238, 0.3);
            border-radius: 10px;
            padding: 0.65rem 1rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.5rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">📡</span>
                <span style="font-size: 0.85rem; color: #22D3EE; font-weight: 700;">OFFLINE REFERENCE STATION TELEMETRY</span>
                <span style="font-size: 0.8rem; color: #94A3B8;">(Live feed unreachable; displaying validated CPCB station data)</span>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Station Time: <strong style="color: #F8FAFC;">{city_info['timestamp']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Primary Environmental Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Dominant Factor", city_info["dominant_pollutant"], subtitle="Primary driver of current AQI")
    with m2:
        render_metric_card("Surface Temperature", city_info["temperature"], subtitle="Ambient temperature")
    with m3:
        render_metric_card("Relative Humidity", city_info["humidity"], subtitle="Moisture saturation")
    with m4:
        render_metric_card("Wind Velocity", city_info["wind"], subtitle="Dispersion capability")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Hero AQI Badge & Dark Gauge Section
    col_aqi, col_gauge = st.columns([0.58, 0.42])
    with col_aqi:
        render_aqi_badge(aqi_val, city_name=city_info["city"])
        
        # Responsible Health Advisory Card
        health_tips = RecommendationService.get_recommendations(aqi_val)
        st.markdown(f"""
        <div style="
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1rem 1.25rem;
        ">
            <div style="font-size: 0.8rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                <span>🛡️</span> CPCB Health Recommendation for {city_info['city']}
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; margin-bottom: 0.35rem;">
                <strong>Outdoor Activity:</strong> {health_tips['outdoor_activity']}
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; margin-bottom: 0.35rem;">
                <strong>Respirator / Mask:</strong> {health_tips['mask_guidance']}
            </div>
            <p style="margin: 0.4rem 0 0 0; font-size: 0.72rem; color: #64748B;">
                <em>{health_tips['disclaimer']}</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_gauge:
        fig_gauge = create_aqi_gauge(aqi_val, f"{city_info['city']} AQI Level")
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Measured Pollutants Breakdown
    st.markdown(f"""
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;">
        🔬 Measured Atmospheric Pollutants ({city_info['city']})
    </div>
    """, unsafe_allow_html=True)

    pollutant_keys = list(city_info["pollutants"].keys())
    col_p1, col_p2 = st.columns([0.5, 0.5])
    with col_p1:
        for p in pollutant_keys[:3]:
            p_data = city_info["pollutants"][p]
            render_pollutant_card(
                name=p,
                value=p_data["value"],
                unit=p_data["unit"],
                limit=p_data["limit"],
                full_name=p_data["full_name"]
            )
    with col_p2:
        for p in pollutant_keys[3:]:
            p_data = city_info["pollutants"][p]
            render_pollutant_card(
                name=p,
                value=p_data["value"],
                unit=p_data["unit"],
                limit=p_data["limit"],
                full_name=p_data["full_name"]
            )

    # Pollutant comparison against CPCB limits
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
    comp_fig = create_pollutant_comparison_chart(city_info["pollutants"], f"{city_info['city']} Pollutant Concentrations vs CPCB Standards")
    st.plotly_chart(comp_fig, use_container_width=True, config={'displayModeBar': False})
