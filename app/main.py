import importlib, streamlit as st
import os, sys

# Make backend imports work when running from any page
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(page_title="Bill Analyzer", layout="wide")

# Mapping: sidebar label -> module path
PAGES = {
    "Upload":   "app.views.upload",
    "Records":  "app.views.records",
    "Insights": "app.views.insights",
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", list(PAGES.keys()))

# Dynamically import & render the selected page
module = importlib.import_module(PAGES[choice])
module.render()
