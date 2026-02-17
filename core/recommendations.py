from __future__ import annotations

from core.models import Recommendation


def generate_recommendations(
    max_dd: float,
    volatility: float,
    top_weight: float,
    avg_corr: float,
    relative_cagr: float,
) -> list[Recommendation]:
    recs: list[Recommendation] = []

    if max_dd < -0.25:
        recs.append(
            Recommendation(
                title="Drawdown Risk Too High",
                trigger_metrics={"max_drawdown": max_dd},
                recommendation_steps=[
                    "Reduce cyclical exposure by 10-20%.",
                    "Add defensive ETF sleeve (e.g., utilities/treasuries).",
                ],
                expected_impact="Potentially reduce future max drawdown by 5-10%.",
                confidence=0.74,
                reasoning="Historical drawdowns beyond -25% indicate poor downside resilience.",
            )
        )

    if volatility > 0.25:
        recs.append(
            Recommendation(
                title="Volatility Above Target",
                trigger_metrics={"volatility": volatility},
                recommendation_steps=[
                    "Increase low-volatility assets.",
                    "Introduce simple volatility caps or risk parity weights.",
                ],
                expected_impact="Could lower annualized volatility by 3-6%.",
                confidence=0.68,
                reasoning="Annualized volatility exceeds common balanced portfolio targets.",
            )
        )

    if top_weight > 0.35:
        recs.append(
            Recommendation(
                title="Concentration Risk",
                trigger_metrics={"top_weight": top_weight},
                recommendation_steps=[
                    "Cap single-position exposure to 20-25%.",
                    "Reallocate excess to uncorrelated sectors.",
                ],
                expected_impact="Expected to improve diversification and smooth returns.",
                confidence=0.8,
                reasoning="Single holding dominates total portfolio risk contribution.",
            )
        )

    if avg_corr > 0.75:
        recs.append(
            Recommendation(
                title="High Intra-Portfolio Correlation",
                trigger_metrics={"average_correlation": avg_corr},
                recommendation_steps=[
                    "Add assets with distinct return drivers.",
                    "Consider bonds/commodities/market-neutral allocation.",
                ],
                expected_impact="Diversification benefit may cut drawdowns in stress periods.",
                confidence=0.65,
                reasoning="Current holdings likely move together under risk-off conditions.",
            )
        )

    if relative_cagr < -0.03:
        recs.append(
            Recommendation(
                title="Persistent Benchmark Underperformance",
                trigger_metrics={"relative_cagr": relative_cagr},
                recommendation_steps=[
                    "Review alpha thesis for each active position.",
                    "Shift portion to low-cost benchmark exposure.",
                ],
                expected_impact="Could improve risk-adjusted return and reduce fee drag.",
                confidence=0.71,
                reasoning="Portfolio CAGR trails benchmark by a material margin.",
            )
        )

    return recs
