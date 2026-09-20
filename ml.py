import json
import os
import joblib
import pandas as pd
from .features import FEATURES, build_features

MODEL_PATH = os.getenv("MODEL_PATH", "models/risk_model.joblib")

def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)

def predict_one(payload):
    model = load_model()
    if model is None:
        raise FileNotFoundError("Model not trained. Run: python scripts/generate_data.py && python scripts/train.py")
    df = pd.DataFrame([payload])
    X = build_features(df)[FEATURES]
    probability = float(model.predict_proba(X)[0, 1])
    band = "High" if probability >= 0.66 else ("Medium" if probability >= 0.33 else "Low")
    score = round(probability * 100)
    ratios = X.iloc[0].to_dict()

    directions = {
        "debt_to_assets": "lower is generally less leveraged",
        "debt_to_equity": "lower is generally less leveraged",
        "current_ratio": "higher generally indicates more short-term liquidity",
        "cash_ratio": "higher generally indicates stronger immediate liquidity",
        "roa": "higher generally indicates stronger asset profitability",
        "interest_coverage": "higher generally indicates greater ability to cover interest",
        "ocf_to_debt": "higher generally indicates stronger cash-flow coverage of debt",
    }
    importances = getattr(model, "feature_importances_", [0] * len(FEATURES))
    ranked = sorted(zip(FEATURES, importances), key=lambda z: z[1], reverse=True)[:5]
    explanations = [
        {"feature": f, "value": round(float(ratios[f]), 4), "importance": round(float(i), 4), "interpretation": directions.get(f, "")}
        for f, i in ranked
    ]
    return probability, band, score, ratios, explanations
