"""
AERIS AI - Phase 3 Live AQI Ingestion & CPCB Calculations Test Suite
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.live_aqi_service import (
    LiveAQIService,
    calculate_cpcb_sub_index,
    calculate_cpcb_aqi,
    INDIAN_CITY_COORDINATES
)
import config

def test_cpcb_sub_index_formulas():
    # PM2.5 tests (breakpoints: 0-30->0-50, 31-60->51-100, 61-90->101-200, 91-120->201-300, 121-250->301-400, 250+->401-500)
    assert calculate_cpcb_sub_index("PM2.5", 15.0) == 25, "Failed PM2.5 low"
    assert calculate_cpcb_sub_index("PM2.5", 45.0) == 75, "Failed PM2.5 satisfactory"
    assert calculate_cpcb_sub_index("PM2.5", 75.0) == 150, "Failed PM2.5 moderate"
    assert calculate_cpcb_sub_index("PM2.5", 105.0) == 250, "Failed PM2.5 poor"
    assert calculate_cpcb_sub_index("PM2.5", 185.0) == 350, "Failed PM2.5 very poor"
    assert calculate_cpcb_sub_index("PM2.5", 300.0) == 421, "Failed PM2.5 severe"
    
    # Negative / None handling
    assert calculate_cpcb_sub_index("PM2.5", -5.0) is None
    assert calculate_cpcb_sub_index("PM2.5", None) is None
    print("✓ CPCB mathematical sub-index calculation verified across all AQI bands.")

def test_overall_aqi_and_dominant():
    pollutants = {
        "PM2.5": 140.0,  # sub-index ~ 316
        "PM10": 120.0,   # sub-index ~ 113
        "NO2": 35.0,     # sub-index ~ 44
        "SO2": 15.0,     # sub-index ~ 19
        "CO": 1.2,       # sub-index ~ 60
        "O3": 40.0       # sub-index ~ 40
    }
    result = calculate_cpcb_aqi(pollutants)
    assert result["dominant_pollutant"] == "PM2.5"
    assert result["aqi"] > 300
    print(f"✓ Overall CPCB AQI correctly resolves dominant pollutant: {result['dominant_pollutant']} (AQI {result['aqi']}).")

def test_city_coordinates():
    svc = LiveAQIService()
    for city in ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata"]:
        coords = svc.get_city_coordinates(city)
        assert coords is not None
        assert "lat" in coords and "lon" in coords
    print("✓ Metropolitan coordinates indexing verified.")

def test_caching_and_freshness():
    svc = LiveAQIService(cache_ttl_seconds=10)
    # First call
    d1 = svc.get_city_aqi("Delhi")
    assert "aqi" in d1
    assert "timestamp" in d1
    
    # Second call (must be from cache)
    d2 = svc.get_city_aqi("Delhi", force_refresh=False)
    assert d1["timestamp"] == d2["timestamp"]
    assert "delhi" in svc._cache
    print("✓ In-memory caching mechanism verified.")

def test_all_15_indian_cities():
    svc = LiveAQIService()
    for city in config.INDIAN_CITIES:
        data = svc.get_city_aqi(city)
        assert data["city"] is not None
        assert 0 <= data["aqi"] <= 500
        assert "PM2.5" in data["pollutants"]
        assert "PM10" in data["pollutants"]
        assert "NO2" in data["pollutants"]
        assert "SO2" in data["pollutants"]
        assert "CO" in data["pollutants"]
        assert "O3" in data["pollutants"]
        assert "timestamp" in data
        assert "source" in data
    print(f"✓ All {len(config.INDIAN_CITIES)} Indian cities successfully return full telemetry schemas.")

if __name__ == "__main__":
    test_cpcb_sub_index_formulas()
    test_overall_aqi_and_dominant()
    test_city_coordinates()
    test_caching_and_freshness()
    test_all_15_indian_cities()
    print("\n🎉 ALL PHASE 3 TESTS PASSED SUCCESSFULLY!")
