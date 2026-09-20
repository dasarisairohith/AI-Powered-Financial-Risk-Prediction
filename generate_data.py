from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1500
rows = []

for i in range(n):
    assets = rng.uniform(100, 5000)
    leverage = rng.uniform(0.15, 0.95)
    liabilities = assets * leverage
    equity = max(assets - liabilities, 20)
    debt = liabilities * rng.uniform(0.45, 0.95)
    revenue = assets * rng.uniform(0.45, 2.2)
    margin = rng.normal(0.08, 0.10)
    ebit = revenue * margin
    net_margin = margin - rng.uniform(0.01, 0.08)
    net_income = revenue * net_margin
    current_liabilities = liabilities * rng.uniform(0.25, 0.7)
    current_assets = current_liabilities * rng.uniform(0.5, 3.0)
    cash = current_assets * rng.uniform(0.03, 0.5)
    ocf = max(net_income + rng.normal(0, assets*0.04), -assets*0.1)
    interest = max(debt * rng.uniform(0.015, 0.12), 1)
    inventory = current_assets * rng.uniform(0.1, 0.65)
    ar = revenue * rng.uniform(0.03, 0.25)

    distress_score = (
        2.2 * max(0, leverage - 0.55)
        + 1.3 * max(0, 0.8 - current_assets / current_liabilities)
        + 2.0 * max(0, -margin)
        + 1.2 * max(0, -ocf / max(debt, 1))
        + 0.8 * max(0, 2 - ebit / interest)
        + rng.normal(0, 0.25)
    )
    probability = 1 / (1 + np.exp(-(distress_score - 0.9) * 2.0))
    label = int(rng.random() < probability)

    rows.append({
        "company": f"DemoCo_{i+1:04d}",
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "cash": cash,
        "total_assets": assets,
        "total_liabilities": liabilities,
        "equity": equity,
        "revenue": revenue,
        "ebit": ebit,
        "net_income": net_income,
        "operating_cash_flow": ocf,
        "interest_expense": interest,
        "inventory": inventory,
        "accounts_receivable": ar,
        "debt": debt,
        "risk_label": label,
    })

df = pd.DataFrame(rows)
Path("data").mkdir(exist_ok=True)
df.to_csv("data/financial_risk_demo.csv", index=False)
print(f"Generated {len(df)} rows at data/financial_risk_demo.csv")
