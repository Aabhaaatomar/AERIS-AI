"""
AERIS AI - Phase 1 Validation & Smoke Tests
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from utils.helpers import get_aqi_category
from services.chatbot_service import ChatbotService
from services.recommendation_service import RecommendationService
from services.historical_data_service import HistoricalDataService
from services.prediction_service import PredictionService
from components.charts import create_aqi_gauge, create_pollutant_comparison_chart, create_city_comparison_bar

def test_aqi_categories():
    test_cases = [
        (25, "Good"),
        (75, "Satisfactory"),
        (150, "Moderate"),
        (250, "Poor"),
        (350, "Very Poor"),
        (450, "Severe")
    ]
    for val, expected in test_cases:
        cat = get_aqi_category(val)
        assert cat["label"] == expected, f"Expected {expected} for {val}, got {cat['label']}"
    print("✓ AQI Categories and CPCB scales verified.")

def test_chatbot_demo_responses():
    bot = ChatbotService()
    for q in config.SUGGESTED_QUESTIONS:
        ans = bot.process_message(q)
        ans_text = ans["content"] if isinstance(ans, dict) else ans
        assert "DEMO RESPONSE" in ans_text or "AERIS AI" in ans_text, f"Invalid demo response for query: {q}"
        assert len(ans_text) > 50, f"Response too short for query: {q}"
    print("✓ All 7 suggested chatbot prompts produce detailed demo responses.")

def test_health_recommendations():
    for val in [30, 80, 160, 240, 360, 480]:
        rec = RecommendationService.get_recommendations(val)
        assert "outdoor_activity" in rec
        assert "mask_guidance" in rec
        assert "sensitive_groups" in rec
        assert "disclaimer" in rec
    print("✓ Health recommendations generated across all 6 AQI severity levels.")

def test_historical_dataset():
    hist = HistoricalDataService()
    df = hist.load_data()
    assert df is not None, "Dataset failed to load"
    assert len(df) == 7310, f"Expected 7310 rows, got {len(df)}"
    delhi_metrics = hist.get_city_metrics("Delhi")
    assert delhi_metrics["record_count"] > 0
    print(f"✓ Historical dataset verified: {len(df)} rows across {df['City'].nunique()} cities.")

def test_prediction_estimator():
    pred = PredictionService()
    est = pred.predict_aqi({"PM2.5": 120, "PM10": 200, "NO2": 50, "CO": 2.0})
    val = est["estimated_aqi"] if isinstance(est, dict) else est
    assert 0 <= val <= 500, f"AQI estimate {val} out of bounds"
    print(f"✓ ML estimation baseline returns valid range: {val} AQI.")

def test_chart_generators():
    gauge = create_aqi_gauge(240, "Test Gauge")
    assert gauge is not None
    bar = create_city_comparison_bar(["Delhi", "Mumbai"], [300, 150])
    assert bar is not None
    print("✓ Plotly chart generators successfully constructed with dark styling.")

if __name__ == "__main__":
    test_aqi_categories()
    test_chatbot_demo_responses()
    test_health_recommendations()
    test_historical_dataset()
    test_prediction_estimator()
    test_chart_generators()
    print("\n🎉 ALL PHASE 1 TESTS PASSED SUCCESSFULLY!")
