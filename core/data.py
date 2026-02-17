from __future__ import annotations

from datetime import date

import pandas as pd
import yfinance as yf

FREQUENCY_MAP = {
    "Daily": "1d",
    "Weekly": "1wk",
    "Monthly": "1mo",
}


def normalize_prices(raw: pd.DataFrame) -> pd.DataFrame:
    if isinstance(raw.columns, pd.MultiIndex):
        if "Adj Close" in raw.columns.get_level_values(0):
            return raw["Adj Close"].dropna(how="all")
        return raw["Close"].dropna(how="all")
    return raw.to_frame(name="Close")


def fetch_price_data(
    tickers: list[str],
    start: date,
    end: date,
    frequency: str = "Daily",
) -> pd.DataFrame:
    interval = FREQUENCY_MAP.get(frequency, "1d")
    data = yf.download(tickers=tickers, start=start, end=end, interval=interval, auto_adjust=True)
    prices = normalize_prices(data)
    prices = prices.ffill().dropna(how="all")
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])
    return prices
