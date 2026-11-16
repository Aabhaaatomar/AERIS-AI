"""
AERIS AI - About View
System Architecture, Standards, and Documentation
Native Streamlit containers and zero raw HTML parsing risk.
"""
import streamlit as st
import config
from components.metric_cards import render_hero_banner

def render_about_view():
    """Render the About AERIS AI page."""
    render_hero_banner(
        title="About AERIS AI",
        subtitle="Intelligent Air Quality Assistant • Architectural & Standards Overview",
        badge_text="SYSTEM SPECS",
        badge_color="#22D3EE"
    )

    col_main, col_side = st.columns([0.65, 0.35])

    with col_main:
        with st.container(border=True):
            st.subheader("🌱 Product Mission")
            st.markdown(
                "**AERIS AI** is a next-generation environmental intelligence platform engineered to "
                "transform raw atmospheric telemetry into actionable, life-protecting insights. "
                "Combining real-time CPCB telemetry feeds, machine learning prediction algorithms, "
                "and conversational AI, AERIS AI empowers individuals, researchers, and communities to "
                "*Understand Your Air and Breathe Smarter*."
            )

        with st.container(border=True):
            st.subheader("🏗️ Modular System Architecture")
            st.caption("AERIS AI is architected with strict separation of concerns across dedicated micro-services:")
            st.markdown("""
            - **Conversational Agent (Phase 2):** Modular LLM controller with intelligent query routing and contextual decision-making.
            - **Live AQI Service (Phase 3):** Real-time atmospheric data provider integration, multi-city indexing, and resilient caching.
            - **Historical Analytics Service (Phase 4):** Longitudinal analysis over 7,300+ CPCB daily records across Indian metropolitan stations.
            - **Predictive ML Engine (Phase 5):** Trained ensemble regressors (Random Forest, Decision Tree, Linear Regression) for multi-pollutant AQI estimation.
            - **Health Advisory Engine (Phase 6):** Evidence-based behavioral recommendations stratified by CPCB AQI bands.
            """)

        with st.container(border=True):
            st.subheader("⚖️ CPCB Indian National AQI Standard")
            st.markdown(
                "India's National Air Quality Index (NAQI) developed by the Central Pollution Control Board (CPCB) "
                "evaluates 8 major pollutants: PM10, PM2.5, NO₂, SO₂, CO, O₃, NH₃, and Pb. "
                "The overall AQI corresponds to the sub-index of the worst dominant pollutant."
            )
            st.caption("*Disclaimer: AERIS AI delivers environmental data and statistical estimates. It does not provide medical diagnoses or replace clinical consultation.*")

    with col_side:
        with st.container(border=True):
            st.caption("SYSTEM ARCHITECTURE")
            st.markdown("#### 🛠️ Technology Stack")
            tech_stack = [
                ("Frontend UI", "Streamlit 1.54"),
                ("Visualizations", "Plotly 6.6"),
                ("ML Pipeline", "Scikit-Learn 1.8"),
                ("Data Engine", "Pandas & NumPy"),
                ("Model Serializer", "Joblib"),
                ("LLM Interface", "Gemini 2.0 / OpenAI API"),
            ]
            for comp, tech in tech_stack:
                c1, c2 = st.columns([0.55, 0.45])
                with c1:
                    st.caption(comp)
                with c2:
                    st.markdown(f"**{tech}**")
                st.divider()

        with st.container(border=True):
            st.caption("ROADMAP")
            st.markdown("#### 🗺️ Development Status")
            roadmap_items = [
                "✅ Phase 1: UI & Foundation",
                "✅ Phase 2: AI Chatbot Integration",
                "✅ Phase 3: Live AQI Telemetry",
                "✅ Phase 4: Historical Dataset Analytics",
                "✅ Phase 5: Machine Learning Models",
                "✅ Phase 6: Service Orchestration",
                "✅ Phase 7: Deployment & QA Verified",
            ]
            for item in roadmap_items:
                st.markdown(f"<span style='color: #10B981; font-weight: 600; font-size: 0.88rem;'>{item}</span>", unsafe_allow_html=True)
