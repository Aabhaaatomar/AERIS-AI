"""
AERIS AI - Modern Sidebar Navigation & Settings Component
"""
import streamlit as st
import config
from utils.helpers import get_active_api_key

def render_sidebar():
    """Render the sidebar with navigation, branding, and LLM configuration."""
    with st.sidebar:
        # Branding Header
        st.markdown(f"""
        <div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid #293946; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="
                    width: 40px;
                    height: 40px;
                    border-radius: 10px;
                    background: linear-gradient(135deg, #10B981 0%, #22D3EE 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.35rem;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                ">
                    🌬️
                </div>
                <div>
                    <h1 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                        {config.APP_NAME}
                    </h1>
                    <span style="font-size: 0.72rem; color: #22D3EE; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                        Intelligent Air Assistant
                    </span>
                </div>
            </div>
            <p style="margin: 0.75rem 0 0 0; font-size: 0.8rem; color: #94A3B8; line-height: 1.3;">
                {config.APP_TAGLINE}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown("""
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;">
            Navigation
        </div>
        """, unsafe_allow_html=True)
        
        nav_options = [item["label"] for item in config.NAV_ITEMS]
        
        current_id = st.session_state.get("current_page", "assistant")
        selected_index = 0
        for i, item in enumerate(config.NAV_ITEMS):
            if item["id"] == current_id:
                selected_index = i
                break
                
        selected_label = st.radio(
            "Select Page",
            options=nav_options,
            index=selected_index,
            label_visibility="collapsed"
        )
        
        for item in config.NAV_ITEMS:
            if item["label"] == selected_label:
                st.session_state.current_page = item["id"]
                break
                
        st.markdown("<hr style='border: 0; border-top: 1px solid #293946; margin: 1.25rem 0;'>", unsafe_allow_html=True)

        # AI Engine Configuration Panel (Phase 2)
        with st.expander("⚙️ LLM & Engine Settings", expanded=not bool(st.session_state.get("api_key"))):
            st.markdown("""
            <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.5rem;">
                Configure genuine LLM API connectivity or run in offline demo mode.
            </div>
            """, unsafe_allow_html=True)
            
            provider_choice = st.selectbox(
                "LLM Provider",
                options=["Google Gemini", "OpenAI / Compatible"],
                index=0 if st.session_state.get("llm_provider", "gemini") == "gemini" else 1
            )
            st.session_state.llm_provider = "gemini" if "Gemini" in provider_choice else "openai"
            
            if st.session_state.llm_provider == "gemini":
                model_choice = st.selectbox(
                    "Model",
                    options=["gemini-1.5-flash (Fast & Recommended)", "gemini-1.5-pro (High Reasoning)", "gemini-2.0-flash-exp"],
                    index=0
                )
                st.session_state.llm_model = model_choice.split(" ")[0]
            else:
                model_choice = st.selectbox(
                    "Model",
                    options=["gpt-4o-mini", "gpt-4o"],
                    index=0
                )
                st.session_state.llm_model = model_choice

            input_key = st.text_input(
                f"{provider_choice} API Key",
                value=st.session_state.get("api_key", ""),
                type="password",
                help="Key is kept in your current session only. You can also specify GEMINI_API_KEY in .env."
            )
            if input_key != st.session_state.get("api_key"):
                st.session_state.api_key = input_key.strip()
                if input_key.strip():
                    st.session_state.demo_mode = False
                st.rerun()

            demo_toggle = st.toggle(
                "Force Demo Mode",
                value=st.session_state.get("demo_mode", False),
                help="Switch to built-in simulated responses without API consumption."
            )
            if demo_toggle != st.session_state.get("demo_mode"):
                st.session_state.demo_mode = demo_toggle
                st.rerun()

            st.markdown("""
            <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.4rem;">
                Tip: Keys can also be defined in <code>.env</code> as <code>GEMINI_API_KEY</code>.
            </div>
            """, unsafe_allow_html=True)

        # Quick Reference / AQI Scale Expander
        with st.expander("📊 CPCB AQI Scale Guide", expanded=False):
            st.markdown("""
            <div style="font-size: 0.78rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#10B981; font-weight:600;">● 0 - 50</span>
                    <span style="color:#94A3B8;">Good</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#84CC16; font-weight:600;">● 51 - 100</span>
                    <span style="color:#94A3B8;">Satisfactory</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#EAB308; font-weight:600;">● 101 - 200</span>
                    <span style="color:#94A3B8;">Moderate</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#F97316; font-weight:600;">● 201 - 300</span>
                    <span style="color:#94A3B8;">Poor</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="color:#EF4444; font-weight:600;">● 301 - 400</span>
                    <span style="color:#94A3B8;">Very Poor</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#991B1B; font-weight:600;">● 401 - 500</span>
                    <span style="color:#94A3B8;">Severe</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Clear Chat Button (if on assistant page)
        if st.session_state.get("current_page") == "assistant" and len(st.session_state.get("messages", [])) > 0:
            if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
                st.session_state.messages = []
                st.session_state.quick_prompt = None
                st.rerun()

        # System Status Footer
        is_live_ai = bool(st.session_state.get("api_key")) and not st.session_state.get("demo_mode")
        status_color = "#10B981" if is_live_ai else "#22D3EE"
        status_text = f"Live AI ({st.session_state.get('llm_model', 'gemini')})" if is_live_ai else "Demo Simulator Mode"
        
        st.markdown(f"""
        <div style="
            margin-top: 1.5rem;
            padding: 0.85rem;
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 10px;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">AI ENGINE</span>
                <span style="
                    font-size: 0.68rem;
                    background: {status_color}22;
                    color: {status_color};
                    border: 1px solid {status_color}55;
                    padding: 0.1rem 0.4rem;
                    border-radius: 4px;
                    font-weight: 700;
                ">v1.0 ONLINE</span>
            </div>
            <div style="font-size: 0.78rem; color: #F8FAFC; font-weight: 600; display: flex; align-items: center; gap: 0.4rem;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:{status_color};"></span>
                {status_text}
            </div>
            <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.3rem;">
                Intent routing & multi-service context active
            </div>
        </div>
        """, unsafe_allow_html=True)
