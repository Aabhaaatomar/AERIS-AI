"""
AERIS AI - Phase 5 Machine Learning Inference & Evaluation Test Suite
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.prediction_service import PredictionService

def test_models_loading():
    svc = PredictionService()
    for m in ["random_forest", "decision_tree", "linear_regression"]:
        model = svc.load_model(m)
        assert model is not None, f"Failed to load model: {m}"
    print("✓ All 3 machine learning regression models successfully deserialized.")

def test_prediction_inference():
    svc = PredictionService()
    test_inputs = {
        "PM2.5": 142.5,
        "PM10": 235.0,
        "NO2": 52.0,
        "SO2": 18.0,
        "CO": 2.1,
        "O3": 44.0
    }
    
    for m in ["random_forest", "decision_tree", "linear_regression"]:
        res = svc.predict_aqi(test_inputs, model_name=m)
        assert "estimated_aqi" in res
        assert 0 <= res["estimated_aqi"] <= 500
        assert res["latency_ms"] >= 0
        assert res["category"]["label"] in ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
        assert "metrics" in res
        print(f"✓ {res['model_name']} predicted AQI {res['estimated_aqi']} ({res['category']['label']}) in {res['latency_ms']} ms.")

def test_input_validation_and_clamping():
    svc = PredictionService()
    # Pass extreme / negative numbers
    out_of_bounds = {
        "PM2.5": -50.0,
        "PM10": 3000.0,
        "NO2": 999.0,
        "SO2": -10.0,
        "CO": 150.0,
        "O3": -5.0
    }
    validated = svc.validate_inputs(out_of_bounds)
    assert validated["PM2.5"] == 0.0
    assert validated["PM10"] == 1500.0
    assert validated["SO2"] == 0.0
    print("✓ Physical atmospheric bounds validation and input clamping verified.")

def test_benchmark_metrics():
    svc = PredictionService()
    metrics = svc.get_metrics()
    assert "metrics" in metrics
    rf = metrics["metrics"]["Random Forest"]
    assert rf["R2"] >= 0.99
    assert rf["MAE"] < 1.0
    print(f"✓ Verified benchmark scores: Random Forest R² = {rf['R2']}, MAE = {rf['MAE']}.")

if __name__ == "__main__":
    test_models_loading()
    test_prediction_inference()
    test_input_validation_and_clamping()
    test_benchmark_metrics()
    print("\n🎉 ALL PHASE 5 TESTS PASSED SUCCESSFULLY!")
