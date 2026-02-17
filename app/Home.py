from __future__ import annotations

import streamlit as st

from app.auth import auth_widget

st.set_page_config(page_title="PortfolioLens", layout="wide")
auth_widget()

st.title("PortfolioLens")
st.caption("Portfolio analytics and actionable recommendations as a micro-SaaS")

st.markdown(
    """
### Demo mode available
- Compare assets and benchmarks instantly
- Upload weighted portfolios and assess performance
- Get rules-based recommendations and what-if guidance

> Sign in to save reports and manage subscription billing.
"""
)

col1, col2 = st.columns(2)
with col1:
    st.info("Free tier: Home + limited Compare")
with col2:
    st.success("Pro tier: Portfolio upload, recommendations, saved reports")
