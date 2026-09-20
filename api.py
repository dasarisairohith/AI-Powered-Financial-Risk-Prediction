import io
import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from .database import get_db
from .models import Prediction
from .schemas import FinancialInput, PredictionResponse
from .ml import predict_one

router = APIRouter()

@router.get("/model-info")
def model_info():
    return {
        "model": "RandomForestClassifier",
        "target": "financial distress risk probability",
        "risk_bands": {"Low": "< 33%", "Medium": "33%–65%", "High": ">= 66%"},
        "features": 13,
    }

@router.post("/predict", response_model=PredictionResponse)
def predict(payload: FinancialInput, db: Session = Depends(get_db)):
    try:
        p, band, score, ratios, explanations = predict_one(payload.model_dump())
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    record = Prediction(company=payload.company, risk_probability=p, risk_band=band)
    db.add(record)
    db.commit()
    return {
        "company": payload.company,
        "risk_probability": round(p, 4),
        "risk_band": band,
        "risk_score": score,
        "ratios": ratios,
        "explanations": explanations,
    }

@router.post("/predict/csv")
async def predict_csv(file: UploadFile = File(...)):
    raw = await file.read()
    df = pd.read_csv(io.BytesIO(raw))
    required = [
        "company","current_assets","current_liabilities","cash","total_assets",
        "total_liabilities","equity","revenue","ebit","net_income",
        "operating_cash_flow","interest_expense","inventory",
        "accounts_receivable","debt"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail={"missing_columns": missing})
    results = []
    for row in df.to_dict(orient="records"):
        try:
            p, band, score, ratios, explanations = predict_one(row)
            results.append({"company": row["company"], "risk_probability": round(p,4), "risk_band": band, "risk_score": score, "explanations": explanations})
        except Exception as e:
            results.append({"company": row.get("company","Unknown"), "error": str(e)})
    return {"results": results}

@router.get("/predictions")
def predictions(db: Session = Depends(get_db)):
    rows = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(50).all()
    return [
        {"id": r.id, "company": r.company, "risk_probability": r.risk_probability, "risk_band": r.risk_band, "created_at": r.created_at}
        for r in rows
    ]
