from __future__ import annotations

import numpy as np
import pandas as pd

from core.metrics import compute_returns, metrics_table
from core.portfolio import validate_weights


def test_compute_returns_shape() -> None:
    prices = pd.DataFrame({"A": [100, 110, 121], "B": [100, 100, 105]})
    returns = compute_returns(prices)
    assert returns.shape == (2, 2)


def test_metrics_table_contains_required_columns() -> None:
    rng = np.random.default_rng(0)
    returns = pd.DataFrame(
        {
            "Portfolio": rng.normal(0.0005, 0.01, size=300),
            "SPY": rng.normal(0.0004, 0.009, size=300),
        }
    )
    table = metrics_table(returns, benchmark_col="SPY")
    assert {"CAGR", "Volatility", "Sharpe", "Sortino", "Max Drawdown", "Calmar", "Beta", "Alpha"}.issubset(
        table.columns
    )


def test_validate_weights() -> None:
    good = pd.DataFrame({"ticker": ["AAPL", "MSFT"], "weight": [0.5, 0.5]})
    ok, _ = validate_weights(good)
    assert ok

    bad = pd.DataFrame({"ticker": ["AAPL", "MSFT"], "weight": [0.7, 0.5]})
    ok, msg = validate_weights(bad)
    assert not ok
    assert "sum" in msg.lower()
