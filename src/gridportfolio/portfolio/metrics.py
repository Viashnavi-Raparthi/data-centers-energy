"""
Canonical portfolio metrics.

These metrics provide a shared vocabulary for leadership and
specialist teams.
"""

from __future__ import annotations

import pandas as pd


def renewable_coverage(
    contracted_mw: float,
    load_mw: float,
) -> float:
    """Percentage of load covered by renewable contracts."""

    if load_mw <= 0:
        return 1.0

    return min(
        1.0,
        contracted_mw / load_mw,
    )


def forecast_uncertainty(
    forecast_error_pct: float,
) -> float:
    """
    Normalize forecast error into a 0-1 uncertainty score.
    """

    return min(
        1.0,
        abs(forecast_error_pct) / 20.0,
    )


def market_risk(
    volatility: float,
) -> float:
    """
    Normalize market volatility into a 0-1 risk score.
    """

    return min(
        1.0,
        volatility / 0.50,
    )


def contract_expiration_risk(
    days_to_expiration: int,
) -> float:
    """Risk increases as contract expiration approaches."""

    if days_to_expiration <= 0:
        return 1.0

    if days_to_expiration >= 365:
        return 0.0

    return max(
        0.0,
        1 - days_to_expiration / 365,
    )


def execution_risk(
    initiative_status: str,
    completion_pct: float,
    blocker: str | None,
) -> float:
    """Estimate execution risk."""

    risk = 0.0

    if initiative_status in {"at_risk", "blocked"}:
        risk += 0.45

    if blocker:
        risk += 0.35

    if completion_pct < 50:
        risk += 0.20

    return min(
        1.0,
        risk,
    )


def build_metric_table(
    cross_functional_view: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate canonical metrics for each asset."""

    result = cross_functional_view.copy()

    today = pd.Timestamp.today().normalize()

    result["days_to_contract_expiration"] = (
        pd.to_datetime(
            result["expiration_date"],
        ) - today
    ).dt.days

    result["renewable_coverage"] = (
        result["contracted_mw"]
        / result["current_load_mw"].clip(lower=1)
    ).clip(
        upper=1.0,
    )

    result["forecast_uncertainty"] = (
        result["forecast_error_pct"]
        .abs()
        / 20
    ).clip(
        upper=1.0,
    )

    result["market_risk"] = (
        result["price_volatility"]
        / 0.50
    ).clip(
        upper=1.0,
    )

    result["contract_expiration_risk"] = (
        result["days_to_contract_expiration"]
        .apply(contract_expiration_risk)
    )

    return result