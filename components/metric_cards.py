"""
AERIS AI - Metric Cards and Visual Badge Components
Engineered using native Streamlit containers and bulletproof HTML rendering.
Zero raw HTML leakage, full dark theme consistency, and responsive layouts.
"""
import streamlit as st
import textwrap
import config
from utils.helpers import get_aqi_category

def render_hero_banner(title: str, subtitle: str, badge_text: str = "AERIS AI", badge_color: str = "#10B981"):
    """Render a premium header banner with consistent branding using st.html."""
    html_content = textwrap.dedent(f"""
    <div style="
        background: linear-gradient(135deg, rgba(20, 30, 39, 0.95) 0%, rgba(25, 38, 48, 0.75) 100%);
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
    """).strip()
    st.html(html_content)

def render_aqi_badge(aqi_value: float, city_name: str = ""):
    """Render a prominent AQI Category Card using native Streamlit container and components."""
    cat = get_aqi_category(aqi_value)
    val_display = int(aqi_value) if aqi_value is not None else "--"
    header_label = f"Air Quality Index • {city_name}" if city_name else "Air Quality Index (CPCB)"

    with st.container(border=True):
        col_metric, col_badge = st.columns([0.62, 0.38])
        with col_metric:
            st.caption(header_label.upper())
            st.metric(
                label="Current AQI Level",
                value=val_display,
                delta=f"{cat['label']}",
                delta_color="normal" if (aqi_value is not None and aqi_value <= 100) else "inverse"
            )
        with col_badge:
            badge_html = (
                f"<div style='text-align: right; margin-top: 10px;'>"
                f"<span style='background-color: {cat['badge_bg']}; color: {cat['color']}; "
                f"border: 1px solid {cat['color']}; padding: 6px 14px; border-radius: 20px; "
                f"font-weight: 700; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 6px;'>"
                f"<span>{cat['icon']}</span> <span>{cat['label']}</span></span></div>"
            )
            st.html(badge_html)
        
        st.divider()
        st.markdown(f"**Health Impact:** {cat['description']}")

def render_metric_card(label: str, value: str, unit: str = "", subtitle: str = "", border_color: str = "#293946"):
    """
    Render a standalone, high-contrast metric card using native Streamlit container and metric.
    Completely eliminates any possibility of raw HTML or Markdown code fence parsing bugs.
    """
    val_str = f"{value} {unit}".strip() if unit else str(value)
    with st.container(border=True):
        st.caption(label.upper())
        st.metric(
            label="Value",
            value=val_str,
            label_visibility="collapsed"
        )
        if subtitle:
            st.caption(subtitle)

def render_pollutant_card(name: str, value: float, unit: str, limit: float, full_name: str = ""):
    """Render a pollutant breakdown card with comparison to acceptable CPCB limits."""
    ratio = (value / limit) if limit > 0 else 0
    
    if ratio <= 1.0:
        status_color = "#10B981"
        status_text = "Within Limit"
    elif ratio <= 2.0:
        status_color = "#EAB308"
        status_text = "Elevated"
    else:
        status_color = "#EF4444"
        status_text = "Hazardous"

    title_text = f"{name} ({full_name})" if full_name else name
    
    with st.container(border=True):
        col_l, col_r = st.columns([0.65, 0.35])
        with col_l:
            st.caption(title_text.upper())
            st.metric(
                label=f"Concentration ({unit})",
                value=f"{value:.1f} {unit}",
                delta=f"Limit: {limit} {unit}",
                delta_color="off"
            )
        with col_r:
            badge_html = (
                f"<div style='text-align: right; margin-top: 8px;'>"
                f"<span style='background: {status_color}22; color: {status_color}; "
                f"border: 1px solid {status_color}55; font-size: 0.72rem; font-weight: 700; "
                f"padding: 3px 9px; border-radius: 9999px; display: inline-block;'>"
                f"{status_text}</span></div>"
            )
            st.html(badge_html)
        
        # Native progress indicator
        progress_val = min(1.0, max(0.0, float(ratio / 2.5)))
        st.progress(progress_val)
