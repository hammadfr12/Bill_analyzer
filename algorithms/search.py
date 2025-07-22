from sqlalchemy import select, or_, and_
from backend.models import ReceiptORM
from backend.database import SessionLocal

def search(keyword: str | None = None,
           min_amt: float | None = None,
           max_amt: float | None = None):
    db = SessionLocal()
    stmt = select(ReceiptORM)
    if keyword:
        like = f"%{keyword.lower()}%"
        stmt = stmt.where(or_(ReceiptORM.vendor.ilike(like),
                              ReceiptORM.category.ilike(like)))
    if min_amt is not None:
        stmt = stmt.where(ReceiptORM.amount >= min_amt)
    if max_amt is not None:
        stmt = stmt.where(ReceiptORM.amount <= max_amt)
    return db.execute(stmt).scalars().all()
