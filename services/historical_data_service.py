"""
AERIS AI - Historical Data Service
Ingests, validates, and serves longitudinal CPCB atmospheric datasets (2023-2024).
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional

import config

class HistoricalDataService:
    """Service for longitudinal CPCB air quality dataset operations."""

    REQUIRED_COLUMNS = [
        "Date", "City", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3",
        "AQI", "AQI_Bucket", "Dominant_Pollutant"
    ]

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = Path(data_path) if data_path else (config.DATA_DIR / "city_day_cpcb.csv")
        self._df: Optional[pd.DataFrame] = None
        self._metadata: Optional[Dict[str, Any]] = None

    def load_data(self) -> Optional[pd.DataFrame]:
        """Load and parse the CPCB historical dataset with datetime indexing."""
        if self._df is None:
            if not self.data_path.exists():
                return None
            df = pd.read_csv(self.data_path)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month
            df["Month_Name"] = df["Date"].dt.strftime("%b")
            self._df = df
        return self._df

    def validate_dataset(self) -> Dict[str, Any]:
        """
        Validate dataset structure, schema integrity, and quality metrics.
        """
        df = self.load_data()
        if df is None:
            return {"valid": False, "error": "Dataset file not found."}

        missing_cols = [c for c in self.REQUIRED_COLUMNS if c not in df.columns]
        if missing_cols:
            return {
                "valid": False,
                "error": f"Missing required columns: {missing_cols}"
            }

        null_counts = df[self.REQUIRED_COLUMNS].isnull().sum().to_dict()
        total_rows = len(df)
        cities = sorted(df["City"].unique().tolist())
        date_min = df["Date"].min().strftime("%Y-%m-%d")
        date_max = df["Date"].max().strftime("%Y-%m-%d")

        return {
            "valid": True,
            "total_rows": total_rows,
            "cities": cities,
            "city_count": len(cities),
            "date_range": (date_min, date_max),
            "null_counts": null_counts,
            "has_nulls": any(v > 0 for v in null_counts.values()),
            "years_covered": sorted(df["Year"].unique().tolist())
        }

    def get_dataset_metadata(self) -> Dict[str, Any]:
        """Return cached summary metadata."""
        if self._metadata is None:
            val = self.validate_dataset()
            if val["valid"]:
                df = self.load_data()
                self._metadata = {
                    "total_records": val["total_rows"],
                    "cities": val["cities"],
                    "date_span": f"{val['date_range'][0]} to {val['date_range'][1]}",
                    "overall_mean_aqi": round(df["AQI"].mean(), 1),
                    "clean_days_pct": round((df["AQI"] <= 100).mean() * 100, 1),
                    "severe_days_pct": round((df["AQI"] >= 401).mean() * 100, 1)
                }
        return self._metadata or {}

    def get_city_metrics(self, city: str, year: Optional[int] = None) -> Dict[str, Any]:
        """Compute key longitudinal summary KPIs for a specific city."""
        df = self.load_data()
        if df is None:
            return {}

        city_df = df[df["City"].str.lower() == city.strip().lower()]
        if year:
            city_df = city_df[city_df["Year"] == year]

        if city_df.empty:
            return {}

        total_days = len(city_df)
        clean_days = (city_df["AQI"] <= 100).sum()
        severe_days = (city_df["AQI"] >= 401).sum()

        dominant_mode = city_df["Dominant_Pollutant"].mode()
        primary_driver = dominant_mode[0] if not dominant_mode.empty else "PM2.5"

        return {
            "city": city,
            "record_count": total_days,
            "avg_aqi": round(city_df["AQI"].mean(), 1),
            "median_aqi": round(city_df["AQI"].median(), 1),
            "max_aqi": round(city_df["AQI"].max(), 1),
            "min_aqi": round(city_df["AQI"].min(), 1),
            "clean_days_pct": round((clean_days / total_days) * 100, 1),
            "severe_days_pct": round((severe_days / total_days) * 100, 1),
            "primary_driver": primary_driver,
            "pollutant_means": {
                "PM2.5": round(city_df["PM2.5"].mean(), 1),
                "PM10": round(city_df["PM10"].mean(), 1),
                "NO2": round(city_df["NO2"].mean(), 1),
                "SO2": round(city_df["SO2"].mean(), 1),
                "CO": round(city_df["CO"].mean(), 2),
                "O3": round(city_df["O3"].mean(), 1)
            }
        }

    def get_monthly_aggregates(self, city: str, parameter: str = "AQI", year: Optional[int] = None) -> pd.DataFrame:
        """Calculate mean parameter levels grouped by calendar month."""
        df = self.load_data()
        if df is None:
            return pd.DataFrame()

        city_df = df[df["City"].str.lower() == city.strip().lower()].copy()
        if year:
            city_df = city_df[city_df["Year"] == year]

        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        monthly = city_df.groupby("Month_Name")[parameter].agg(["mean", "min", "max", "std"]).reindex(month_order).dropna().reset_index()
        monthly.columns = ["Month", "Mean", "Min", "Max", "Std"]
        monthly["Mean"] = monthly["Mean"].round(1)
        return monthly

    def get_yearly_comparison(self, city: str) -> Dict[str, Any]:
        """Compute head-to-head annual aggregates for 2023 vs 2024."""
        df = self.load_data()
        if df is None:
            return {}

        city_df = df[df["City"].str.lower() == city.strip().lower()]
        years = sorted(city_df["Year"].unique().tolist())
        
        comparison = {}
        for y in years:
            ydf = city_df[city_df["Year"] == y]
            comparison[y] = {
                "avg_aqi": round(ydf["AQI"].mean(), 1),
                "clean_days": int((ydf["AQI"] <= 100).sum()),
                "severe_days": int((ydf["AQI"] >= 401).sum()),
                "peak_aqi": round(ydf["AQI"].max(), 1),
                "avg_pm25": round(ydf["PM2.5"].mean(), 1)
            }

        # Calculate YoY Delta if 2023 & 2024 present
        if 2023 in comparison and 2024 in comparison:
            aqi_delta = round(comparison[2024]["avg_aqi"] - comparison[2023]["avg_aqi"], 1)
            comparison["yoy_aqi_delta"] = aqi_delta
            comparison["yoy_pct_change"] = round((aqi_delta / comparison[2023]["avg_aqi"]) * 100, 1)

        return comparison

    def get_city_rankings(self, year: Optional[int] = None) -> pd.DataFrame:
        """Rank all cities based on longitudinal average AQI."""
        df = self.load_data()
        if df is None:
            return pd.DataFrame()

        filtered = df if not year else df[df["Year"] == year]
        
        ranks = filtered.groupby("City").agg(
            Avg_AQI=("AQI", "mean"),
            Peak_AQI=("AQI", "max"),
            Avg_PM25=("PM2.5", "mean"),
            Clean_Days_Pct=("AQI", lambda x: (x <= 100).mean() * 100)
        ).round(1).sort_values("Avg_AQI").reset_index()

        ranks["Rank"] = range(1, len(ranks) + 1)
        return ranks[["Rank", "City", "Avg_AQI", "Peak_AQI", "Avg_PM25", "Clean_Days_Pct"]]

    def get_correlations(self, city: str) -> pd.DataFrame:
        """Compute pollutant-to-AQI Pearson correlation coefficients."""
        df = self.load_data()
        if df is None:
            return pd.DataFrame()

        city_df = df[df["City"].str.lower() == city.strip().lower()]
        pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "AQI"]
        corr = city_df[pollutants].corr()["AQI"].drop("AQI").round(3).reset_index()
        corr.columns = ["Pollutant", "Correlation_With_AQI"]
        return corr.sort_values("Correlation_With_AQI", ascending=False)
