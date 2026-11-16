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
        <div style="padding: 0.25rem 0 1.25rem 0; border-bottom: 1px solid #293946; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="
                    width: 42px;
                    height: 42px;
                    border-radius: 12px;
                    background: linear-gradient(135deg, #10B981 0%, #22D3EE 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.4rem;
                    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
                    flex-shrink: 0;
                ">
                    🌬️
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <h1 style="margin: 0; font-size: 1.35rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                            {config.APP_NAME}
                        </h1>
                        <span style="
                            font-size: 0.65rem;
                            background: rgba(16, 185, 129, 0.15);
                            color: #10B981;
                            border: 1px solid rgba(16, 185, 129, 0.35);
                            padding: 0.1rem 0.4rem;
                            border-radius: 4px;
                            font-weight: 700;
                        ">v1.0</span>
                    </div>
                    <span style="font-size: 0.72rem; color: #22D3EE; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                        Intelligent Air Assistant
                    </span>
                </div>
            </div>
            <p style="margin: 0.65rem 0 0 0; font-size: 0.8rem; color: #94A3B8; line-height: 1.35;">
                {config.APP_TAGLINE}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation Section
        st.markdown("""
        <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem;">
            Navigation Menu
        </div>
        """, unsafe_allow_html=True)
        
        nav_options = [f"{item['icon']}  {item['label']}" for item in config.NAV_ITEMS]
        
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
            if item["label"] in selected_label:
                st.session_state.current_page = item["id"]
                break
                
        st.markdown("<hr style='border: 0; border-top: 1px solid #293946; margin: 1.25rem 0 1rem 0;'>", unsafe_allow_html=True)

        # AI Engine Configuration Panel (Clean Collapsible Section)
        provider = st.session_state.get("llm_provider", "gemini")
        api_key = get_active_api_key(provider)
        is_live_ai = bool(api_key) and not st.session_state.get("demo_mode", False)

        with st.expander("⚙️ AI Engine Settings", expanded=not bool(api_key)):
            # Active status badge inside settings
            if is_live_ai:
                st.markdown("""
                <div style="
                    background: rgba(16, 185, 129, 0.12);
                    border: 1px solid rgba(16, 185, 129, 0.35);
                    border-radius: 8px;
                    padding: 0.5rem 0.75rem;
                    margin-bottom: 0.75rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                ">
                    <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981;"></span>
                    <span style="font-size: 0.78rem; color: #10B981; font-weight: 700;">Genuine AI Mode Active</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="
                    background: rgba(34, 211, 238, 0.12);
                    border: 1px solid rgba(34, 211, 238, 0.35);
                    border-radius: 8px;
                    padding: 0.5rem 0.75rem;
                    margin-bottom: 0.75rem;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                ">
                    <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#22D3EE;"></span>
                    <span style="font-size: 0.78rem; color: #22D3EE; font-weight: 700;">Demo Simulator Mode</span>
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
                placeholder="Paste API key here...",
                help="Key is stored securely in current session only. You can also define GEMINI_API_KEY in .env."
            )
            if input_key != st.session_state.get("api_key"):
                st.session_state.api_key = input_key.strip()
                if input_key.strip():
                    st.session_state.demo_mode = False
                st.rerun()

            demo_toggle = st.toggle(
                "Force Offline Demo Mode",
                value=st.session_state.get("demo_mode", False),
                help="Switch to built-in simulated responses without API consumption."
            )
            if demo_toggle != st.session_state.get("demo_mode"):
                st.session_state.demo_mode = demo_toggle
                st.rerun()

            st.markdown("""
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.4rem; line-height: 1.4;">
                Get a free key from <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#22D3EE; text-decoration:none;">Google AI Studio ↗</a>
            </div>
            """, unsafe_allow_html=True)

        # Quick Reference / AQI Scale Expander (Perfect Grid Alignment)
        with st.expander("📊 CPCB AQI Scale Guide", expanded=False):
            st.markdown("""
            <div style="
                display: grid;
                grid-template-columns: 18px 74px 1fr;
                align-items: center;
                row-gap: 10px;
                column-gap: 8px;
                padding: 0.35rem 0;
            ">
                <span style="color: #10B981; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">0 – 50</span>
                <div>
                    <div style="color: #10B981; font-weight: 700; font-size: 0.82rem;">Good</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Minimal health impact</div>
                </div>
                
                <span style="color: #84CC16; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">51 – 100</span>
                <div>
                    <div style="color: #84CC16; font-weight: 700; font-size: 0.82rem;">Satisfactory</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Minor breathing discomfort</div>
                </div>

                <span style="color: #EAB308; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">101 – 200</span>
                <div>
                    <div style="color: #EAB308; font-weight: 700; font-size: 0.82rem;">Moderate</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Discomfort to asthma/heart</div>
                </div>

                <span style="color: #F97316; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">201 – 300</span>
                <div>
                    <div style="color: #F97316; font-weight: 700; font-size: 0.82rem;">Poor</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Discomfort to most people</div>
                </div>

                <span style="color: #EF4444; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">301 – 400</span>
                <div>
                    <div style="color: #EF4444; font-weight: 700; font-size: 0.82rem;">Very Poor</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Respiratory illness on exposure</div>
                </div>

                <span style="color: #991B1B; font-size: 1rem; line-height: 1;">●</span>
                <span style="color: #F8FAFC; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 600;">401 – 500</span>
                <div>
                    <div style="color: #991B1B; font-weight: 700; font-size: 0.82rem;">Severe</div>
                    <div style="color: #94A3B8; font-size: 0.68rem;">Affects healthy people seriously</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Clear Chat Button (if on assistant page and has history)
        if st.session_state.get("current_page") == "assistant" and len(st.session_state.get("messages", [])) > 0:
            if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
                st.session_state.messages = []
                st.session_state.quick_prompt = None
                st.rerun()

        # System Status Footer
        status_color = "#10B981" if is_live_ai else "#22D3EE"
        status_text = f"Live AI ({st.session_state.get('llm_model', 'gemini')})" if is_live_ai else "Demo Simulator Mode"
        
        st.markdown(f"""
        <div style="
            margin-top: 1.25rem;
            padding: 0.75rem 0.85rem;
            background: #141E27;
            border: 1px solid #293946;
            border-radius: 10px;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 600;">SYSTEM ENGINE</span>
                <span style="
                    font-size: 0.65rem;
                    background: {status_color}22;
                    color: {status_color};
                    border: 1px solid {status_color}55;
                    padding: 0.1rem 0.4rem;
                    border-radius: 4px;
                    font-weight: 700;
                ">ONLINE</span>
            </div>
            <div style="font-size: 0.78rem; color: #F8FAFC; font-weight: 600; display: flex; align-items: center; gap: 0.4rem;">
                <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:{status_color}; flex-shrink: 0;"></span>
                <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{status_text}</span>
            </div>
            <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.25rem;">
                Multi-service intent orchestrator active
            </div>
        </div>
        """, unsafe_allow_html=True)
