"""
AERIS AI - Phase 4 Historical Analytics Test Suite
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.historical_data_service import HistoricalDataService

def test_dataset_validation():
    svc = HistoricalDataService()
    report = svc.validate_dataset()
    assert report["valid"] is True
    assert report["total_rows"] == 7310
    assert report["city_count"] == 10
    assert report["date_range"] == ("2023-01-01", "2024-12-31")
    assert not report["has_nulls"]
    print("✓ Dataset integrity, schema, and completeness (7,310 rows, 0 nulls) verified.")

def test_city_metrics_and_year_filters():
    svc = HistoricalDataService()
    delhi_all = svc.get_city_metrics("Delhi")
    assert delhi_all["record_count"] == 731
    assert delhi_all["avg_aqi"] > 200
    assert delhi_all["max_aqi"] <= 500
    assert "pollutant_means" in delhi_all
    
    delhi_2023 = svc.get_city_metrics("Delhi", year=2023)
    assert delhi_2023["record_count"] == 365
    print("✓ City metric calculations and temporal filters verified.")

def test_monthly_seasonality():
    svc = HistoricalDataService()
    monthly = svc.get_monthly_aggregates("Delhi", "AQI")
    assert len(monthly) == 12
    assert "Jan" in monthly["Month"].values
    assert "Nov" in monthly["Month"].values
    print("✓ Monthly aggregation across all 12 calendar months verified.")

def test_yearly_comparison():
    svc = HistoricalDataService()
    yoy = svc.get_yearly_comparison("Delhi")
    assert 2023 in yoy
    assert 2024 in yoy
    assert "yoy_pct_change" in yoy
    print(f"✓ YoY comparative benchmarking verified (Delhi YoY delta: {yoy['yoy_aqi_delta']} AQI).")

def test_city_rankings():
    svc = HistoricalDataService()
    ranks = svc.get_city_rankings()
    assert len(ranks) == 10
    # Cleanest city should have lower AQI than most polluted
    assert ranks.iloc[0]["Avg_AQI"] < ranks.iloc[-1]["Avg_AQI"]
    print(f"✓ National city league table verified (Cleanest: {ranks.iloc[0]['City']}, Highest: {ranks.iloc[-1]['City']}).")

def test_pollutant_correlations():
    svc = HistoricalDataService()
    corr = svc.get_correlations("Delhi")
    assert len(corr) == 6
    assert "PM2.5" in corr["Pollutant"].values
    pm25_corr = corr[corr["Pollutant"] == "PM2.5"]["Correlation_With_AQI"].values[0]
    assert pm25_corr > 0.8
    print(f"✓ Pollutant correlation engine verified (PM2.5 correlation: r = {pm25_corr:.3f}).")

if __name__ == "__main__":
    test_dataset_validation()
    test_city_metrics_and_year_filters()
    test_monthly_seasonality()
    test_yearly_comparison()
    test_city_rankings()
    test_pollutant_correlations()
    print("\n🎉 ALL PHASE 4 TESTS PASSED SUCCESSFULLY!")
