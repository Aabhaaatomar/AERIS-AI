"""
AERIS AI - Metric Cards and Visual Badge Components
"""
import streamlit as st
import config
from utils.helpers import get_aqi_category

def render_hero_banner(title: str, subtitle: str, badge_text: str = "AERIS AI", badge_color: str = "#10B981"):
    """Render a premium header banner with consistent branding."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(20, 30, 39, 0.9) 0%, rgba(25, 38, 48, 0.7) 100%);
        border: 1px solid #293946;
        border-radius: 14px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;">
            <div>
                <div style="
                    display: inline-flex;
                    align-items: center;
                    gap: 0.4rem;
                    padding: 0.2rem 0.65rem;
                    border-radius: 9999px;
                    font-size: 0.75rem;
                    font-weight: 700;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                    background: rgba(16, 185, 129, 0.15);
                    color: {badge_color};
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    margin-bottom: 0.5rem;
                ">
                    <span>⚡</span> {badge_text}
                </div>
                <h2 style="margin: 0; font-size: 1.75rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                    {title}
                </h2>
                <p style="margin: 0.35rem 0 0 0; font-size: 0.95rem; color: #94A3B8;">
                    {subtitle}
                </p>
            </div>
            <div style="
                background: #141E27;
                border: 1px solid #293946;
                padding: 0.6rem 1rem;
                border-radius: 10px;
                text-align: right;
            ">
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">System Status</div>
                <div style="font-size: 0.85rem; color: #10B981; font-weight: 700; display: flex; align-items: center; gap: 0.4rem; justify-content: flex-end;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></span>
                    Online & Ready
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_aqi_badge(aqi_value: float, city_name: str = ""):
    """Render a prominent AQI Category Card."""
    cat = get_aqi_category(aqi_value)
    
    st.markdown(f"""
    <div style="
        background-color: #192630;
        border: 1px solid {cat['color']}66;
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.5);
        margin-bottom: 1rem;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span style="
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    color: #94A3B8;
                    font-weight: 700;
                ">
                    {f"Air Quality Index • {city_name}" if city_name else "Air Quality Index"}
                </span>
                <div style="display: flex; align-items: baseline; gap: 0.75rem; margin-top: 0.25rem;">
                    <span style="
                        font-size: 3rem;
                        font-weight: 800;
                        color: {cat['color']};
                        line-height: 1;
                        font-family: 'Plus Jakarta Sans', sans-serif;
                    ">{int(aqi_value) if aqi_value is not None else "--"}</span>
                    <span style="font-size: 1rem; color: #94A3B8; font-weight: 500;">AQI (CPCB)</span>
                </div>
            </div>
            <div style="
                background: {cat['badge_bg']};
                border: 1px solid {cat['color']};
                padding: 0.4rem 0.9rem;
                border-radius: 20px;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 1.1rem;">{cat['icon']}</span>
                <span style="color: {cat['color']}; font-weight: 700; font-size: 0.9rem;">{cat['label']}</span>
            </div>
        </div>
        <div style="
            margin-top: 0.85rem;
            padding-top: 0.75rem;
            border-top: 1px solid #293946;
            color: #94A3B8;
            font-size: 0.85rem;
            line-height: 1.4;
        ">
            {cat['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, unit: str = "", subtitle: str = "", border_color: str = "#293946"):
    """Render a standalone, high-contrast metric card."""
    st.markdown(f"""
    <div style="
        background-color: #192630;
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        height: 100%;
    ">
        <div style="
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94A3B8;
            margin-bottom: 0.35rem;
        ">
            {label}
        </div>
        <div style="display: flex; align-items: baseline; gap: 0.35rem;">
            <span style="
                font-size: 1.85rem;
                font-weight: 700;
                color: #F8FAFC;
                line-height: 1.2;
            ">
                {value}
            </span>
            {f'<span style="font-size: 0.85rem; color: #94A3B8; font-weight: 500;">{unit}</span>' if unit else ''}
        </div>
        {f'<div style="font-size: 0.75rem; color: #64748B; margin-top: 0.35rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def render_pollutant_card(name: str, value: float, unit: str, limit: float, full_name: str = ""):
    """Render a pollutant breakdown card with comparison to acceptable CPCB limits."""
    ratio = (value / limit) if limit > 0 else 0
    
    if ratio <= 1.0:
        status_color = "#10B981"
        status_text = "Within Limit"
        pct_bar = min(100, int(ratio * 100))
    elif ratio <= 2.0:
        status_color = "#EAB308"
        status_text = "Elevated"
        pct_bar = min(100, int(ratio * 50))
    else:
        status_color = "#EF4444"
        status_text = "Hazardous"
        pct_bar = 100

    st.markdown(f"""
    <div style="
        background-color: #192630;
        border: 1px solid #293946;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div>
                <span style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">{name}</span>
                {f'<span style="font-size: 0.75rem; color: #94A3B8; margin-left: 0.4rem;">({full_name})</span>' if full_name else ''}
            </div>
            <span style="
                background: {status_color}22;
                color: {status_color};
                border: 1px solid {status_color}44;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 0.15rem 0.5rem;
                border-radius: 9999px;
            ">{status_text}</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 0.4rem;">
            <span style="font-size: 1.5rem; font-weight: 700; color: #F8FAFC;">{value:.1f}</span>
            <span style="font-size: 0.8rem; color: #94A3B8;">{unit}</span>
            <span style="font-size: 0.75rem; color: #64748B; margin-left: auto;">Limit: {limit} {unit}</span>
        </div>
        <div style="
            width: 100%;
            height: 6px;
            background: #141E27;
            border-radius: 3px;
            margin-top: 0.65rem;
            overflow: hidden;
        ">
            <div style="
                width: {pct_bar}%;
                height: 100%;
                background: {status_color};
                border-radius: 3px;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
