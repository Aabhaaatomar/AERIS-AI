"""
AERIS AI - Historical Analysis View (Phase 1 UI Layout)
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config
from components.metric_cards import render_hero_banner, render_metric_card
from components.charts import create_trend_line_chart, apply_dark_theme

@st.cache_data
def load_historical_dataset():
    """Load the historical CPCB dataset."""
    data_path = config.DATA_DIR / "city_day_cpcb.csv"
    if data_path.exists():
        df = pd.read_csv(data_path)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    return None

def render_historical_analysis_view():
    """Render the Historical Analysis page."""
    render_hero_banner(
        title="Historical Atmospheric Analytics",
        subtitle="Empirical longitudinal studies and seasonal trends across Indian metropolitan hubs.",
        badge_text="CPCB ARCHIVE",
        badge_color="#10B981"
    )

    df = load_historical_dataset()

    if df is None:
        st.warning("Historical dataset not found at expected path. Please verify `data/city_day_cpcb.csv`.")
        return

    # Filter Controls
    col_city, col_year, col_pollutant = st.columns([0.4, 0.3, 0.3])
    
    cities = sorted(df["City"].unique())
    with col_city:
        selected_city = st.selectbox("Select Target City", options=cities, index=0)
        
    city_df = df[df["City"] == selected_city].copy().sort_values("Date")
    years = ["All Years"] + sorted(list(city_df["Date"].dt.year.unique()))
    
    with col_year:
        selected_year = st.selectbox("Filter Year", options=years, index=0)
        
    pollutant_options = ["AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    with col_pollutant:
        selected_pollutant = st.selectbox("Primary Parameter", options=pollutant_options, index=0)

    # Apply year filter
    if selected_year != "All Years":
        city_df = city_df[city_df["Date"].dt.year == int(selected_year)]

    # Historical Summary KPI Cards
    avg_val = city_df[selected_pollutant].mean()
    max_val = city_df[selected_pollutant].max()
    min_val = city_df[selected_pollutant].min()
    
    # Calculate % of satisfactory days (AQI <= 100)
    good_days_pct = (city_df["AQI"] <= 100).mean() * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        render_metric_card("Average Recorded", f"{avg_val:.1f}", unit="µg/m³" if selected_pollutant != "AQI" and selected_pollutant != "CO" else "", subtitle=f"Mean {selected_pollutant} level")
    with kpi2:
        render_metric_card("Peak Recorded", f"{max_val:.1f}", unit="", subtitle="Maximum recorded spike", border_color="rgba(239, 68, 68, 0.4)")
    with kpi3:
        render_metric_card("Lowest Recorded", f"{min_val:.1f}", unit="", subtitle="Cleanest recorded day", border_color="rgba(16, 185, 129, 0.4)")
    with kpi4:
        render_metric_card("Clean Air Index", f"{good_days_pct:.1f}%", subtitle="Days with AQI ≤ 100")

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # Longitudinal Trend Chart
    st.markdown(f"""
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;">
        📈 {selected_city}: {selected_pollutant} Longitudinal Trajectory
    </div>
    """, unsafe_allow_html=True)
    
    trend_fig = create_trend_line_chart(city_df, "Date", selected_pollutant, f"{selected_city} {selected_pollutant} Time Series ({city_df['Date'].min().strftime('%b %Y')} - {city_df['Date'].max().strftime('%b %Y')})")
    st.plotly_chart(trend_fig, use_container_width=True)

    # Monthly Seasonality & Bucket Distribution
    col_month, col_buckets = st.columns([0.55, 0.45])
    
    with col_month:
        st.markdown(f"""
        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;">
            📅 Monthly Average Pattern
        </div>
        """, unsafe_allow_html=True)
        city_df["Month"] = city_df["Date"].dt.strftime("%b")
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly_avg = city_df.groupby("Month")[selected_pollutant].mean().reindex(month_order).dropna().reset_index()
        
        fig_bar = px.bar(
            monthly_avg,
            x="Month",
            y=selected_pollutant,
            color=selected_pollutant,
            color_continuous_scale=["#10B981", "#EAB308", "#EF4444", "#991B1B"]
        )
        apply_dark_theme(fig_bar, f"Mean Monthly {selected_pollutant} Distribution")
        fig_bar.update_layout(height=320, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_buckets:
        st.markdown("""
        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.5rem;">
            🏷️ AQI Category Breakdown
        </div>
        """, unsafe_allow_html=True)
        bucket_counts = city_df["AQI_Bucket"].value_counts().reset_index()
        bucket_counts.columns = ["Category", "Count"]
        
        # Color mapping for buckets
        color_map = {
            "Good": "#10B981",
            "Satisfactory": "#84CC16",
            "Moderate": "#EAB308",
            "Poor": "#F97316",
            "Very Poor": "#EF4444",
            "Severe": "#991B1B"
        }
        
        fig_pie = px.pie(
            bucket_counts,
            names="Category",
            values="Count",
            color="Category",
            color_discrete_map=color_map,
            hole=0.45
        )
        apply_dark_theme(fig_pie, "Distribution of Recorded Days")
        fig_pie.update_layout(height=320)
        st.plotly_chart(fig_pie, use_container_width=True)
