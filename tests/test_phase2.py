"""
AERIS AI - Phase 2 LLM Integration & Orchestration Tests
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.llm_client import LLMClient
from services.chatbot_service import ChatbotService
import config

def test_llm_client_missing_key():
    client = LLMClient(api_key="", provider="gemini")
    res = client.generate("Test prompt")
    assert not res["success"]
    assert res["error_type"] == "MISSING_KEY"
    print("✓ LLMClient correctly flags missing API keys without crashing.")

def test_context_extraction():
    bot = ChatbotService(api_key="demo_key")
    
    # 1. City query
    ctx_city = bot.extract_context_from_services("What is the average AQI in Delhi?")
    assert "DELHI" in ctx_city
    assert "Average AQI" in ctx_city
    print("✓ Domain context extraction successfully retrieved Delhi historical records.")
    
    # 2. Prediction query
    ctx_pred = bot.extract_context_from_services("Predict AQI if PM2.5=150 and PM10=250")
    assert "ML PREDICTION ENGINE" in ctx_pred
    print("✓ Domain context extraction successfully routed to ML prediction engine.")
    
    # 3. Health query
    ctx_health = bot.extract_context_from_services("Is it safe for an asthma patient to exercise outside?")
    assert "CPCB HEALTH MATRIX" in ctx_health
    print("✓ Domain context extraction successfully routed to health advisory service.")

def test_chatbot_demo_fallback():
    bot = ChatbotService(api_key="")
    # Test fallback in unconfigured mode
    res = bot.process_message("What is the current AQI in Delhi?", force_demo=True)
    assert res["is_demo"] is True
    assert "DEMO RESPONSE" in res["content"]
    assert "Delhi" in res["content"]
    print("✓ Chatbot accurately falls back to labeled demo mode when unconfigured.")

def test_conversation_history_handling():
    bot = ChatbotService(api_key="")
    history = [
        {"role": "user", "content": "Hello AERIS AI"},
        {"role": "assistant", "content": "Welcome to AERIS AI!"}
    ]
    res = bot.process_message("What is PM2.5?", conversation_history=history, force_demo=True)
    assert res["is_demo"] is True
    assert "PM2.5" in res["content"]
    print("✓ Multi-turn conversation history accepted and passed cleanly.")

def test_error_resilience():
    # Test with an invalid dummy key that will fail API call
    bot = ChatbotService(api_key="invalid_dummy_key_12345", provider="gemini")
    res = bot.process_message("What is the AQI in Delhi?", force_demo=False)
    # The chatbot should handle the failure gracefully, return an error alert and fallback text
    assert res["is_demo"] is True
    assert "LLM API Error" in res["content"]
    print("✓ Chatbot gracefully handles HTTP/API errors with diagnostic alert and demo fallback.")

if __name__ == "__main__":
    test_llm_client_missing_key()
    test_context_extraction()
    test_chatbot_demo_fallback()
    test_conversation_history_handling()
    test_error_resilience()
    print("\n🎉 ALL PHASE 2 TESTS PASSED SUCCESSFULLY!")
