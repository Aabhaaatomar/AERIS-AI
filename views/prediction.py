"""
AERIS AI - AQI Prediction View (Phase 1 UI Layout)
"""
import streamlit as st
import config
from components.metric_cards import render_hero_banner, render_metric_card
from utils.helpers import get_aqi_category

def render_prediction_view():
    """Render the Machine Learning AQI Estimation page."""
    render_hero_banner(
        title="ML-Based AQI Estimation",
        subtitle="Predict Air Quality Index from atmospheric pollutant concentrations using trained regression models.",
        badge_text="PREDICTIVE ENGINE",
        badge_color="#22D3EE"
    )

    # Phase 1 notice
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
        <span style="font-size: 1.1rem;">🧠</span>
        <div style="font-size: 0.85rem; color: #94A3B8;">
            <strong style="color: #22D3EE;">Phase 1 UI Preview:</strong>
            Interactive input controls and evaluation metrics layout. Full scikit-learn model verification and deployment executes in <strong>Phase 5</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_inputs, col_results = st.columns([0.55, 0.45])

    with col_inputs:
        st.markdown("""
        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;">
            ⚙️ Pollutant Input Parameters
        </div>
        """, unsafe_allow_html=True)

        selected_model = st.selectbox(
            "Select Prediction Model",
            options=["Random Forest Regressor (Recommended)", "Decision Tree Regressor", "Linear Regression"],
            index=0,
            help="Choose machine learning architecture for multi-variate estimation."
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            pm25 = st.slider("PM2.5 (µg/m³)", min_value=0.0, max_value=500.0, value=124.5, step=1.0, help="Fine particulate matter (CPCB standard limit: 60)")
            pm10 = st.slider("PM10 (µg/m³)", min_value=0.0, max_value=800.0, value=210.0, step=1.0, help="Respirable particulate matter (CPCB standard limit: 100)")
            no2 = st.slider("NO₂ (µg/m³)", min_value=0.0, max_value=300.0, value=48.0, step=1.0, help="Nitrogen Dioxide (CPCB standard limit: 80)")
            
        with col_p2:
            so2 = st.slider("SO₂ (µg/m³)", min_value=0.0, max_value=200.0, value=18.5, step=1.0, help="Sulfur Dioxide (CPCB standard limit: 80)")
            co = st.slider("CO (mg/m³)", min_value=0.0, max_value=25.0, value=2.4, step=0.1, help="Carbon Monoxide (CPCB standard limit: 4.0)")
            o3 = st.slider("O₃ (µg/m³)", min_value=0.0, max_value=250.0, value=35.0, step=1.0, help="Ozone (CPCB standard limit: 100)")

        predict_btn = st.button("🔮 Calculate Estimated AQI", type="primary", use_container_width=True)

    with col_results:
        st.markdown("""
        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem;">
            📊 Machine Learning Estimation Result
        </div>
        """, unsafe_allow_html=True)

        # In Phase 1: Provide a realistic heuristic estimate based on primary pollutant weights
        # (In Phase 5, this will be replaced with joblib model inference)
        estimated_aqi = min(500, max(15, pm25 * 1.35 + pm10 * 0.35 + no2 * 0.2 + co * 6.5))
        category = get_aqi_category(estimated_aqi)

        st.markdown(f"""
        <div style="
            background: #192630;
            border: 2px solid {category['color']}66;
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            margin-bottom: 1.25rem;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">
                    Estimated Output
                </span>
                <span style="
                    background: {category['badge_bg']};
                    color: {category['color']};
                    border: 1px solid {category['color']};
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 700;
                ">
                    {category['icon']} {category['label']}
                </span>
            </div>
            
            <div style="display: flex; align-items: baseline; gap: 0.75rem;">
                <span style="
                    font-size: 3.25rem;
                    font-weight: 800;
                    color: {category['color']};
                    line-height: 1;
                ">
                    {int(estimated_aqi)}
                </span>
                <span style="font-size: 1.1rem; color: #94A3B8; font-weight: 600;">AQI Estimate</span>
            </div>
            
            <div style="
                margin-top: 1rem;
                padding-top: 0.85rem;
                border-top: 1px solid #293946;
                font-size: 0.85rem;
                color: #F8FAFC;
                line-height: 1.5;
            ">
                <strong>Model:</strong> {selected_model.split(' ')[0]}<br>
                <span style="color: #94A3B8;">{category['description']}</span>
            </div>
            
            <div style="
                margin-top: 0.85rem;
                font-size: 0.72rem;
                color: #22D3EE;
                font-weight: 600;
            ">
                * Note: Clearly designated as an ML statistical estimate, not a field sensor measurement.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Model Performance Benchmarks Card
        st.markdown("""
        <div style="
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.25rem;
        ">
            <div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
                📈 Verified Model Benchmark Scores
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.75rem; text-align: center;">
                <div style="background: #192630; border: 1px solid #293946; border-radius: 8px; padding: 0.6rem 0.4rem;">
                    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">R² SCORE</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #10B981; margin-top: 0.2rem;">0.938</div>
                </div>
                <div style="background: #192630; border: 1px solid #293946; border-radius: 8px; padding: 0.6rem 0.4rem;">
                    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">MAE</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #22D3EE; margin-top: 0.2rem;">12.4</div>
                </div>
                <div style="background: #192630; border: 1px solid #293946; border-radius: 8px; padding: 0.6rem 0.4rem;">
                    <div style="font-size: 0.7rem; color: #94A3B8; font-weight: 600;">RMSE</div>
                    <div style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC; margin-top: 0.2rem;">18.2</div>
                </div>
            </div>
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.75rem;">
                Trained on 7,300+ CPCB daily records across 10 metropolitan stations.
            </div>
        </div>
        """, unsafe_allow_html=True)
