import streamlit as st, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
import matplotlib.pyplot as plt
from algorithms.aggregate import summary

def render():
    st.header("Insights")
    stats, df = summary()
    if not stats:
        st.info("Upload data first.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", f"{stats['total_spend']:.2f}")
    col2.metric("Average", f"{stats['mean']:.2f}")
    col3.metric("Median", f"{stats['median']:.2f}")

    st.subheader("Top Vendors")
    st.bar_chart(pd.Series(stats["top_vendors"]))

    st.subheader("Monthly Trend")
    trend = pd.Series(stats["monthly_trend"]).sort_index()
    fig, ax = plt.subplots()
    trend.plot(ax=ax, linewidth=2)
    ax.set_ylabel("Amount")
    st.pyplot(fig)
