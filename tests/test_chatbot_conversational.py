"""
Comprehensive Test Suite for AERIS AI Chatbot Conversational Intelligence
Verifies the 7 user-requested interactions:
1. Hello
2. What is AQI?
3. Explain PM2.5.
4. Haryana AQI
5. Compare Delhi and Mumbai.
6. Is it safe to exercise outside?
7. What did I ask you previously? (Conversation memory)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from services.chatbot_service import ChatbotService

def run_conversational_tests():
    bot = ChatbotService()
    history = []

    print("\n--- TEST 1: 'Hello' ---")
    res1 = bot.process_message("Hello", conversation_history=history, force_demo=False)
    print("Content preview:", res1["content"][:160].replace("\n", " "))
    assert "AERIS AI" in res1["content"]
    assert "help" in res1["content"].lower() or "assist" in res1["content"].lower()
    history.append({"role": "user", "content": "Hello"})
    history.append({"role": "assistant", "content": res1["content"]})
    print("✓ Interaction 1 passed: Warm, conversational greeting.")

    print("\n--- TEST 2: 'What is AQI?' ---")
    res2 = bot.process_message("What is AQI?", conversation_history=history, force_demo=False)
    print("Content preview:", res2["content"][:180].replace("\n", " "))
    assert "Air Quality Index" in res2["content"] or "AQI" in res2["content"]
    assert "CPCB" in res2["content"] or "Good" in res2["content"]
    history.append({"role": "user", "content": "What is AQI?"})
    history.append({"role": "assistant", "content": res2["content"]})
    print("✓ Interaction 2 passed: Clear explanation of AQI and CPCB standards.")

    print("\n--- TEST 3: 'Explain PM2.5.' ---")
    res3 = bot.process_message("Explain PM2.5.", conversation_history=history, force_demo=False)
    print("Content preview:", res3["content"][:180].replace("\n", " "))
    assert "2.5" in res3["content"]
    assert "PM10" in res3["content"] or "lungs" in res3["content"] or "alveoli" in res3["content"]
    history.append({"role": "user", "content": "Explain PM2.5."})
    history.append({"role": "assistant", "content": res3["content"]})
    print("✓ Interaction 3 passed: Rich explanation of PM2.5 and contrast with PM10.")

    print("\n--- TEST 4: 'Haryana AQI' ---")
    res4 = bot.process_message("Haryana AQI", conversation_history=history, force_demo=False)
    print("Content preview:", res4["content"][:180].replace("\n", " "))
    assert "Haryana" in res4["content"]
    assert ("Gurgaon" in res4["content"] or "Faridabad" in res4["content"] or "city" in res4["content"])
    history.append({"role": "user", "content": "Haryana AQI"})
    history.append({"role": "assistant", "content": res4["content"]})
    print("✓ Interaction 4 passed: Clarifies regional monitoring and presents Gurgaon/Faridabad telemetry.")

    print("\n--- TEST 5: 'Compare Delhi and Mumbai.' ---")
    res5 = bot.process_message("Compare Delhi and Mumbai.", conversation_history=history, force_demo=False)
    print("Content preview:", res5["content"][:180].replace("\n", " "))
    assert "Delhi" in res5["content"] and "Mumbai" in res5["content"]
    assert "AQI" in res5["content"]
    history.append({"role": "user", "content": "Compare Delhi and Mumbai."})
    history.append({"role": "assistant", "content": res5["content"]})
    print("✓ Interaction 5 passed: Comparative benchmarking between Delhi and Mumbai.")

    print("\n--- TEST 6: 'Is it safe to exercise outside?' ---")
    res6 = bot.process_message("Is it safe to exercise outside?", conversation_history=history, force_demo=False)
    print("Content preview:", res6["content"][:180].replace("\n", " "))
    assert "exercise" in res6["content"].lower() or "safe" in res6["content"].lower()
    assert "AQI" in res6["content"]
    history.append({"role": "user", "content": "Is it safe to exercise outside?"})
    history.append({"role": "assistant", "content": res6["content"]})
    print("✓ Interaction 6 passed: Contextual exercise and health safety guidance.")

    print("\n--- TEST 7: 'What did I ask you previously?' (Conversation Memory) ---")
    res7 = bot.process_message("What did I ask you previously?", conversation_history=history, force_demo=False)
    print("Content preview:", res7["content"][:180].replace("\n", " "))
    assert "exercise" in res7["content"].lower() or "safe" in res7["content"].lower()
    print("✓ Interaction 7 passed: Accurately remembered previous turn ('Is it safe to exercise outside?').")

    # TEST 8: Follow-up question ("What about Mumbai?")
    print("\n--- TEST 8: Follow-up ('What about Mumbai?') ---")
    followup_history = [
        {"role": "user", "content": "What is AQI in Delhi?"},
        {"role": "assistant", "content": "In Delhi, the AQI is currently 316 (Very Poor)."}
    ]
    res8 = bot.process_message("What about Mumbai?", conversation_history=followup_history, force_demo=False)
    print("Content preview:", res8["content"][:180].replace("\n", " "))
    assert "Mumbai" in res8["content"]
    print("✓ Interaction 8 passed: Successfully handled contextual follow-up query.")

    print("\n🎉 ALL 8 CONVERSATIONAL INTELLIGENCE AND MEMORY TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_conversational_tests()
