import os, sys, streamlit as st
from sqlalchemy import select, or_

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database import SessionLocal
from backend.models   import ReceiptORM
from algorithms.sort  import sort

# --------------------------------------------------
# Helper: delete bad rows (amount 0/1 or vendor Unknown)
# --------------------------------------------------

def purge_bad_rows():
    db   = SessionLocal()
    n    = (
        db.query(ReceiptORM)
          .filter(or_(ReceiptORM.amount.in_([0, 1]), ReceiptORM.vendor == "Unknown"))
          .delete(synchronize_session=False)
    )
    db.commit(); db.close()
    return n

# --------------------------------------------------
# Streamlit page
# --------------------------------------------------

def render():
    st.header("Stored records")

    # Admin button to clean faulty rows
    if st.button("🗑️  Delete faulty rows (amount 0/1 or vendor Unknown)"):
        removed = purge_bad_rows()
        st.success(f"Deleted {removed} faulty rows. Refreshing…")
        st.experimental_rerun()

    db        = SessionLocal()
    receipts  = db.execute(select(ReceiptORM)).scalars().all()
    db.close()

    if not receipts:
        st.info("No receipts in the database.")
        return

    # Sorting controls
    col1, col2 = st.columns(2)
    key  = col1.selectbox("Sort by", options=["vendor", "bill_date", "amount"])
    algo = col2.selectbox("Algorithm", options=["timsort", "quicksort", "mergesort"])

    sorted_recs = sort(receipts, key, algo)

    st.dataframe(
        [
            {
                "vendor":   r.vendor,
                "bill_date": r.bill_date,
                "amount":   r.amount,
                "currency": r.currency,
                "category": r.category,
            }
            for r in sorted_recs
        ],
        use_container_width=True,
    )
