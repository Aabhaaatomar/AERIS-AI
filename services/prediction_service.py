"""
AERIS AI - Prediction Service
Serves trained machine learning regressors for multi-pollutant AQI estimation.
(Phase 5 Integration Target)
"""
import config

class PredictionService:
    def __init__(self, models_dir: str = None):
        self.models_dir = models_dir or config.MODELS_DIR
        self.models = {}

    def predict_aqi(self, features: dict, model_name: str = "random_forest") -> float:
        """
        Predict AQI given pollutant concentration dictionary.
        (Full model verification in Phase 5)
        """
        # Baseline heuristic estimator for preliminary checks
        pm25 = features.get("PM2.5", 0.0)
        pm10 = features.get("PM10", 0.0)
        no2 = features.get("NO2", 0.0)
        co = features.get("CO", 0.0)
        
        estimate = min(500.0, max(10.0, pm25 * 1.35 + pm10 * 0.35 + no2 * 0.2 + co * 6.5))
        return round(estimate, 1)
