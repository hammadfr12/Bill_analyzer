import pandas as pd
from sqlalchemy import select
from backend.database import SessionLocal
from backend.models import ReceiptORM

def summary():
    db = SessionLocal()
    df = pd.read_sql(select(ReceiptORM), db.bind)
    if df.empty: return {}, df

    stats = {
        "total_spend": df["amount"].sum(),
        "mean": df["amount"].mean(),
        "median": df["amount"].median(),
        "mode": df["amount"].mode().iloc[0] if not df["amount"].mode().empty else None,
        "top_vendors": df["vendor"].value_counts().head(5).to_dict(),
    }
    df["month"] = pd.to_datetime(df["bill_date"]).dt.to_period("M")
    stats["monthly_trend"] = df.groupby("month")["amount"].sum().to_dict()
    return stats, df
