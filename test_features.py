import pandas as pd
from app.features import build_features

def test_feature_count():
    row = {
        "current_assets": 200, "current_liabilities": 100, "cash": 50,
        "total_assets": 500, "total_liabilities": 250, "equity": 250,
        "revenue": 600, "ebit": 90, "net_income": 60,
        "operating_cash_flow": 80, "interest_expense": 20,
        "inventory": 100, "accounts_receivable": 60, "debt": 180
    }
    x = build_features(pd.DataFrame([row]))
    assert x.shape == (1, 13)
    assert x.iloc[0]["current_ratio"] == 2.0
