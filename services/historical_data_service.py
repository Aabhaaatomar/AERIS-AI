"""
AERIS AI - Historical Data Service
Provides longitudinal CPCB atmospheric datasets, aggregates, and trend calculations.
(Phase 4 Integration Target)
"""
import pandas as pd
import config

class HistoricalDataService:
    def __init__(self, data_path: str = None):
        self.data_path = data_path or (config.DATA_DIR / "city_day_cpcb.csv")
        self._df = None

    def load_data(self) -> pd.DataFrame:
        if self._df is None and self.data_path.exists():
            self._df = pd.read_csv(self.data_path)
            self._df["Date"] = pd.to_datetime(self._df["Date"])
        return self._df

    def get_city_metrics(self, city: str) -> dict:
        df = self.load_data()
        if df is None:
            return {}
        city_df = df[df["City"] == city]
        return {
            "avg_aqi": city_df["AQI"].mean(),
            "max_aqi": city_df["AQI"].max(),
            "min_aqi": city_df["AQI"].min(),
            "record_count": len(city_df)
        }
