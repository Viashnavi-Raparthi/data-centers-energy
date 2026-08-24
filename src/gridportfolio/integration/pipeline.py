"""
Integration pipeline.

Connects fragmented source systems into a common portfolio context.

The integration layer preserves specialist ownership while creating
relationships across:

    Asset Management
          ↕
    Data & Analytics
          ↕
    Wholesale
          ↕
    Origination
          ↕
    Procurement
          ↕
    Initiatives
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from gridportfolio.integration.quality import (
    DataQualityResult,
    assess_all_sources,
)


@dataclass
class IntegratedPortfolio:
    """Integrated representation of the portfolio."""

    assets: pd.DataFrame
    forecasts: pd.DataFrame
    markets: pd.DataFrame
    contracts: pd.DataFrame
    procurement: pd.DataFrame
    initiatives: pd.DataFrame
    quality: dict[str, DataQualityResult]


def integrate_sources(
    sources: dict[str, pd.DataFrame],
) -> IntegratedPortfolio:
    """
    Integrate specialist datasets into a common portfolio structure.
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

    quality = assess_all_sources(sources)

    return IntegratedPortfolio(
        assets=sources["asset_management"].copy(),
        forecasts=sources["analytics"].copy(),
        markets=sources["wholesale"].copy(),
        contracts=sources["origination"].copy(),
        procurement=sources["procurement"].copy(),
        initiatives=sources["initiatives"].copy(),
        quality=quality,
    )


def build_cross_functional_view(
    portfolio: IntegratedPortfolio,
) -> pd.DataFrame:
    """
    Build a single cross-functional portfolio view.

    The output combines asset, forecast, market, contract,
    procurement, and initiative context.
    """

    # ============================================================
    # 1. Latest asset observation
    # ============================================================

    assets = portfolio.assets.copy()

    if "observation_time" in assets.columns:
        assets = (
            assets
            .sort_values("observation_time")
            .groupby("asset_code", as_index=False)
            .tail(1)
        )

    # ============================================================
    # 2. Latest forecast for each asset
    # ============================================================

    forecasts = portfolio.forecasts.copy()

    if "forecast_date" in forecasts.columns:
        forecasts = (
            forecasts
            .sort_values("forecast_date")
            .groupby("asset_code", as_index=False)
            .tail(1)
        )

    forecast_columns = [
        column
        for column in [
            "asset_code",
            "predicted_load_mw",
            "forecast_lower_mw",
            "forecast_upper_mw",
            "forecast_error_pct",
            "confidence",
            "model_name",
            "model_version",
        ]
        if column in forecasts.columns
    ]

    view = assets.merge(
        forecasts[forecast_columns],
        on="asset_code",
        how="left",
    )

    # ============================================================
    # 3. Map assets to markets
    # ============================================================

    asset_market = {
        "DC-001": "WEST",
        "DC-002": "EAST",
        "DC-003": "CENTRAL",
        "DC-004": "WEST",
        "DC-005": "EAST",
    }

    view["market_code"] = (
        view["asset_code"]
        .map(asset_market)
    )

    # ============================================================
    # 4. Latest wholesale observation by market
    # ============================================================

    markets = portfolio.markets.copy()

    if "observation_time" in markets.columns:
        markets = (
            markets
            .sort_values("observation_time")
            .groupby("market_code", as_index=False)
            .tail(1)
        )

    market_columns = [
        column
        for column in [
            "market_code",
            "market_name",
            "region",
            "real_time_price_usd_mwh",
            "day_ahead_price_usd_mwh",
            "price_volatility",
            "exposure_mw",
        ]
        if column in markets.columns
    ]

    view = view.merge(
        markets[market_columns],
        on="market_code",
        how="left",
        suffixes=("", "_market"),
    )

    # ============================================================
    # 5. Contract context
    # ============================================================

    contracts = portfolio.contracts.copy()

    if not contracts.empty and "asset_code" in contracts.columns:

        contract_summary = (
            contracts
            .groupby("asset_code")
            .agg(
                contract_count=(
                    "contract_code",
                    "count",
                ),
                contracted_mw=(
                    "contracted_mw",
                    "sum",
                ),
                average_contract_price_usd_mwh=(
                    "contract_price_usd_mwh",
                    "mean",
                ),
                renewable_contract_count=(
                    "renewable_flag",
                    "sum",
                ),
            )
            .reset_index()
        )

        view = view.merge(
            contract_summary,
            on="asset_code",
            how="left",
        )

    # ============================================================
    # 6. Procurement context
    # ============================================================
    #
    # Procurement opportunities are portfolio-level rather than
    # asset-level in the current demo schema.
    #
    # Therefore preserve them as portfolio-level context rather
    # than forcing an incorrect asset join.
    # ============================================================

    procurement = portfolio.procurement.copy()

    if not procurement.empty:

        procurement_summary: dict[str, object] = {
            "procurement_opportunity_count": len(procurement),
        }

        if "required_mw" in procurement.columns:
            procurement_summary["procurement_required_mw"] = (
                procurement["required_mw"].sum()
            )

        if "estimated_value_usd" in procurement.columns:
            procurement_summary["procurement_estimated_value_usd"] = (
                procurement["estimated_value_usd"].sum()
            )

        if "blocker" in procurement.columns:
            procurement_summary["procurement_blocker_count"] = int(
                procurement["blocker"]
                .notna()
                .sum()
            )

        if "procurement_stage" in procurement.columns:
            procurement_summary["procurement_active_count"] = int(
                procurement["procurement_stage"]
                .notna()
                .sum()
            )

        for column, value in procurement_summary.items():
            view[column] = value

    # ============================================================
    # 7. Initiative context
    # ============================================================

    initiatives = portfolio.initiatives.copy()

    if not initiatives.empty:

        initiative_summary: dict[str, object] = {
            "initiative_count": len(initiatives),
        }

        if "completion_pct" in initiatives.columns:
            initiative_summary[
                "average_initiative_completion_pct"
            ] = initiatives["completion_pct"].mean()

        if "dependency_count" in initiatives.columns:
            initiative_summary[
                "total_initiative_dependencies"
            ] = initiatives["dependency_count"].sum()

        if "blocker" in initiatives.columns:
            initiative_summary[
                "initiative_blocker_count"
            ] = int(
                initiatives["blocker"]
                .notna()
                .sum()
            )

        if "priority" in initiatives.columns:
            initiative_summary[
                "high_priority_initiative_count"
            ] = int(
                initiatives["priority"]
                .astype(str)
                .str.lower()
                .isin(["high", "critical"])
                .sum()
            )

        for column, value in initiative_summary.items():
            view[column] = value

    return view