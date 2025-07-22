from datetime import date
from sqlalchemy import Column, Integer, String, Date, Float
from backend.database import Base
from pydantic import BaseModel, Field, model_validator
from backend.currency import detect_currency

class ReceiptORM(Base):
    __tablename__ = "receipts"
    id        = Column(Integer, primary_key=True, index=True)
    vendor    = Column(String,  index=True)
    bill_date = Column(Date,    index=True)
    amount    = Column(Float)           # numeric value in original currency
    currency  = Column(String(3))
    category  = Column(String, nullable=True)

class Receipt(BaseModel):
    vendor:     str  = Field(..., min_length=1)
    bill_date:  date
    amount_raw: str
    currency:   str | None = None
    category:   str | None = None
    amount_val: float = 0.0

    @model_validator(mode="before")
    def parse_amount(cls, v):
        code, num       = detect_currency(v.get("amount_raw", ""))
        v["currency"]   = code
        v["amount_val"] = num
        return v

    model_config = {"from_attributes": True}
