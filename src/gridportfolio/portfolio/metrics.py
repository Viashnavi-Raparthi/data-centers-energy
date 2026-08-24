"""
Portfolio metrics.

Provides normalized metrics used by the portfolio, signal, agent,
and governance layers.
"""

from __future__ import annotations

import pandas as pd


def _first_existing(
    dataframe: pd.DataFrame,
    columns: list[str],
    default: object = None,
) -> pd.Series:
    """Return the first existing column, or a default Series."""
    for column in columns:
        if column in dataframe.columns:
            return dataframe[column]

    return pd.Series(
        [default] * len(dataframe),
        index=dataframe.index,
    )


def _numeric(
    series: pd.Series,
    default: float = 0.0,
) -> pd.Series:
    """Safely convert a Series to numeric."""
    return pd.to_numeric(
        series,
        errors="coerce",
    ).fillna(default)


def forecast_uncertainty(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Estimate forecast uncertainty.

    Returns a value from 0 to 1.
    Higher values indicate greater uncertainty.
    """
    confidence = _numeric(
        _first_existing(
            dataframe,
            ["confidence"],
        )
    )

    error = _numeric(
        _first_existing(
            dataframe,
            ["forecast_error_pct"],
        )
    ).abs()

    confidence_normalized = confidence.clip(
        lower=0.0,
        upper=1.0,
    )

    error_normalized = (
        error
        .div(100.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )

    return (
        (1.0 - confidence_normalized) * 0.50
        + error_normalized * 0.50
    ).clip(
        lower=0.0,
        upper=1.0,
    )


def contract_expiration_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate contract expiration risk.

    Higher values indicate contracts that are closer to expiration.
    """
    if dataframe.empty:
        return pd.Series(
            dtype=float,
            index=dataframe.index,
        )

    expiration = pd.to_datetime(
        _first_existing(
            dataframe,
            ["expiration_date"],
        ),
        errors="coerce",
    )

    today = pd.Timestamp.today().normalize()

    days_remaining = (
        expiration - today
    ).dt.days

    risk = pd.Series(
        0.0,
        index=dataframe.index,
        dtype=float,
    )

    valid = days_remaining.notna()

    risk.loc[
        valid & (days_remaining <= 0)
    ] = 1.0

    risk.loc[
        valid
        & (days_remaining > 0)
        & (days_remaining <= 30)
    ] = 0.9

    risk.loc[
        valid
        & (days_remaining > 30)
        & (days_remaining <= 90)
    ] = 0.7

    risk.loc[
        valid
        & (days_remaining > 90)
        & (days_remaining <= 180)
    ] = 0.4

    risk.loc[
        valid & (days_remaining > 180)
    ] = 0.1

    return risk


def forecast_error_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """Normalize forecast error into a 0-1 risk score."""
    error = _numeric(
        _first_existing(
            dataframe,
            ["forecast_error_pct"],
        )
    ).abs()

    return (
        error
        .div(100.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def market_volatility_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """Normalize market volatility into a 0-1 risk score."""
    volatility = _numeric(
        _first_existing(
            dataframe,
            [
                "price_volatility",
                "volatility",
            ],
        )
    ).abs()

    return (
        volatility
        .div(100.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def market_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Backward-compatible market risk metric.

    Market risk is represented by normalized price volatility.
    """
    return market_volatility_risk(dataframe)


def contract_coverage(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate contracted capacity as a 0-1 coverage ratio.
    """
    contracted = _numeric(
        _first_existing(
            dataframe,
            ["contracted_mw"],
        )
    )

    capacity = _numeric(
        _first_existing(
            dataframe,
            ["installed_capacity_mw"],
        )
    )

    return (
        contracted
        .div(
            capacity.replace(0, pd.NA)
        )
        .fillna(0.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def renewable_coverage(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate renewable contract coverage.

    If renewable capacity is explicitly available, use it.
    Otherwise use contracted capacity for rows marked renewable.
    """
    capacity = _numeric(
        _first_existing(
            dataframe,
            ["installed_capacity_mw"],
        )
    )

    renewable_capacity = _numeric(
        _first_existing(
            dataframe,
            [
                "renewable_capacity_mw",
                "renewable_contracted_mw",
            ],
        )
    )

    renewable_flag = _first_existing(
        dataframe,
        ["renewable_flag"],
        False,
    )

    renewable_flag = (
        renewable_flag
        .astype(str)
        .str.lower()
        .isin(
            [
                "true",
                "1",
                "yes",
                "y",
            ]
        )
    )

    contracted = _numeric(
        _first_existing(
            dataframe,
            ["contracted_mw"],
        )
    )

    fallback_renewable = contracted.where(
        renewable_flag,
        0.0,
    )

    renewable_capacity = renewable_capacity.where(
        renewable_capacity.ne(0),
        fallback_renewable,
    )

    return (
        renewable_capacity
        .div(
            capacity.replace(0, pd.NA)
        )
        .fillna(0.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def build_metric_table(
    cross_functional: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the normalized portfolio metric table.

    This function intentionally creates both the newer metric names
    and backward-compatible aliases expected by downstream modules.
    """
    result = cross_functional.copy()

    # ---------------------------------------------------------------
    # Identity
    # ---------------------------------------------------------------

    result["asset_code"] = _first_existing(
        result,
        ["asset_code"],
    )

    result["asset_name"] = _first_existing(
        result,
        ["asset_name"],
    )

    result["region"] = _first_existing(
        result,
        ["region"],
    )

    # ---------------------------------------------------------------
    # Load / capacity
    # ---------------------------------------------------------------

    result["installed_capacity_mw"] = _numeric(
        _first_existing(
            result,
            ["installed_capacity_mw"],
        )
    )

    result["current_load_mw"] = _numeric(
        _first_existing(
            result,
            ["current_load_mw"],
        )
    )

    result["forecast_load_mw"] = _numeric(
        _first_existing(
            result,
            [
                "forecast_load_mw",
                "predicted_load_mw",
            ],
        )
    )

    result["predicted_load_mw"] = _numeric(
        _first_existing(
            result,
            [
                "predicted_load_mw",
                "forecast_load_mw",
            ],
        )
    )

    # ---------------------------------------------------------------
    # Forecast
    # ---------------------------------------------------------------

    result["forecast_error_pct"] = _numeric(
        _first_existing(
            result,
            ["forecast_error_pct"],
        )
    )

    result["confidence"] = _numeric(
        _first_existing(
            result,
            ["confidence"],
        )
    )

    # ---------------------------------------------------------------
    # Wholesale / market
    # ---------------------------------------------------------------

    result["real_time_price_usd_mwh"] = _numeric(
        _first_existing(
            result,
            [
                "real_time_price_usd_mwh",
                "price_mwh",
            ],
        )
    )

    result["day_ahead_price_usd_mwh"] = _numeric(
        _first_existing(
            result,
            ["day_ahead_price_usd_mwh"],
        )
    )

    result["price_volatility"] = _numeric(
        _first_existing(
            result,
            [
                "price_volatility",
                "volatility",
            ],
        )
    )

    # Backward-compatible aliases.
    result["price_mwh"] = result[
        "real_time_price_usd_mwh"
    ]

    result["volatility"] = result[
        "price_volatility"
    ]

    result["exposure_mw"] = _numeric(
        _first_existing(
            result,
            ["exposure_mw"],
        )
    )

    # ---------------------------------------------------------------
    # Contracts
    # ---------------------------------------------------------------

    result["contract_code"] = _first_existing(
        result,
        ["contract_code"],
    )

    result["contract_type"] = _first_existing(
        result,
        ["contract_type"],
    )

    result["contracted_mw"] = _numeric(
        _first_existing(
            result,
            ["contracted_mw"],
        )
    )

    result["contract_price_usd_mwh"] = _numeric(
        _first_existing(
            result,
            ["contract_price_usd_mwh"],
        )
    )

    result["renewable_flag"] = _first_existing(
        result,
        ["renewable_flag"],
        False,
    )

    result["start_date"] = _first_existing(
        result,
        ["start_date"],
    )

    result["expiration_date"] = _first_existing(
        result,
        ["expiration_date"],
    )

    result["contract_status"] = _first_existing(
        result,
        ["contract_status"],
    )

    # ---------------------------------------------------------------
    # Procurement
    # ---------------------------------------------------------------

    result["opportunity_code"] = _first_existing(
        result,
        ["opportunity_code"],
    )

    result["required_mw"] = _numeric(
        _first_existing(
            result,
            ["required_mw"],
        )
    )

    result["procurement_stage"] = _first_existing(
        result,
        ["procurement_stage"],
    )

    result["expected_price_usd_mwh"] = _numeric(
        _first_existing(
            result,
            ["expected_price_usd_mwh"],
        )
    )

    result["estimated_value_usd"] = _numeric(
        _first_existing(
            result,
            ["estimated_value_usd"],
        )
    )

    result["procurement_blocker"] = _first_existing(
        result,
        ["blocker"],
    )

    # ---------------------------------------------------------------
    # Derived utilization
    # ---------------------------------------------------------------

    capacity = result["installed_capacity_mw"]

    result["current_utilization_pct"] = (
        result["current_load_mw"]
        .div(
            capacity.replace(0, pd.NA)
        )
        .fillna(0.0)
        * 100.0
    )

    result["forecast_utilization_pct"] = (
        result["predicted_load_mw"]
        .div(
            capacity.replace(0, pd.NA)
        )
        .fillna(0.0)
        * 100.0
    )

    result["contract_coverage_pct"] = (
        result["contracted_mw"]
        .div(
            capacity.replace(0, pd.NA)
        )
        .fillna(0.0)
        * 100.0
    )

    # ---------------------------------------------------------------
    # Risk
    # ---------------------------------------------------------------

    result["market_volatility_risk"] = (
        market_volatility_risk(result)
    )

    result["market_risk"] = (
        market_risk(result)
    )

    result["market_risk_score"] = (
        result["market_risk"]
    )

    result["forecast_error_risk"] = (
        forecast_error_risk(result)
    )

    result["forecast_risk_score"] = (
        result["forecast_error_risk"]
    )

    result["forecast_uncertainty"] = (
        forecast_uncertainty(result)
    )

    result["contract_expiration_risk"] = (
        contract_expiration_risk(result)
    )

    result["contract_coverage"] = (
        contract_coverage(result)
    )

    result["renewable_coverage"] = (
        renewable_coverage(result)
    )

    # Overall risk combines the major risk dimensions.
    result["overall_risk_score"] = (
        result["market_risk"] * 0.40
        + result["forecast_error_risk"] * 0.30
        + result["contract_expiration_risk"] * 0.20
        + result["forecast_uncertainty"] * 0.10
    ).clip(
        lower=0.0,
        upper=1.0,
    )

    return result


__all__ = [
    "build_metric_table",
    "forecast_uncertainty",
    "contract_expiration_risk",
    "forecast_error_risk",
    "market_volatility_risk",
    "market_risk",
    "contract_coverage",
    "renewable_coverage",
]
