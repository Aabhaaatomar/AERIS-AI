"""
AERIS AI - End-to-End System & Integration Test Suite (Phases 6 & 7)
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.chatbot_service import ChatbotService
from services.live_aqi_service import LiveAQIService
from services.historical_data_service import HistoricalDataService
from services.prediction_service import PredictionService
from services.recommendation_service import RecommendationService
import config

def test_full_chatbot_multi_service_orchestration():
    bot = ChatbotService()
    
    # Query requesting ML prediction + health advice
    complex_query = "Predict AQI if PM2.5=180 and PM10=320, and tell me precautions for Delhi"
    ctx = bot.extract_context_from_services(complex_query)
    
    assert "[ML PREDICTION ENGINE]" in ctx
    assert "[CPCB HEALTH MATRIX]" in ctx
    assert "[CURRENT TELEMETRY FOR DELHI]" in ctx
    assert "[HISTORICAL ARCHIVE FOR DELHI]" in ctx
    
    # Process message through bot (demo fallback or LLM)
    res = bot.process_message(complex_query, force_demo=True)
    assert res["content"] is not None
    assert len(res["content"]) > 100
    print("✓ Phase 6: Chatbot dynamically orchestrates Live, Historical, ML, and Health services simultaneously!")

def test_deployment_configuration():
    # Verify required files exist for Streamlit Community Cloud
    req_file = config.BASE_DIR / "requirements.txt"
    app_file = config.BASE_DIR / "app.py"
    config_file = config.BASE_DIR / ".streamlit" / "config.toml"
    readme_file = config.BASE_DIR / "README.md"
    dataset_file = config.DATA_DIR / "city_day_cpcb.csv"
    
    assert req_file.exists(), "Missing requirements.txt"
    assert app_file.exists(), "Missing app.py"
    assert config_file.exists(), "Missing config.toml"
    assert readme_file.exists(), "Missing README.md"
    assert dataset_file.exists(), "Missing dataset"
    
    # Verify no local hardcoded machine paths in code
    for py_file in config.BASE_DIR.glob("**/*.py"):
        if "tests" in str(py_file):
            continue
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "C:\\Users\\" not in content, f"Hardcoded Windows path found in {py_file}"
            assert "C:/Users/" not in content, f"Hardcoded Windows path found in {py_file}"
            
    print("✓ Phase 7: Deployment readiness verified. Zero hardcoded local paths. All cloud assets intact.")

if __name__ == "__main__":
    test_full_chatbot_multi_service_orchestration()
    test_deployment_configuration()
    print("\n🎉 ALL END-TO-END DEPLOYMENT TESTS PASSED SUCCESSFULLY!")
