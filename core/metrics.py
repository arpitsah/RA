from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def compute_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change().dropna(how="all")


def equity_curve(returns: pd.DataFrame) -> pd.DataFrame:
    return (1 + returns).cumprod()


def drawdown_curve(eq_curve: pd.DataFrame) -> pd.DataFrame:
    running_max = eq_curve.cummax()
    return eq_curve / running_max - 1


def annualized_return(returns: pd.Series) -> float:
    compounded = (1 + returns).prod()
    years = len(returns) / TRADING_DAYS
    return compounded ** (1 / years) - 1 if years > 0 else 0.0


def annualized_volatility(returns: pd.Series) -> float:
    return returns.std(ddof=1) * np.sqrt(TRADING_DAYS)


def sharpe_ratio(returns: pd.Series, rf: float = 0.0) -> float:
    excess = returns - rf / TRADING_DAYS
    vol = annualized_volatility(excess)
    if vol == 0:
        return 0.0
    return annualized_return(excess) / vol


def sortino_ratio(returns: pd.Series, rf: float = 0.0) -> float:
    excess = returns - rf / TRADING_DAYS
    downside = excess[excess < 0]
    downside_dev = downside.std(ddof=1) * np.sqrt(TRADING_DAYS) if not downside.empty else 0.0
    if downside_dev == 0:
        return 0.0
    return annualized_return(excess) / downside_dev


def max_drawdown(returns: pd.Series) -> float:
    dd = drawdown_curve(equity_curve(returns.to_frame("x")))["x"]
    return float(dd.min())


def calmar_ratio(returns: pd.Series) -> float:
    mdd = abs(max_drawdown(returns))
    if mdd == 0:
        return 0.0
    return annualized_return(returns) / mdd


def beta_alpha(asset: pd.Series, benchmark: pd.Series) -> tuple[float, float]:
    aligned = pd.concat([asset, benchmark], axis=1).dropna()
    if aligned.empty:
        return 0.0, 0.0
    x = aligned.iloc[:, 1]
    y = aligned.iloc[:, 0]
    beta = np.cov(y, x)[0, 1] / np.var(x) if np.var(x) != 0 else 0.0
    alpha_daily = y.mean() - beta * x.mean()
    return float(beta), float(alpha_daily * TRADING_DAYS)


def metrics_table(returns: pd.DataFrame, benchmark_col: str | None = None) -> pd.DataFrame:
    rows = {}
    benchmark = returns[benchmark_col] if benchmark_col and benchmark_col in returns else None
    for col in returns.columns:
        series = returns[col].dropna()
        b, a = beta_alpha(series, benchmark) if benchmark is not None and col != benchmark_col else (0.0, 0.0)
        rows[col] = {
            "CAGR": annualized_return(series),
            "Volatility": annualized_volatility(series),
            "Sharpe": sharpe_ratio(series),
            "Sortino": sortino_ratio(series),
            "Max Drawdown": max_drawdown(series),
            "Calmar": calmar_ratio(series),
            "Beta": b,
            "Alpha": a,
        }
    return pd.DataFrame(rows).T


def rolling_correlation(returns: pd.DataFrame, left: str, right: str, window: int = 63) -> pd.DataFrame:
    df = returns[[left, right]].dropna()
    rolling = df[left].rolling(window=window).corr(df[right])
    return rolling.to_frame(name=f"{left} vs {right}")
