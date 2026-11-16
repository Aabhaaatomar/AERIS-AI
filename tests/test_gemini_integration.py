"""
Unit Tests for Gemini Integration, Mode Selection, and Error Handling
"""
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from services.chatbot_service import ChatbotService
from services.llm_client import LLMClient

def test_gemini_mode_selection_and_mock():
    # 1. Unconfigured State -> Reports Offline Simulator
    bot_unconfigured = ChatbotService(api_key="")
    assert not bot_unconfigured.is_configured
    resp_unconf = bot_unconfigured.process_message("What is AQI?")
    assert resp_unconf["is_demo"] is True
    assert "OFFLINE CONVERSATIONAL SIMULATOR" in resp_unconf["content"]
    print("✓ Unconfigured mode properly flags Offline Simulator without silent failure.")

    # 2. Force Demo Mode ON -> Reports Demo Simulator
    bot_force_demo = ChatbotService(api_key="AIzaSyValidLookingKey12345678901234567890")
    assert bot_force_demo.is_configured
    resp_demo = bot_force_demo.process_message("Hello", force_demo=True)
    assert resp_demo["is_demo"] is True
    assert "DEMO MODE • OFFLINE SIMULATOR" in resp_demo["content"]
    print("✓ Force Demo Mode ON properly returns labelled Demo Mode.")

    # 3. Genuine Mode with Mocked Successful Gemini API Response
    with patch.object(LLMClient, "_call_gemini_sdk") as mock_sdk:
        mock_sdk.return_value = {
            "success": True,
            "text": "This is a genuine generative response from Gemini 2.0 Flash.",
            "model": "gemini-2.0-flash",
            "error": None,
            "error_type": None
        }
        
        bot_live = ChatbotService(api_key="AIzaSyValidLookingKey12345678901234567890", model="gemini-2.0-flash")
        resp_live = bot_live.process_message("What is PM2.5?", force_demo=False)
        assert resp_live["is_demo"] is False
        assert resp_live["model"] == "gemini-2.0-flash"
        assert "GENUINE AI RESPONSE" in resp_live["content"]
        assert "This is a genuine generative response from Gemini 2.0 Flash." in resp_live["content"]
        print("✓ Genuine Gemini response returned successfully with GENUINE AI badge.")

    # 4. Genuine Mode with Simulated API Error (e.g. Invalid Key)
    with patch.object(LLMClient, "_call_gemini_sdk") as mock_sdk_err:
        mock_sdk_err.return_value = {
            "success": False,
            "text": "",
            "model": "gemini-2.0-flash",
            "error": "Authentication Error (400): Invalid or restricted Gemini API key. Please check your key in settings.",
            "error_type": "AUTH_ERROR"
        }
        
        bot_err = ChatbotService(api_key="AIzaSyBadKey12345678901234567890", model="gemini-2.0-flash")
        resp_err = bot_err.process_message("Delhi AQI", force_demo=False)
        assert "Gemini API Error (AUTH_ERROR)" in resp_err["content"]
        assert "Invalid or restricted Gemini API key" in resp_err["content"]
        assert resp_err["error"] is not None
        print("✓ Genuine API Error properly surfaced via prominent error banner.")

    print("\n🎉 ALL GEMINI INTEGRATION & MODE SELECTION TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    test_gemini_mode_selection_and_mock()
