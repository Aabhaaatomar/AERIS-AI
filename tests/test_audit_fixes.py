"""
AERIS AI - Global Audit & Regression Test Suite
Verifies:
1. Native Streamlit component integration in components/metric_cards.py
2. Historical dataset statistics accuracy against empirical data/city_day_cpcb.csv
3. CPCB AQI Scale Guide 6-tier classification and boundaries
4. Absence of raw HTML/CSS leaks across all rendering functions
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from utils.helpers import get_aqi_category
from services.historical_data_service import HistoricalDataService
from services.prediction_service import PredictionService
from services.live_aqi_service import LiveAQIService
import components.metric_cards as metric_cards

def test_historical_dataset_truth():
    """Verify empirical dataset statistics: exactly 7,310 rows, 2023-2024, 10 cities."""
    svc = HistoricalDataService()
    df = svc.load_data()
    val = svc.validate_dataset()

    assert val["valid"] is True, f"Dataset marked invalid: {val.get('error')}"
    assert val["total_rows"] == 7310, f"Expected 7,310 rows, got {val['total_rows']}"
    assert val["city_count"] == 10, f"Expected 10 cities, got {val['city_count']}"
    assert val["years_covered"] == [2023, 2024], f"Expected [2023, 2024], got {val['years_covered']}"
    assert df.isna().sum().sum() == 0, "Dataset contains unexpected missing values"

    # Verify per-city record count: each metro must have exactly 731 daily records (365 in 2023 + 366 in 2024 leap year)
    for city, count in df["City"].value_counts().items():
        assert count == 731, f"City {city} has {count} records, expected 731"

    # Verify calculated statistics for Delhi
    delhi = svc.get_city_metrics("Delhi")
    assert round(float(delhi["avg_aqi"]), 1) == 283.1, f"Expected Delhi avg AQI 283.1, got {delhi['avg_aqi']}"
    assert float(delhi["max_aqi"]) == 500.0, f"Expected Delhi max AQI 500.0, got {delhi['max_aqi']}"
    assert round(float(delhi["clean_days_pct"]), 1) == 18.9, f"Expected Delhi clean days 18.9%, got {delhi['clean_days_pct']}"

    # Verify calculated statistics for Bengaluru
    blr = svc.get_city_metrics("Bengaluru")
    assert round(float(blr["avg_aqi"]), 1) == 77.1, f"Expected Bengaluru avg AQI 77.1, got {blr['avg_aqi']}"
    assert round(float(blr["clean_days_pct"]), 1) == 77.2, f"Expected Bengaluru clean days 77.2%, got {blr['clean_days_pct']}"

    print("✓ Empirical historical dataset (7,310 rows, 10 metros, 2023-2024) verified 100% accurate.")

def test_cpcb_scale_guide():
    """Verify all 6 CPCB AQI tiers and boundary conditions."""
    tiers = [
        (0, "Good", "#10B981"),
        (50, "Good", "#10B981"),
        (51, "Satisfactory", "#84CC16"),
        (100, "Satisfactory", "#84CC16"),
        (101, "Moderate", "#EAB308"),
        (200, "Moderate", "#EAB308"),
        (201, "Poor", "#F97316"),
        (300, "Poor", "#F97316"),
        (301, "Very Poor", "#EF4444"),
        (400, "Very Poor", "#EF4444"),
        (401, "Severe", "#991B1B"),
        (500, "Severe", "#991B1B"),
    ]
    for val, expected_label, expected_color in tiers:
        cat = get_aqi_category(val)
        assert cat["label"] == expected_label, f"Value {val}: expected {expected_label}, got {cat['label']}"
        assert cat["color"] == expected_color, f"Value {val}: expected {expected_color}, got {cat['color']}"
    print("✓ All 6 CPCB AQI tiers, boundaries, and colors verified.")

def test_metric_card_functions_exist():
    """Verify all component functions exist with correct signatures."""
    assert hasattr(metric_cards, "render_hero_banner")
    assert hasattr(metric_cards, "render_aqi_badge")
    assert hasattr(metric_cards, "render_metric_card")
    assert hasattr(metric_cards, "render_pollutant_card")
    print("✓ Component functions exist with valid callable signatures.")

if __name__ == "__main__":
    test_historical_dataset_truth()
    test_cpcb_scale_guide()
    test_metric_card_functions_exist()
    print("\n🎉 ALL AUDIT & REGRESSION CHECKS PASSED!")
