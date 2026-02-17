from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from app.auth import auth_widget, require_tier
from app.data import build_portfolio_report
from app.persistence import save_report_for_user
from core.portfolio import validate_weights

st.set_page_config(page_title="Upload Portfolio", layout="wide")
auth_widget()
st.title("Upload Portfolio")

if not require_tier("pro"):
    st.stop()

st.download_button(
    label="Download CSV template",
    data="ticker,weight\nAAPL,0.4\nMSFT,0.3\nTLT,0.3\n",
    file_name="portfolio_template.csv",
)

uploaded = st.file_uploader("Upload CSV (ticker,weight)", type=["csv"])
benchmark = st.text_input("Benchmark", value="SPY")
start = st.date_input("Start", value=date.today() - timedelta(days=365 * 3))
end = st.date_input("End", value=date.today())
frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    ok, message = validate_weights(df)
    if not ok:
        st.error(message)
    else:
        report = build_portfolio_report(df, benchmark=benchmark, start_date=start, end_date=end, frequency=frequency)
        st.subheader("Portfolio Metrics")
        st.dataframe(report.metrics_table)
        st.line_chart(report.equity_curve)
        st.line_chart(report.drawdown_curve)

        if st.session_state.get("user") and st.button("Save report"):
            save_report_for_user(
                supabase_user_id=st.session_state["user"],
                email=st.session_state["user"],
                name="Portfolio",
                benchmark=benchmark,
                cagr=float(report.metrics_table.loc["Portfolio", "CAGR"]),
                sharpe=float(report.metrics_table.loc["Portfolio", "Sharpe"]),
                metadata={"tickers": report.tickers},
            )
            st.success("Saved")
