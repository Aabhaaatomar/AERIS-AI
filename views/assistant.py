"""
AERIS AI - Assistant View
Default landing page hosting the conversational AI assistant
"""
import streamlit as st
from components.chat_interface import render_chat_interface

def render_assistant_view():
    """Render the AI Assistant view."""
    render_chat_interface()
