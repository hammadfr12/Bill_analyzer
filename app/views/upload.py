import streamlit as st
import shutil, uuid, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.ocr import file_to_text
from backend.parser import parse
from backend.database import SessionLocal
from backend.models import ReceiptORM

# --------------------------------------------------
# Streamlit Page
# --------------------------------------------------

def render():
    st.header("Upload a receipt / bill")

    files = st.file_uploader(
        "Choose receipt files (image / PDF / text)",
        type=["png", "jpg", "jpeg", "pdf", "txt"],
        accept_multiple_files=True,
    )

    show_ocr = st.checkbox("Show OCR text for debugging", value=False)

    if st.button("Process") and files:
        db = SessionLocal()
        for f in files:
            try:
                # ---------------- Save file locally ----------------
                fname = f"{uuid.uuid4()}{os.path.splitext(f.name)[1]}"
                path  = os.path.join("data", fname)
                with open(path, "wb") as out_file:
                    shutil.copyfileobj(f, out_file)

                # ---------------- OCR + parsing -------------------
                text = file_to_text(path)
                if show_ocr:
                    st.text_area(f"OCR ({f.name})", text, height=150)

                rec  = parse(text)

                # ---------------- Persist to DB ------------------
                db.add(ReceiptORM(
                    vendor=rec.vendor,
                    bill_date=rec.bill_date,
                    amount=rec.amount_val,
                    currency=rec.currency,
                    category=rec.category,
                ))
                db.commit()

                st.success(f"✅ {f.name}: {rec.vendor} – {rec.amount_val:.2f} {rec.currency}")

            except Exception as e:
                st.error(f"❌ {f.name} failed: {e}")
        db.close()
