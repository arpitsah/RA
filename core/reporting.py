from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

from core.metrics import (
    compute_returns,
    drawdown_curve,
    equity_curve,
    metrics_table,
    rolling_correlation,
)
from core.models import Report
from core.recommendations import generate_recommendations


def build_report(
    prices: pd.DataFrame,
    name: str,
    benchmark: str,
    frequency: str,
    start_date: date,
    end_date: date,
) -> Report:
    rets = compute_returns(prices)
    eq = equity_curve(rets)
    dd = drawdown_curve(eq)
    metrics = metrics_table(rets, benchmark_col=benchmark if benchmark in rets.columns else None)
    corr = rets.corr()

    if len(rets.columns) >= 2:
        rolling = rolling_correlation(rets, rets.columns[0], rets.columns[1])
    else:
        rolling = pd.DataFrame()

    top_weight_proxy = 1 / len(rets.columns) if len(rets.columns) else 1.0
    avg_corr = float(corr.where(~np.eye(corr.shape[0], dtype=bool)).stack().mean()) if len(corr) > 1 else 0.0
    relative_cagr = 0.0
    if benchmark in metrics.index and name in metrics.index:
        relative_cagr = float(metrics.loc[name, "CAGR"] - metrics.loc[benchmark, "CAGR"])

    recommendations = generate_recommendations(
        max_dd=float(metrics["Max Drawdown"].min()) if not metrics.empty else 0.0,
        volatility=float(metrics["Volatility"].max()) if not metrics.empty else 0.0,
        top_weight=top_weight_proxy,
        avg_corr=avg_corr,
        relative_cagr=relative_cagr,
    )

    beta_alpha = metrics[["Beta", "Alpha"]].copy() if not metrics.empty else pd.DataFrame()

    return Report(
        name=name,
        tickers=list(prices.columns),
        benchmark=benchmark,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        metrics_table=metrics,
        returns=rets,
        equity_curve=eq,
        drawdown_curve=dd,
        correlation_matrix=corr,
        rolling_correlation=rolling,
        beta_alpha=beta_alpha,
        recommendations=recommendations,
    )
