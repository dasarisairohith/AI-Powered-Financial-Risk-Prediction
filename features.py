import pandas as pd
import numpy as np

FEATURES = [
    "current_ratio",
    "cash_ratio",
    "debt_to_assets",
    "debt_to_equity",
    "equity_ratio",
    "roa",
    "operating_margin",
    "net_margin",
    "interest_coverage",
    "ocf_to_debt",
    "asset_turnover",
    "inventory_to_assets",
    "receivables_to_revenue",
]

def safe_div(a, b):
    return np.divide(a, b, out=np.zeros_like(np.asarray(a, dtype=float)), where=np.asarray(b, dtype=float)!=0)

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame(index=df.index)
    x["current_ratio"] = safe_div(df.current_assets, df.current_liabilities)
    x["cash_ratio"] = safe_div(df.cash, df.current_liabilities)
    x["debt_to_assets"] = safe_div(df.debt, df.total_assets)
    x["debt_to_equity"] = safe_div(df.debt, df.equity)
    x["equity_ratio"] = safe_div(df.equity, df.total_assets)
    x["roa"] = safe_div(df.net_income, df.total_assets)
    x["operating_margin"] = safe_div(df.ebit, df.revenue)
    x["net_margin"] = safe_div(df.net_income, df.revenue)
    x["interest_coverage"] = safe_div(df.ebit, df.interest_expense)
    x["ocf_to_debt"] = safe_div(df.operating_cash_flow, df.debt)
    x["asset_turnover"] = safe_div(df.revenue, df.total_assets)
    x["inventory_to_assets"] = safe_div(df.inventory, df.total_assets)
    x["receivables_to_revenue"] = safe_div(df.accounts_receivable, df.revenue)
    return x.replace([np.inf, -np.inf], 0).fillna(0)
