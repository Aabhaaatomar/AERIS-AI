"""
AERIS AI - Chat Interface Component (Polished UI & Responsive Bubbles)
Uses native Streamlit chat components for guaranteed Markdown formatting and zero raw HTML leaks.
"""
import streamlit as st
import time
import textwrap
import config
from utils.helpers import get_active_api_key

def get_demo_response(user_query: str) -> str:
    """
    Generate realistic, markdown-formatted conversational responses for offline preview.
    Uses ground-truth application services and real atmospheric domain knowledge.
    """
    from services.chatbot_service import ChatbotService
    svc = ChatbotService()
    return svc.generate_conversational_response(user_query)

def render_chat_interface():
    """Render the main conversational interface connected to ChatbotService."""
    from services.chatbot_service import ChatbotService
    
    # Active engine status
    provider = st.session_state.get("llm_provider", "gemini")
    model = st.session_state.get("llm_model", "gemini-2.0-flash")
    api_key = get_active_api_key(provider)
    is_demo = st.session_state.get("demo_mode", False) or not bool(api_key)
    
    # Header area with clear conversation button
    if len(st.session_state.messages) > 0:
        col_hdr, col_btn = st.columns([0.80, 0.20])
        with col_hdr:
            header_html = textwrap.dedent("""
            <div style="margin-bottom: 0.25rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">💬</span>
                    <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">
                        AERIS AI Conversational Assistant
                    </h2>
                </div>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #94A3B8;">
                    Real-time reasoning, multi-service atmospheric queries, and health recommendations.
                </p>
            </div>
            """).strip()
            st.html(header_html)
        with col_btn:
            st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Chat", use_container_width=True, type="secondary"):
                st.session_state.messages = []
                st.session_state.quick_prompt = None
                st.rerun()
    else:
        header_html = textwrap.dedent("""
        <div style="margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">💬</span>
                <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">
                    AERIS AI Conversational Assistant
                </h2>
            </div>
            <p style="margin: 0.2rem 0 0 0; font-size: 0.85rem; color: #94A3B8;">
                Real-time reasoning, multi-service atmospheric queries, and health recommendations.
            </p>
        </div>
        """).strip()
        st.html(header_html)

    # Informative Banner for Current Engine Status
    if is_demo and len(st.session_state.messages) == 0:
        status_banner_html = textwrap.dedent("""
        <div style="
            background: rgba(34, 211, 238, 0.08);
            border: 1px solid rgba(34, 211, 238, 0.25);
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="font-size: 1rem;">💡</span>
            <span style="font-size: 0.82rem; color: #94A3B8;">
                Running in <strong>Demo Simulator Mode</strong>. To activate live LLM generation, enter your Gemini API key in the sidebar under <strong>⚙️ AI Engine Settings</strong>.
            </span>
        </div>
        """).strip()
        st.html(status_banner_html)
    elif not is_demo and len(st.session_state.messages) == 0:
        status_banner_html = textwrap.dedent(f"""
        <div style="
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(16, 185, 129, 0.25);
            border-radius: 10px;
            padding: 0.6rem 0.9rem;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981;"></span>
            <span style="font-size: 0.82rem; color: #10B981; font-weight: 600;">
                Genuine LLM Active: Connected to {provider.title()} ({model}) with live telemetry context injection.
            </span>
        </div>
        """).strip()
        st.html(status_banner_html)

    # Welcome Card if conversation is empty
    if len(st.session_state.messages) == 0:
        welcome_html = textwrap.dedent("""
        <div class="chat-welcome-container">
            <div style="
                width: 52px;
                height: 52px;
                border-radius: 14px;
                background: linear-gradient(135deg, #10B981 0%, #22D3EE 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin: 0 auto 0.85rem auto;
                box-shadow: 0 4px 18px rgba(16, 185, 129, 0.35);
            ">
                🌱
            </div>
            <h3 style="margin: 0; font-size: 1.45rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                Welcome to AERIS AI
            </h3>
            <p style="margin: 0.45rem auto 1rem auto; max-width: 620px; font-size: 0.92rem; color: #94A3B8; line-height: 1.55;">
                Your intelligent environmental copilot. Ask me about live city air quality, pollutant risks,
                CPCB historical analytics, ML estimations, or safety guidance.
            </p>
            <div style="
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin-top: 0.5rem;
            ">
                <span style="background: #141E27; border: 1px solid #293946; color: #22D3EE; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 20px;">📡 Live Telemetry</span>
                <span style="background: #141E27; border: 1px solid #293946; color: #10B981; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 20px;">🧠 ML Prediction</span>
                <span style="background: #141E27; border: 1px solid #293946; color: #F8FAFC; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 20px;">📊 7,300+ CPCB Records</span>
                <span style="background: #141E27; border: 1px solid #293946; color: #EAB308; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.65rem; border-radius: 20px;">🛡️ Health Advisories</span>
            </div>
        </div>
        """).strip()
        st.html(welcome_html)

        # Suggested Questions (Visually Attractive & Responsive)
        st.caption("💡 SUGGESTED QUESTIONS")

        cols = st.columns(2)
        question_icons = ["🌫️", "🛡️", "⚖️", "🔬", "📉", "🧠", "🩺"]
        for i, q in enumerate(config.SUGGESTED_QUESTIONS):
            target_col = cols[i % 2]
            icon = question_icons[i % len(question_icons)]
            with target_col:
                if st.button(f"{icon}  {q}", key=f"sugg_{i}", use_container_width=True, type="secondary"):
                    st.session_state.quick_prompt = q
                    st.rerun()

    # Render Chat History using native Streamlit chat messages for bulletproof markdown parsing
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(content)
        else:
            with st.chat_message("assistant", avatar="🌬️"):
                st.markdown(content)

    # Check for prompt trigger
    incoming_prompt = None
    if st.session_state.quick_prompt:
        incoming_prompt = st.session_state.quick_prompt
        st.session_state.quick_prompt = None

    user_input = st.chat_input("Ask anything about air quality, city AQI, health precautions, or ML predictions...")
    prompt_to_process = incoming_prompt or user_input
    
    if prompt_to_process:
        # Append User Message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt_to_process
        })
        
        # Instantiate Chatbot Service
        chatbot_svc = ChatbotService(
            api_key=api_key,
            provider=provider,
            model=model
        )
        
        # Display spinner
        with st.spinner("AERIS AI is analyzing query and consulting atmospheric services..."):
            result = chatbot_svc.process_message(
                user_query=prompt_to_process,
                conversation_history=st.session_state.messages[:-1],
                force_demo=st.session_state.demo_mode
            )
            
        # Append AI Message
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["content"]
        })
        
        st.rerun()
