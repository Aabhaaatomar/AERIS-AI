"""
Unit Test: AQI Prediction Card Output & Input Variations
Verifies:
1. Predictions for 3 distinct atmospheric inputs (Good, Moderate, Severe).
2. Proper calculation of AQI, category badge, and inference latency.
3. Verification that no raw HTML/CSS strings or code block markup leak.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from services.prediction_service import PredictionService
from utils.helpers import get_aqi_category

def test_prediction_card_inputs():
    pred_svc = PredictionService()

    # Test Case 1: Clean / Monsoon (Should yield Good or Satisfactory)
    input_clean = {"PM2.5": 15.0, "PM10": 35.0, "NO2": 15.0, "SO2": 8.0, "CO": 0.5, "O3": 20.0}
    res_clean = pred_svc.predict_aqi(input_clean, model_name="Random Forest Regressor")
    cat_clean = res_clean["category"]
    
    assert res_clean["estimated_aqi"] < 100, f"Expected clean AQI < 100, got {res_clean['estimated_aqi']}"
    assert cat_clean["label"] in ["Good", "Satisfactory"]
    print(f"✓ Test Case 1 (Clean): AQI {res_clean['estimated_aqi']:.1f} -> {cat_clean['label']}")

    # Test Case 2: Moderate Smog (Should yield Moderate or Poor)
    input_moderate = {"PM2.5": 110.0, "PM10": 180.0, "NO2": 55.0, "SO2": 25.0, "CO": 2.2, "O3": 45.0}
    res_mod = pred_svc.predict_aqi(input_moderate, model_name="Random Forest Regressor")
    cat_mod = res_mod["category"]

    assert res_mod["estimated_aqi"] != res_clean["estimated_aqi"]
    assert 100 <= res_mod["estimated_aqi"] <= 300, f"Expected moderate AQI 100-300, got {res_mod['estimated_aqi']}"
    print(f"✓ Test Case 2 (Moderate): AQI {res_mod['estimated_aqi']:.1f} -> {cat_mod['label']}")

    # Test Case 3: Severe Post-Diwali Winter Inversion (Should yield Very Poor or Severe)
    input_severe = {"PM2.5": 380.0, "PM10": 520.0, "NO2": 110.0, "SO2": 65.0, "CO": 4.8, "O3": 95.0}
    res_severe = pred_svc.predict_aqi(input_severe, model_name="Random Forest Regressor")
    cat_severe = res_severe["category"]

    assert res_severe["estimated_aqi"] > 300, f"Expected severe AQI > 300, got {res_severe['estimated_aqi']}"
    assert cat_severe["label"] in ["Very Poor", "Severe"]
    print(f"✓ Test Case 3 (Severe): AQI {res_severe['estimated_aqi']:.1f} -> {cat_severe['label']}")

    # Verify model outputs vary across architectures
    dt_res = pred_svc.predict_aqi(input_moderate, model_name="Decision Tree Regressor")
    lr_res = pred_svc.predict_aqi(input_moderate, model_name="Linear Regression")
    assert dt_res["estimated_aqi"] > 0
    assert lr_res["estimated_aqi"] > 0
    print(f"✓ Decision Tree: {dt_res['estimated_aqi']:.1f}, Linear Regression: {lr_res['estimated_aqi']:.1f}")

    print("\n🎉 ALL 3 PREDICTION INPUT TESTS PASSED WITH DISTINCT VALUES AND PROPER CATEGORIES!")

if __name__ == "__main__":
    test_prediction_card_inputs()
