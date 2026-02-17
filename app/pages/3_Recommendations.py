from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from app.auth import auth_widget, require_tier
from app.data import build_asset_report

st.set_page_config(page_title="Recommendations", layout="wide")
auth_widget()
st.title("Recommendations")

if not require_tier("pro"):
    st.stop()

st.caption("Rules-based engine v1")

tickers_raw = st.text_input("Tickers", value="SPY,QQQ,TLT")
benchmark = st.text_input("Benchmark", value="SPY")
start = st.date_input("Start", value=date.today() - timedelta(days=365 * 3))
end = st.date_input("End", value=date.today())

if st.button("Generate"):
    tickers = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]
    report = build_asset_report(tickers=tickers, start_date=start, end_date=end, frequency="Daily", benchmark=benchmark)
    if not report.recommendations:
        st.success("No high-priority rules triggered.")

    for rec in report.recommendations:
        with st.expander(rec.title, expanded=True):
            st.write(rec.reasoning)
            st.json(rec.trigger_metrics)
            st.markdown("**Actions**")
            for step in rec.recommendation_steps:
                st.write(f"- {step}")
            st.write(f"Expected impact: {rec.expected_impact}")
            st.write(f"Confidence: {rec.confidence:.0%}")

    st.subheader("What-if (simple)")
    shift = st.slider("Reduce risk assets by %", min_value=0, max_value=30, value=10)
    st.info(f"Estimated volatility reduction: {shift * 0.2:.1f}% (heuristic)")
