"""
AERIS AI - About View
System Architecture, Standards, and Documentation
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
        st.markdown(f"""
        <div style="
            background: #192630;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
        ">
            <h3 style="margin-top: 0; color: #10B981; font-size: 1.3rem;">🌱 Product Mission</h3>
            <p style="color: #F8FAFC; line-height: 1.6; font-size: 0.95rem;">
                <strong>AERIS AI</strong> is a next-generation environmental intelligence platform engineered to transform raw atmospheric telemetry into actionable, life-protecting insights. Combining real-time CPCB telemetry feeds, machine learning prediction algorithms, and conversational AI, AERIS AI empowers individuals, researchers, and communities to <em>Understand Your Air and Breathe Smarter</em>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #192630;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.25rem;
        ">
            <h3 style="margin-top: 0; color: #22D3EE; font-size: 1.3rem;">🏗️ Modular System Architecture</h3>
            <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.5;">
                AERIS AI is architected with strict separation of concerns across dedicated micro-services:
            </p>
            <ul style="color: #F8FAFC; font-size: 0.9rem; line-height: 1.7; padding-left: 1.2rem;">
                <li><strong>Conversational Agent (Phase 2):</strong> Modular LLM controller with intelligent query routing and contextual decision-making.</li>
                <li><strong>Live AQI Service (Phase 3):</strong> Real-time atmospheric data provider integration, multi-city indexing, and resilient caching.</li>
                <li><strong>Historical Analytics Service (Phase 4):</strong> Longitudinal analysis over 7,300+ CPCB daily records across Indian metropolitan stations.</li>
                <li><strong>Predictive ML Engine (Phase 5):</strong> Trained ensemble regressors (Random Forest, Decision Tree, Linear Regression) for multi-pollutant AQI estimation.</li>
                <li><strong>Health Advisory Engine (Phase 6):</strong> Evidence-based behavioral recommendations stratified by CPCB AQI bands.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #192630;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.5rem;
        ">
            <h3 style="margin-top: 0; color: #F8FAFC; font-size: 1.2rem;">⚖️ CPCB Indian National AQI Standard</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5;">
                India's National Air Quality Index (NAQI) developed by the Central Pollution Control Board (CPCB) evaluates 8 major pollutants: PM10, PM2.5, NO₂, SO₂, CO, O₃, NH₃, and Pb. The overall AQI corresponds to the sub-index of the worst dominant pollutant.
            </p>
            <div style="margin-top: 0.75rem; font-size: 0.85rem; color: #64748B;">
                <em>Disclaimer: AERIS AI delivers environmental data and statistical estimates. It does not provide medical diagnoses or replace clinical consultation.</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_side:
        st.markdown("""
        <div style="
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1.25rem;
        ">
            <h4 style="margin-top: 0; color: #F8FAFC; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">
                🛠️ Technology Stack
            </h4>
            <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.85rem; color: #94A3B8; margin-top: 0.75rem;">
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #293946; padding-bottom: 0.35rem;">
                    <span>Frontend UI</span>
                    <strong style="color: #F8FAFC;">Streamlit 1.54</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #293946; padding-bottom: 0.35rem;">
                    <span>Visualizations</span>
                    <strong style="color: #22D3EE;">Plotly 6.6</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #293946; padding-bottom: 0.35rem;">
                    <span>ML Pipeline</span>
                    <strong style="color: #10B981;">Scikit-Learn 1.8</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #293946; padding-bottom: 0.35rem;">
                    <span>Data Engine</span>
                    <strong style="color: #F8FAFC;">Pandas & NumPy</strong>
                </div>
                <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #293946; padding-bottom: 0.35rem;">
                    <span>Model Serializer</span>
                    <strong style="color: #F8FAFC;">Joblib</strong>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span>LLM Interface</span>
                    <strong style="color: #22D3EE;">Gemini / OpenAI API</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 12px;
            padding: 1.25rem;
        ">
            <h4 style="margin-top: 0; color: #F8FAFC; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">
                🗺️ Development Roadmap
            </h4>
            <div style="display: flex; flex-direction: column; gap: 0.6rem; font-size: 0.8rem; margin-top: 0.75rem;">
                <div style="color: #10B981; font-weight: 600;">✅ Phase 1: UI & Foundation</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 2: AI Chatbot Integration</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 3: Live AQI Telemetry</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 4: Historical Dataset Analytics</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 5: Machine Learning Models</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 6: Service Orchestration</div>
                <div style="color: #10B981; font-weight: 600;">✅ Phase 7: Deployment & QA Verified</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
