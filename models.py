from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    risk_probability = Column(Float, nullable=False)
    risk_band = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
