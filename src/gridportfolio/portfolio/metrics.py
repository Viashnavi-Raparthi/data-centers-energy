"""
Canonical portfolio metrics.

This module converts the integrated cross-functional portfolio view
into a stable metric table consumed by:

    - portfolio health
    - signal detection
    - risk identification
    - executive agents

The key design principle is that downstream layers should depend on
these canonical metric names rather than raw source-system fields.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


def _first_existing(
    dataframe: pd.DataFrame,
    columns: Iterable[str],
) -> pd.Series:
    """Return the first available column, or an all-NaN series."""

    for column in columns:
        if column in dataframe.columns:
            return dataframe[column]

    return pd.Series(
        np.nan,
        index=dataframe.index,
        dtype=float,
    )


def _numeric(
    series: pd.Series,
) -> pd.Series:
    """Convert a series to numeric values safely."""

    return pd.to_numeric(
        series,
        errors="coerce",
    )


def _fill_zero(
    series: pd.Series,
) -> pd.Series:
    """Convert numeric values and replace missing values with zero."""

    return _numeric(series).fillna(0.0)


def forecast_uncertainty(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate normalized forecast uncertainty.

    Preferred source:
        forecast_upper_mw - forecast_lower_mw

    The range is normalized against forecast load so that uncertainty
    is comparable across data centers of different sizes.
    """

    upper = _numeric(
        _first_existing(
            dataframe,
            [
                "forecast_upper_mw",
                "upper_forecast_mw",
            ],
        )
    )

    lower = _numeric(
        _first_existing(
            dataframe,
            [
                "forecast_lower_mw",
                "lower_forecast_mw",
            ],
        )
    )

    forecast = _numeric(
        _first_existing(
            dataframe,
            [
                "forecast_load_mw",
                "predicted_load_mw",
            ],
        )
    )

    denominator = forecast.abs().replace(
        0,
        np.nan,
    )

    uncertainty = (
        (upper - lower)
        .abs()
        .div(denominator)
    )

    return uncertainty.fillna(0.0).clip(
        lower=0.0,
        upper=1.0,
    )


def forecast_error_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """Calculate normalized forecast-error risk."""

    error = _numeric(
        _first_existing(
            dataframe,
            [
                "forecast_error_pct",
                "forecast_error",
            ],
        )
    ).abs()

    # Forecast error is expressed as a percentage.
    # 25% error or higher is treated as maximum risk.
    return (
        error
        .div(25.0)
        .fillna(0.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )


def market_volatility_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate normalized market-volatility risk.

    Synthetic data in this project represents volatility on a
    0-to-1 scale, so 0.38 means 38% volatility.
    """

    volatility = _numeric(
        _first_existing(
            dataframe,
            [
                "price_volatility",
                "market_volatility",
                "volatility",
            ],
        )
    ).abs()

    return volatility.fillna(0.0).clip(
        lower=0.0,
        upper=1.0,
    )


def market_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate canonical market risk.

    For now, market risk is represented by market volatility.
    This intentionally provides a stable downstream interface that
    can later incorporate price exposure, basis risk, or market
    concentration.
    """

    volatility_risk = market_volatility_risk(
        dataframe,
    )

    return volatility_risk.clip(
        lower=0.0,
        upper=1.0,
    )


def contract_expiration_risk(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate contract-expiration risk.

    Risk increases as the number of days remaining decreases:

        <= 30 days   -> 1.00
        60 days      -> 0.75
        90 days      -> 0.50
        180 days     -> 0.00

    Missing expiration information produces zero risk rather than
    fabricating a date.
    """

    days = _numeric(
        _first_existing(
            dataframe,
            [
                "days_to_contract_expiration",
                "contract_days_remaining",
            ],
        )
    )

    risk = (
        (180.0 - days)
        .div(150.0)
    )

    return risk.fillna(0.0).clip(
        lower=0.0,
        upper=1.0,
    )


def contract_coverage(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate contract coverage as contracted MW / current load MW.
    """

    contracted = _numeric(
        _first_existing(
            dataframe,
            [
                "contracted_mw",
                "contracted_capacity_mw",
            ],
        )
    )

    load = _numeric(
        _first_existing(
            dataframe,
            [
                "current_load_mw",
                "load_mw",
            ],
        )
    )

    denominator = load.replace(
        0,
        np.nan,
    )

    coverage = contracted.div(
        denominator,
    )

    return coverage.fillna(0.0).clip(
        lower=0.0,
        upper=1.0,
    )


def renewable_coverage(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate renewable contract coverage.

    Renewable contracted MW is estimated from the proportion of
    renewable contracts when detailed renewable MW is unavailable.
    """

    contracted = _numeric(
        _first_existing(
            dataframe,
            [
                "contracted_mw",
                "contracted_capacity_mw",
            ],
        )
    ).fillna(0.0)

    renewable_count = _numeric(
        _first_existing(
            dataframe,
            [
                "renewable_contract_count",
            ],
        )
    ).fillna(0.0)

    contract_count = _numeric(
        _first_existing(
            dataframe,
            [
                "contract_count",
            ],
        )
    ).fillna(0.0)

    renewable_ratio = (
        renewable_count
        .div(
            contract_count.replace(
                0,
                np.nan,
            )
        )
        .fillna(0.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )

    renewable_mw = (
        contracted * renewable_ratio
    )

    load = _numeric(
        _first_existing(
            dataframe,
            [
                "current_load_mw",
                "load_mw",
            ],
        )
    )

    coverage = renewable_mw.div(
        load.replace(
            0,
            np.nan,
        )
    )

    return coverage.fillna(0.0).clip(
        lower=0.0,
        upper=1.0,
    )


def build_metric_table(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the canonical portfolio metric table.

    All downstream consumers should use the columns generated here.
    """

    result = dataframe.copy()

    # ---------------------------------------------------------------
    # Canonical risk metrics
    # ---------------------------------------------------------------

    result["forecast_uncertainty"] = (
        forecast_uncertainty(result)
    )

    result["forecast_error_risk"] = (
        forecast_error_risk(result)
    )

    result["market_volatility_risk"] = (
        market_volatility_risk(result)
    )

    result["market_risk"] = (
        market_risk(result)
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

    # ---------------------------------------------------------------
    # Derived operational fields
    # ---------------------------------------------------------------

    current_load = _numeric(
        _first_existing(
            result,
            ["current_load_mw"],
        )
    )

    forecast_load = _numeric(
        _first_existing(
            result,
            ["forecast_load_mw"],
        )
    )

    result["load_growth_pct"] = (
        forecast_load
        .sub(current_load)
        .div(
            current_load.replace(
                0,
                np.nan,
            )
        )
        .mul(100.0)
        .fillna(0.0)
    )

    result["load_growth_risk"] = (
        result["load_growth_pct"]
        .div(10.0)
        .clip(
            lower=0.0,
            upper=1.0,
        )
    )

    # ---------------------------------------------------------------
    # Combined procurement exposure
    # ---------------------------------------------------------------

    result["procurement_exposure_risk"] = (
        result["forecast_uncertainty"] * 0.25
        + result["market_risk"] * 0.25
        + result["contract_expiration_risk"] * 0.30
        + result["load_growth_risk"] * 0.20
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