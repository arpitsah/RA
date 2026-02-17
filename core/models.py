from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import pandas as pd


@dataclass(slots=True)
class Recommendation:
    title: str
    trigger_metrics: dict[str, float]
    recommendation_steps: list[str]
    expected_impact: str
    confidence: float
    reasoning: str


@dataclass(slots=True)
class Report:
    name: str
    tickers: list[str]
    benchmark: str
    start_date: date
    end_date: date
    frequency: str
    metrics_table: pd.DataFrame
    returns: pd.DataFrame
    equity_curve: pd.DataFrame
    drawdown_curve: pd.DataFrame
    correlation_matrix: pd.DataFrame
    rolling_correlation: pd.DataFrame
    beta_alpha: pd.DataFrame
    recommendations: list[Recommendation] = field(default_factory=list)
