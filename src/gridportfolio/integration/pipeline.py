"""
Integration pipeline.

This is the central connective-tissue component.

It takes fragmented source systems and creates a common portfolio
context.

The pipeline does not attempt to eliminate specialist ownership.

Instead it creates relationships between their outputs.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from gridportfolio.integration.quality import (
    QualityResult,
    assess_all_sources,
)


@dataclass
class IntegratedPortfolio:
    """
    Integrated representation of the fragmented organization.
    """

    assets: pd.DataFrame
    forecasts: pd.DataFrame
    markets: pd.DataFrame
    contracts: pd.DataFrame
    procurement: pd.DataFrame
    initiatives: pd.DataFrame
    quality: list[QualityResult]


def integrate_sources(
    sources: dict[str, pd.DataFrame],
) -> IntegratedPortfolio:
    """
    Integrate specialist datasets.

    The joins are intentionally explicit.

    These relationships are the core of the project:

        asset
          ↕
        forecast
          ↕
        market
          ↕
        contract
          ↕
        procurement
          ↕
        initiative
    """

    required = {
        "asset_management",
        "analytics",
        "wholesale",
        "origination",
        "procurement",
        "initiatives",
    }

    missing = required - set(sources)

    if missing:
        raise ValueError(
            f"Missing required source datasets: {sorted(missing)}"
        )

    assets = sources["asset_management"].copy()

    forecasts = sources["analytics"].copy()

    markets = sources["wholesale"].copy()

    contracts = sources["origination"].copy()

    procurement = sources["procurement"].copy()

    initiatives = sources["initiatives"].copy()

    quality = assess_all_sources(sources)

    return IntegratedPortfolio(
        assets=assets,
        forecasts=forecasts,
        markets=markets,
        contracts=contracts,
        procurement=procurement,
        initiatives=initiatives,
        quality=quality,
    )


def build_cross_functional_view(
    portfolio: IntegratedPortfolio,
) -> pd.DataFrame:
    """
    Build the central cross-functional table.

    This is where separate team outputs become one business view.

    Each row connects:

        asset
        forecast
        market
        contract
        procurement
        initiative
    """

    assets = (
        portfolio.assets
        .sort_values("observation_time")
        .groupby("asset_code")
        .tail(1)
    )

    forecasts = (
        portfolio.forecasts
        .sort_values("forecast_date")
        .groupby("asset_code")
        .tail(1)
    )

    markets = (
        portfolio.markets
        .sort_values("observation_time")
        .groupby("market_code")
        .tail(1)
    )

    contracts = portfolio.contracts.copy()

    view = assets.merge(
        forecasts[
            [
                "asset_code",
                "predicted_load_mw",
                "forecast_error_pct",
                "confidence",
            ]
        ],
        on="asset_code",
        how="left",
    )

    asset_market = {
        "DC-001": "WEST",
        "DC-002": "WEST",
        "DC-003": "ERCOT",
        "DC-004": "SOUTHEAST",
    }

    view["market_code"] = view["asset_code"].map(
        asset_market,
    )

    view = view.merge(
        markets[
            [
                "market_code",
                "real_time_price_usd_mwh",
                "price_volatility",
                "exposure_mw",
            ]
        ],
        on="market_code",
        how="left",
    )

    view = view.merge(
        contracts[
            [
                "contract_code",
                "asset_code",
                "contracted_mw",
                "contract_price_usd_mwh",
                "expiration_date",
                "renewable_flag",
                "contract_status",
            ]
        ],
        on="asset_code",
        how="left",
    )

    return view