"""
AERIS AI - Live AQI View (Phase 1 UI Layout)
"""
import streamlit as st
import datetime
import config
from components.metric_cards import render_hero_banner, render_aqi_badge, render_metric_card, render_pollutant_card
from components.charts import create_aqi_gauge, create_pollutant_comparison_chart

# Sample demo telemetry data for Phase 1 UI showcase
DEMO_CITY_DATA = {
    "Delhi": {
        "aqi": 342,
        "temp": "21°C",
        "humidity": "68%",
        "wind": "4.2 km/h",
        "dominant": "PM2.5",
        "pollutants": {
            "PM2.5": {"value": 242.5, "limit": 60, "unit": "µg/m³", "full_name": "Fine Particulate Matter"},
            "PM10": {"value": 395.0, "limit": 100, "unit": "µg/m³", "full_name": "Respirable Particulate Matter"},
            "NO2": {"value": 78.4, "limit": 80, "unit": "µg/m³", "full_name": "Nitrogen Dioxide"},
            "SO2": {"value": 24.1, "limit": 80, "unit": "µg/m³", "full_name": "Sulfur Dioxide"},
            "CO": {"value": 3.2, "limit": 4.0, "unit": "mg/m³", "full_name": "Carbon Monoxide"},
            "O3": {"value": 46.8, "limit": 100, "unit": "µg/m³", "full_name": "Ozone"}
        }
    },
    "Mumbai": {
        "aqi": 138,
        "temp": "28°C",
        "humidity": "74%",
        "wind": "14.5 km/h",
        "dominant": "PM10",
        "pollutants": {
            "PM2.5": {"value": 52.0, "limit": 60, "unit": "µg/m³", "full_name": "Fine Particulate Matter"},
            "PM10": {"value": 142.0, "limit": 100, "unit": "µg/m³", "full_name": "Respirable Particulate Matter"},
            "NO2": {"value": 36.2, "limit": 80, "unit": "µg/m³", "full_name": "Nitrogen Dioxide"},
            "SO2": {"value": 14.5, "limit": 80, "unit": "µg/m³", "full_name": "Sulfur Dioxide"},
            "CO": {"value": 1.1, "limit": 4.0, "unit": "mg/m³", "full_name": "Carbon Monoxide"},
            "O3": {"value": 32.1, "limit": 100, "unit": "µg/m³", "full_name": "Ozone"}
        }
    },
    "Bengaluru": {
        "aqi": 64,
        "temp": "24°C",
        "humidity": "58%",
        "wind": "9.8 km/h",
        "dominant": "PM2.5",
        "pollutants": {
            "PM2.5": {"value": 32.0, "limit": 60, "unit": "µg/m³", "full_name": "Fine Particulate Matter"},
            "PM10": {"value": 68.0, "limit": 100, "unit": "µg/m³", "full_name": "Respirable Particulate Matter"},
            "NO2": {"value": 22.4, "limit": 80, "unit": "µg/m³", "full_name": "Nitrogen Dioxide"},
            "SO2": {"value": 9.1, "limit": 80, "unit": "µg/m³", "full_name": "Sulfur Dioxide"},
            "CO": {"value": 0.8, "limit": 4.0, "unit": "mg/m³", "full_name": "Carbon Monoxide"},
            "O3": {"value": 28.5, "limit": 100, "unit": "µg/m³", "full_name": "Ozone"}
        }
    }
}

def render_live_aqi_view():
    """Render the Live AQI monitoring interface."""
    render_hero_banner(
        title="Live Air Quality Telemetry",
        subtitle="Real-time environmental monitoring across major Indian urban centers.",
        badge_text="TELEMETRY RADAR",
        badge_color="#22D3EE"
    )
    
    # Notice banner for Phase 1
    st.markdown("""
    <div style="
        background: rgba(34, 211, 238, 0.08);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    ">
        <span style="font-size: 1.1rem;">📡</span>
        <div style="font-size: 0.85rem; color: #94A3B8;">
            <strong style="color: #22D3EE;">Phase 1 Layout Preview:</strong>
            Interactive live API connection (WAQI / CPCB) will activate in <strong>Phase 3</strong>. Displaying representative telemetry values for design verification.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # City Search and Selection Bar
    col_sel, col_stat = st.columns([0.65, 0.35])
    with col_sel:
        selected_city = st.selectbox(
            "Select or Search City",
            options=config.INDIAN_CITIES,
            index=0,
            help="Select an Indian city to view current atmospheric measurements."
        )
    with col_stat:
        st.markdown(f"""
        <div style="
            background: #192630;
            border: 1px solid #293946;
            border-radius: 8px;
            padding: 0.65rem 1rem;
            margin-top: 1.7rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <span style="font-size: 0.75rem; color: #94A3B8;">Last Telemetry Sync:</span>
            <span style="font-size: 0.8rem; color: #10B981; font-weight: 600;">Just now</span>
        </div>
        """, unsafe_allow_html=True)

    # Pull city data or fallback to Delhi sample
    city_info = DEMO_CITY_DATA.get(selected_city, DEMO_CITY_DATA["Delhi"])
    
    # Primary Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Dominant Factor", city_info["dominant"], subtitle="Primary contributor to AQI")
    with m2:
        render_metric_card("Temperature", city_info["temp"], subtitle="Ambient surface temp")
    with m3:
        render_metric_card("Relative Humidity", city_info["humidity"], subtitle="Atmospheric moisture")
    with m4:
        render_metric_card("Wind Velocity", city_info["wind"], subtitle="Dispersion capability")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # AQI Hero Card & Gauge Section
    col_aqi, col_gauge = st.columns([0.58, 0.42])
    with col_aqi:
        render_aqi_badge(city_info["aqi"], city_name=selected_city)
        
        # Health Alert Box
        st.markdown(f"""
        <div style="
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1rem 1.25rem;
        ">
            <div style="font-size: 0.8rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                <span>🛡️</span> Exposure Recommendation for {selected_city}
            </div>
            <p style="margin: 0; font-size: 0.85rem; color: #94A3B8; line-height: 1.45;">
                {"Avoid strenuous outdoor exercise and wear an N95 mask outdoors." if city_info["aqi"] > 200 else "Air quality is acceptable. Sensitive individuals should monitor symptoms."}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_gauge:
        fig_gauge = create_aqi_gauge(city_info["aqi"], f"{selected_city} AQI Level")
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Pollutant Breakdown Section
    st.markdown("""
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;">
        🔬 Measured Pollutant Breakdown
    </div>
    """, unsafe_allow_html=True)

    col_cards, col_chart = st.columns([0.5, 0.5])
    with col_cards:
        for p_name, p_data in list(city_info["pollutants"].items())[:3]:
            render_pollutant_card(
                name=p_name,
                value=p_data["value"],
                unit=p_data["unit"],
                limit=p_data["limit"],
                full_name=p_data["full_name"]
            )
    with col_chart:
        for p_name, p_data in list(city_info["pollutants"].items())[3:]:
            render_pollutant_card(
                name=p_name,
                value=p_data["value"],
                unit=p_data["unit"],
                limit=p_data["limit"],
                full_name=p_data["full_name"]
            )

    # Pollutant comparison against CPCB limits
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
    comp_fig = create_pollutant_comparison_chart(city_info["pollutants"], f"{selected_city} Concentrations vs CPCB Standards")
    st.plotly_chart(comp_fig, use_container_width=True, config={'displayModeBar': False})
