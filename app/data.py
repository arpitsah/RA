from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from core.data import fetch_price_data
from core.portfolio import portfolio_returns
from core.reporting import build_report


@st.cache_data(show_spinner=False, ttl=3600)
def cached_prices(tickers: list[str], start_date: date, end_date: date, frequency: str) -> pd.DataFrame:
    return fetch_price_data(tickers, start_date, end_date, frequency)


def build_asset_report(
    tickers: list[str], start_date: date, end_date: date, frequency: str, benchmark: str
):
    prices = cached_prices(tickers, start_date, end_date, frequency)
    return build_report(
        prices=prices,
        name=tickers[0],
        benchmark=benchmark,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
    )


def build_portfolio_report(
    weights_df: pd.DataFrame,
    benchmark: str,
    start_date: date,
    end_date: date,
    frequency: str,
):
    tickers = weights_df[weights_df.columns[0]].str.upper().tolist()
    price_df = cached_prices(tickers + [benchmark], start_date, end_date, frequency)
    returns = price_df.pct_change().dropna()
    p_returns = portfolio_returns(returns, weights_df)
    merged = pd.concat([p_returns, returns[[benchmark]]], axis=1).dropna()
    synthetic_prices = (1 + merged).cumprod()
    return build_report(
        prices=synthetic_prices,
        name="Portfolio",
        benchmark=benchmark,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
    )
