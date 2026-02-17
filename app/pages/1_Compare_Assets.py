from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from app.auth import auth_widget
from app.data import build_asset_report

st.set_page_config(page_title="Compare Assets", layout="wide")
auth_widget()
st.title("Compare Assets")

with st.form("compare_form"):
    tickers_raw = st.text_input("Tickers (comma separated)", value="SPY,QQQ,IWM")
    benchmark = st.text_input("Benchmark", value="SPY")
    start = st.date_input("Start", value=date.today() - timedelta(days=365 * 3))
    end = st.date_input("End", value=date.today())
    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
    submitted = st.form_submit_button("Run Analysis")

if submitted:
    tickers = [t.strip().upper() for t in tickers_raw.split(",") if t.strip()]
    report = build_asset_report(tickers=tickers, start_date=start, end_date=end, frequency=frequency, benchmark=benchmark)

    st.subheader("Metrics")
    st.dataframe(report.metrics_table)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Equity Curve")
        st.line_chart(report.equity_curve)
    with c2:
        st.subheader("Drawdown Curve")
        st.line_chart(report.drawdown_curve)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Correlation Matrix")
        st.dataframe(report.correlation_matrix)
    with c4:
        st.subheader("Rolling Correlation")
        st.line_chart(report.rolling_correlation)
