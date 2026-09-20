from pydantic import BaseModel, Field

class FinancialInput(BaseModel):
    company: str = "Unknown"
    current_assets: float = Field(gt=0)
    current_liabilities: float = Field(gt=0)
    cash: float = Field(ge=0)
    total_assets: float = Field(gt=0)
    total_liabilities: float = Field(ge=0)
    equity: float = Field(gt=0)
    revenue: float = Field(gt=0)
    ebit: float
    net_income: float
    operating_cash_flow: float
    interest_expense: float = Field(ge=0)
    inventory: float = Field(ge=0)
    accounts_receivable: float = Field(ge=0)
    debt: float = Field(ge=0)

class PredictionResponse(BaseModel):
    company: str
    risk_probability: float
    risk_band: str
    risk_score: int
    ratios: dict
    explanations: list[dict]
