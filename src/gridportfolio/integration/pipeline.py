"""
Integration layer for GridPortfolio.

Combines fragmented source systems into a canonical,
cross-functional portfolio view.

The integration layer preserves the fields needed by downstream
portfolio metrics, signal detection, risk analysis, and the
executive decision layer.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from gridportfolio.data.generators import generate_all_sources
from gridportfolio.integration.quality import (
    DataQualityResult,
    assess_all_sources,
)


@dataclass
class IntegratedPortfolio:
    """Container for integrated source-system data."""

    assets: pd.DataFrame
    forecasts: pd.DataFrame
    markets: pd.DataFrame
    contracts: pd.DataFrame
    procurement: pd.DataFrame
    initiatives: pd.DataFrame
    quality: list[DataQualityResult]


def integrate_sources(
    sources: dict[str, pd.DataFrame],
) -> IntegratedPortfolio:
    """
    Integrate fragmented source systems into a common portfolio object.
    """

    quality_results = assess_all_sources(sources)

    quality = list(quality_results.values())

    return IntegratedPortfolio(
        assets=sources["asset_management"].copy(),
        forecasts=sources["analytics"].copy(),
        markets=sources["wholesale"].copy(),
        contracts=sources["origination"].copy(),
        procurement=sources["procurement"].copy(),
        initiatives=sources["initiatives"].copy(),
        quality=quality,
    )


def _aggregate_contracts(
    contracts: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate contract-level information to the asset level.

    The source Origination data identifies renewable contracts using
    ``contract_type`` rather than a boolean ``renewable_contract`` field.

    This function derives the renewable-contract indicator while
    preserving the earliest expiration date for downstream
    contract-expiration risk calculations.
    """

    if contracts.empty:
        return pd.DataFrame()

    required = {
        "asset_code",
        "contract_code",
        "contracted_mw",
        "contract_price_usd_mwh",
        "contract_type",
        "expiration_date",
    }

    missing = required - set(contracts.columns)

    if missing:
        raise ValueError(
            "Origination contract data is missing required columns: "
            f"{sorted(missing)}"
        )

    contracts = contracts.copy()

    contracts["expiration_date"] = pd.to_datetime(
        contracts["expiration_date"],
        errors="coerce",
    )

    # ---------------------------------------------------------------
    # Derive renewable-contract flag from the source contract type.
    #
    # PPA and VPPA are treated as renewable contracts for this
    # demonstration. This keeps the integration layer aligned with
    # the actual generated Origination schema.
    # ---------------------------------------------------------------

    contracts["renewable_contract"] = (
        contracts["contract_type"]
        .astype(str)
        .str.upper()
        .isin({"PPA", "VPPA"})
    )

    contract_summary = (
        contracts
        .groupby("asset_code", as_index=False)
        .agg(
            contract_count=(
                "contract_code",
                "nunique",
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
                "renewable_contract",
                "sum",
            ),
            earliest_contract_expiration_date=(
                "expiration_date",
                "min",
            ),
        )
    )

    return contract_summary


