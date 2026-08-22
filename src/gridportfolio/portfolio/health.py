"""
Portfolio health calculation.

Portfolio health is deliberately decomposable.

A leadership score should explain itself.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class PortfolioHealthResult:
    overall_score: float
    renewable_coverage_score: float
    forecast_stability_score: float
    market_exposure_score: float
    contract_coverage_score: float
    execution_health_score: float
    explanation: str


def calculate_portfolio_health(
    metrics: pd.DataFrame,
) -> PortfolioHealthResult:
    """
    Calculate an interpretable portfolio-health score.
    """

    if metrics.empty:
        return PortfolioHealthResult(
            overall_score=0,
            renewable_coverage_score=0,
            forecast_stability_score=0,
            market_exposure_score=0,
            contract_coverage_score=0,
            execution_health_score=0,
            explanation="No portfolio data available.",
        )

    renewable = (
        metrics["renewable_coverage"].mean()
        * 100
    )

    forecast = (
        1
        - metrics["forecast_uncertainty"].mean()
    ) * 100

    market = (
        1
        - metrics["market_risk"].mean()
    ) * 100

    contract = (
        1
        - metrics["contract_expiration_risk"].mean()
    ) * 100

    execution = 75.0

    overall = (
        renewable * 0.25
        + forecast * 0.15
        + market * 0.20
        + contract * 0.25
        + execution * 0.15
    )

    explanation = (
        f"Portfolio health is {overall:.1f}/100. "
        f"Contract coverage contributes {contract:.1f}, "
        f"market conditions contribute {market:.1f}, "
        f"forecast stability contributes {forecast:.1f}, "
        f"and renewable coverage contributes {renewable:.1f}."
    )

    return PortfolioHealthResult(
        overall_score=overall,
        renewable_coverage_score=renewable,
        forecast_stability_score=forecast,
        market_exposure_score=market,
        contract_coverage_score=contract,
        execution_health_score=execution,
        explanation=explanation,
    )