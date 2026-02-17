from __future__ import annotations

import pandas as pd


def validate_weights(weights: pd.DataFrame) -> tuple[bool, str]:
    needed = {"ticker", "weight"}
    if not needed.issubset(weights.columns.str.lower()):
        return False, "CSV must contain columns ticker and weight"
    mapping = {c.lower(): c for c in weights.columns}
    w = weights[mapping["weight"]].astype(float)
    if (w < 0).any():
        return False, "Weights must be non-negative"
    if abs(w.sum() - 1.0) > 1e-6:
        return False, "Weights must sum to 1"
    return True, "OK"


def portfolio_returns(asset_returns: pd.DataFrame, weights: pd.DataFrame) -> pd.Series:
    mapping = {c.lower(): c for c in weights.columns}
    tickers = weights[mapping["ticker"]].str.upper().tolist()
    w = weights[mapping["weight"]].astype(float).values
    aligned = asset_returns[[t for t in tickers if t in asset_returns.columns]].copy()
    aligned = aligned.fillna(0.0)
    valid_weights = w[: len(aligned.columns)]
    if valid_weights.sum() == 0:
        return pd.Series(dtype=float)
    normalized = valid_weights / valid_weights.sum()
    return pd.Series(aligned.values @ normalized, index=aligned.index, name="Portfolio")
