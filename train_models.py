"""
AERIS AI - Machine Learning Pipeline
Trains Linear Regression, Decision Tree, and Random Forest Regressors on CPCB dataset.
Saves serialized models via Joblib and exports evaluation metrics.
"""
import os
import json
import joblib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import config

FEATURES = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
TARGET = "AQI"

def train_and_evaluate(random_state: int = 42):
    """Execute complete training, evaluation, and serialization pipeline."""
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    data_path = config.DATA_DIR / "city_day_cpcb.csv"
    
    if not data_path.exists():
        raise FileNotFoundError(f"CPCB dataset missing at {data_path}")

    print(f"Loading CPCB historical records from {data_path}...")
    df = pd.read_csv(data_path)
    df_clean = df.dropna(subset=FEATURES + [TARGET])
    
    X = df_clean[FEATURES]
    y = df_clean[TARGET]
    
    print(f"Training dataset: {X.shape[0]} samples, {len(FEATURES)} features.")

    # 80/20 Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=random_state
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=10, min_samples_leaf=4, random_state=random_state),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_leaf=2, random_state=random_state, n_jobs=-1)
    }

    metrics = {}
    test_eval_df = pd.DataFrame({"Actual_AQI": y_test.values})

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))
        
        metrics[name] = {
            "MAE": round(mae, 3),
            "MSE": round(mse, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 4)
        }
        
        slug = name.lower().replace(" ", "_")
        test_eval_df[f"Pred_{slug}"] = np.round(y_pred, 2)
        test_eval_df[f"Residual_{slug}"] = np.round(y_test.values - y_pred, 2)
        
        save_path = config.MODELS_DIR / f"{slug}.joblib"
        joblib.dump(model, save_path)
        print(f"Saved {name} -> {save_path} (R²: {r2:.4f}, MAE: {mae:.3f})")

    # Feature Importance Analysis
    rf_model = models["Random Forest"]
    dt_model = models["Decision Tree"]
    lr_model = models["Linear Regression"]

    feature_analysis = {
        "features": FEATURES,
        "rf_importances": [round(float(v), 4) for v in rf_model.feature_importances_],
        "dt_importances": [round(float(v), 4) for v in dt_model.feature_importances_],
        "lr_coefficients": [round(float(v), 4) for v in lr_model.coef_],
        "lr_intercept": round(float(lr_model.intercept_), 4)
    }

    best_model_name = max(metrics.keys(), key=lambda k: metrics[k]["R2"])

    summary = {
        "features": FEATURES,
        "target": TARGET,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "metrics": metrics,
        "best_model": best_model_name,
        "feature_analysis": feature_analysis,
        "feature_ranges": {
            feat: {
                "min": float(df_clean[feat].min()),
                "max": float(df_clean[feat].max()),
                "mean": float(df_clean[feat].mean()),
                "median": float(df_clean[feat].median()),
                "std": float(df_clean[feat].std())
            } for feat in FEATURES
        }
    }

    metrics_path = config.MODELS_DIR / "model_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"Saved model metrics to {metrics_path}")

    eval_path = config.MODELS_DIR / "test_evaluation_data.csv"
    test_eval_df.to_csv(eval_path, index=False)
    print(f"Saved evaluation test samples to {eval_path}")

    return summary

if __name__ == "__main__":
    train_and_evaluate()