def _aggregate_procurement(
    procurement: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate procurement information to the asset level."""

    if procurement.empty:
        return pd.DataFrame()

    required = {
        "asset_code",
        "procurement_opportunity_count",
        "procurement_required_mw",
        "procurement_estimated_value_usd",
        "procurement_blocker_count",
        "procurement_active_count",
    }

    missing = required - set(procurement.columns)

    if missing:
        raise ValueError(
            "Procurement data is missing required columns: "
            f"{sorted(missing)}"
        )

    return (
        procurement
        .groupby("asset_code", as_index=False)
        .agg(
            procurement_opportunity_count=(
                "procurement_opportunity_count",
                "sum",
            ),
            procurement_required_mw=(
                "procurement_required_mw",
                "sum",
            ),
            procurement_estimated_value_usd=(
                "procurement_estimated_value_usd",
                "sum",
            ),
            procurement_blocker_count=(
                "procurement_blocker_count",
                "sum",
            ),
            procurement_active_count=(
                "procurement_active_count",
                "sum",
            ),
        )
    )


def _aggregate_initiatives(
    initiatives: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate initiative information to the asset level."""

    if initiatives.empty:
        return pd.DataFrame()

    required = {
        "asset_code",
        "initiative_count",
        "initiative_completion_pct",
        "initiative_dependencies",
        "initiative_blocker_count",
        "high_priority_initiative_count",
    }

    missing = required - set(initiatives.columns)

    if missing:
        raise ValueError(
            "Initiative data is missing required columns: "
            f"{sorted(missing)}"
        )

    return (
        initiatives
        .groupby("asset_code", as_index=False)
        .agg(
            initiative_count=(
                "initiative_count",
                "sum",
            ),
            average_initiative_completion_pct=(
                "initiative_completion_pct",
                "mean",
            ),
            total_initiative_dependencies=(
                "initiative_dependencies",
                "sum",
            ),
            initiative_blocker_count=(
                "initiative_blocker_count",
                "sum",
            ),
            high_priority_initiative_count=(
                "high_priority_initiative_count",
                "sum",
            ),
        )
    )


def _aggregate_markets(
    markets: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate market information to the market level."""

    if markets.empty:
        return pd.DataFrame()

    required = {
        "market_code",
        "market_name",
        "region",
        "real_time_price_usd_mwh",
        "day_ahead_price_usd_mwh",
        "price_volatility",
    }

    missing = required - set(markets.columns)

    if missing:
        raise ValueError(
            "Wholesale market data is missing required columns: "
            f"{sorted(missing)}"
        )

    return (
        markets
        .groupby("market_code", as_index=False)
        .agg(
            market_name=(
                "market_name",
                "first",
            ),
            region_market=(
                "region",
                "first",
            ),
            real_time_price_usd_mwh=(
                "real_time_price_usd_mwh",
                "mean",
            ),
            day_ahead_price_usd_mwh=(
                "day_ahead_price_usd_mwh",
                "mean",
            ),
            price_volatility=(
                "price_volatility",
                "mean",
            ),
        )
    )


def build_cross_functional_view(
    portfolio: IntegratedPortfolio,
) -> pd.DataFrame:
    """
    Build one canonical asset-level DataFrame.

    The resulting table combines:

    - asset management
    - analytics / forecasting
    - wholesale markets
    - origination / contracts
    - procurement
    - initiatives
    """

    assets = portfolio.assets.copy()
    forecasts = portfolio.forecasts.copy()
    markets = portfolio.markets.copy()

    result = assets.copy()

    # ---------------------------------------------------------------
    # 1. Forecast context
    # ---------------------------------------------------------------

    if not forecasts.empty:
        forecast_columns = [
            "asset_code",
            "predicted_load_mw",
            "forecast_lower_mw",
            "forecast_upper_mw",
            "forecast_error_pct",
            "confidence",
            "model_name",
            "model_version",
        ]

        available = [
            column
            for column in forecast_columns
            if column in forecasts.columns
        ]

        result = result.merge(
            forecasts[available],
            on="asset_code",
            how="left",
        )

    # ---------------------------------------------------------------
    # 2. Market context
    # ---------------------------------------------------------------

    if not markets.empty and "market_code" in result.columns:
        market_summary = _aggregate_markets(markets)

        result = result.merge(
            market_summary,
            on="market_code",
            how="left",
        )

    # ---------------------------------------------------------------
    # 3. Contract context
    # ---------------------------------------------------------------

    contracts = portfolio.contracts.copy()

    if not contracts.empty and "asset_code" in contracts.columns:
        contract_summary = _aggregate_contracts(
            contracts
        )

        result = result.merge(
            contract_summary,
            on="asset_code",
            how="left",
        )

    # ---------------------------------------------------------------
    # 4. Procurement context
    # ---------------------------------------------------------------

    procurement = portfolio.procurement.copy()

    if not procurement.empty and "asset_code" in procurement.columns:
        procurement_summary = _aggregate_procurement(
            procurement
        )

        result = result.merge(
            procurement_summary,
            on="asset_code",
            how="left",
        )

    # ---------------------------------------------------------------
    # 5. Initiative context
    # ---------------------------------------------------------------

    initiatives = portfolio.initiatives.copy()

    if not initiatives.empty and "asset_code" in initiatives.columns:
        initiative_summary = _aggregate_initiatives(
            initiatives
        )

        result = result.merge(
            initiative_summary,
            on="asset_code",
            how="left",
        )

    # ---------------------------------------------------------------
    # 6. Normalize missing values
    # ---------------------------------------------------------------

    numeric_defaults = {
        "predicted_load_mw": 0.0,
        "forecast_lower_mw": 0.0,
        "forecast_upper_mw": 0.0,
        "forecast_error_pct": 0.0,
        "confidence": 0.0,
        "contract_count": 0.0,
        "contracted_mw": 0.0,
        "average_contract_price_usd_mwh": 0.0,
        "renewable_contract_count": 0.0,
        "procurement_opportunity_count": 0.0,
        "procurement_required_mw": 0.0,
        "procurement_estimated_value_usd": 0.0,
        "procurement_blocker_count": 0.0,
        "procurement_active_count": 0.0,
        "initiative_count": 0.0,
        "average_initiative_completion_pct": 0.0,
        "total_initiative_dependencies": 0.0,
        "initiative_blocker_count": 0.0,
        "high_priority_initiative_count": 0.0,
    }

    for column, default in numeric_defaults.items():
        if column in result.columns:
            result[column] = result[column].fillna(
                default
            )

    # ---------------------------------------------------------------
    # 7. Preserve datetime semantics for downstream risk metrics.
    #
    # Do NOT replace expiration dates with zero/NaN numeric defaults.
    # Missing expiration dates remain NaT and are handled by the
    # contract-risk function.
    # ---------------------------------------------------------------

    if "earliest_contract_expiration_date" in result.columns:
        result["earliest_contract_expiration_date"] = pd.to_datetime(
            result["earliest_contract_expiration_date"],
            errors="coerce",
        )

    return result


def generate_integrated_portfolio() -> IntegratedPortfolio:
    """
    Convenience function for generating and integrating demo data.
    """

    sources = generate_all_sources()

    return integrate_sources(
        sources
    )