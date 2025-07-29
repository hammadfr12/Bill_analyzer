import os
import sys
import importlib

import streamlit as st

# ─────────────────────────────────────────────
# Make backend imports work from any page
# ─────────────────────────────────────────────
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

# ─────────────────────────────────────────────
# Initialize Streamlit + Database
# ─────────────────────────────────────────────
st.set_page_config(page_title="Bill Analyzer", layout="wide")

# 1️⃣ Ensure the ./data/ folder exists BEFORE touching the DB
from backend.utils import ensure_upload_dir
ensure_upload_dir()

# 2️⃣ Create the receipts table if it doesn't exist yet
from backend.database import Base, engine
Base.metadata.create_all(bind=engine)

# ─────────────────────────────────────────────
# App header + sidebar nav
# ─────────────────────────────────────────────
st.title("📊 Bill Analyzer")
st.markdown("Easily upload and analyze receipts in multiple currencies.")

PAGES = {
    "Upload":   "app.views.upload",
    "Records":  "app.views.records",
    "Insights": "app.views.insights",
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))

# ─────────────────────────────────────────────
# Dynamically import & render the selected page
# ─────────────────────────────────────────────
try:
    module = importlib.import_module(PAGES[choice])
    module.render()
except Exception as e:
    st.error(f"❌ Failed to load the “{choice}” page:\n{e}")
