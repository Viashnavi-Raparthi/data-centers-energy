"""
Synthetic energy organization generator.

This is the heart of the open-source demonstration.

The synthetic data is deliberately fragmented.

Each team sees a different piece of the portfolio:

    Asset Management
        → load growth

    Analytics
        → forecast uncertainty

    Wholesale
        → market volatility

    Origination
        → contract coverage

    Procurement
        → sourcing pipeline

    Program Management
        → execution blockers

The integration layer must discover that these are connected.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from gridportfolio.config import get_settings
from gridportfolio.data.schemas import (
    AnalyticsForecastRecord,
    AssetManagementRecord,
    InitiativeRecord,
    OriginationContractRecord,
    ProcurementPipelineRecord,
    WholesaleMarketRecord,
)


def generate_asset_management_data(
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Generate operational asset data.

    Includes an intentional load-growth event for the flagship
    demonstration scenario.
    """

    settings = get_settings()

    rng = np.random.default_rng(
        settings.seed if seed is None else seed,
    )

    rows: list[dict] = []

    assets = [
        {
            "asset_code": "DC-001",
            "asset_name": "Phoenix Data Center",
            "region": "WEST",
            "asset_category": "data_center",
            "capacity": 500,
        },
        {
            "asset_code": "DC-002",
            "asset_name": "Mesa Data Center",
            "region": "WEST",
            "asset_category": "data_center",
            "capacity": 400,
        },
        {
            "asset_code": "DC-003",
            "asset_name": "Dallas Data Center",
            "region": "ERCOT",
            "asset_category": "data_center",
            "capacity": 600,
        },
        {
            "asset_code": "DC-004",
            "asset_name": "Atlanta Data Center",
            "region": "SOUTHEAST",
            "asset_category": "data_center",
            "capacity": 350,
        },
    ]

    now = datetime.utcnow()

    for asset in assets:
        base_load = asset["capacity"] * 0.65

        for day in range(30):
            timestamp = now - timedelta(days=29 - day)

            growth = 1.0

            # Flagship cross-team signal:
            # Phoenix load has accelerated materially.
            if asset["asset_code"] == "DC-001" and day >= 20:
                growth = 1.18

            load = base_load * growth

            rows.append(
                {
                    "asset_code": asset["asset_code"],
                    "asset_name": asset["asset_name"],
                    "region": asset["region"],
                    "asset_category": asset["asset_category"],
                    "installed_capacity_mw": asset["capacity"],
                    "current_load_mw": max(
                        0,
                        load + rng.normal(0, 8),
                    ),
                    "forecast_load_mw": max(
                        0,
                        load + rng.normal(0, 4),
                    ),
                    "availability_pct": max(
                        0,
                        min(
                            100,
                            97 + rng.normal(0, 1.5),
                        ),
                    ),
                    "outage_status": "normal",
                    "observation_time": timestamp,
                }
            )

    return pd.DataFrame(rows)


def generate_analytics_data(
    asset_df: pd.DataFrame,
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Generate forecast output.

    The Phoenix forecast intentionally becomes less accurate during
    the same period that load accelerates.

    Analytics sees forecast deterioration.

    It does not inherently know that this is connected to the
    expiring contract and market conditions.
    """

    settings = get_settings()

    rng = np.random.default_rng(
        settings.seed + 1 if seed is None else seed + 1,
    )

    rows: list[dict] = []

    for _, row in asset_df.iterrows():
        forecast = row["forecast_load_mw"]

        is_phoenix = row["asset_code"] == "DC-001"

        error = (
            rng.normal(2.0, 1.0)
            + (6.0 if is_phoenix and row["observation_time"].day >= 1 else 0)
        )

        lower = forecast * (1 - abs(error) / 100)
        upper = forecast * (1 + abs(error) / 100)

        rows.append(
            {
                "asset_code": row["asset_code"],
                "forecast_date": row["observation_time"].date(),
                "predicted_load_mw": forecast,
                "forecast_lower_mw": lower,
                "forecast_upper_mw": upper,
                "model_name": "synthetic_load_forecaster",
                "model_version": "1.0",
                "confidence": max(
                    0.5,
                    min(
                        0.99,
                        1 - abs(error) / 100,
                    ),
                ),
                "forecast_error_pct": error,
            }
        )

    return pd.DataFrame(rows)


def generate_wholesale_data(
    seed: int | None = None,
) -> pd.DataFrame:
    """
    Generate market data.

    The WEST market intentionally experiences elevated volatility,
    creating a second signal that should be connected with the
    Phoenix load-growth signal.
    """

    settings = get_settings()

    rng = np.random.default_rng(
        settings.seed + 2 if seed is None else seed + 2,
    )

    rows: list[dict] = []

    markets = [
        ("WEST", "Western Market", 72),
        ("ERCOT", "ERCOT", 68),
        ("SOUTHEAST", "Southeast Market", 61),
    ]

    now = datetime.utcnow()

    for market_code, market_name, base_price in markets:
        for day in range(30):
            timestamp = now - timedelta(days=29 - day)

            volatility = 0.15

            if market_code == "WEST" and day >= 20:
                volatility = 0.38

            price = base_price * (
                1 + rng.normal(0, volatility)
            )

            rows.append(
                {
                    "market_code": market_code,
                    "market_name": market_name,
                    "region": market_code,
                    "observation_time": timestamp,
                    "real_time_price_usd_mwh": max(
                        0,
                        price,
                    ),
                    "day_ahead_price_usd_mwh": max(
                        0,
                        price * 0.97,
                    ),
                    "price_volatility": volatility,
                    "exposure_mw": (
                        300
                        if market_code == "WEST"
                        else 200
                    ),
                }
            )

    return pd.DataFrame(rows)


def generate_origination_data() -> pd.DataFrame:
    """
    Generate renewable contract positions.

    The flagship contract expires soon.

    Origination owns this information.

    The integration layer must connect it to the other signals.
    """

    today = date.today()

    contracts = [
        {
            "contract_code": "PPA-001",
            "asset_code": "DC-001",
            "market_code": "WEST",
            "counterparty_name": "Synthetic Renewable Partner",
            "contract_type": "PPA",
            "contracted_mw": 250,
            "contract_price_usd_mwh": 54,
            "renewable_flag": True,
            "start_date": today - timedelta(days=600),
            "expiration_date": today + timedelta(days=74),
            "contract_status": "expiring",
        },
        {
            "contract_code": "PPA-002",
            "asset_code": "DC-002",
            "market_code": "WEST",
            "counterparty_name": "Synthetic Solar Partner",
            "contract_type": "PPA",
            "contracted_mw": 220,
            "contract_price_usd_mwh": 52,
            "renewable_flag": True,
            "start_date": today - timedelta(days=400),
            "expiration_date": today + timedelta(days=500),
            "contract_status": "active",
        },
        {
            "contract_code": "PPA-003",
            "asset_code": "DC-003",
            "market_code": "ERCOT",
            "counterparty_name": "Synthetic Wind Partner",
            "contract_type": "VPPA",
            "contracted_mw": 300,
            "contract_price_usd_mwh": 48,
            "renewable_flag": True,
            "start_date": today - timedelta(days=300),
            "expiration_date": today + timedelta(days=800),
            "contract_status": "active",
        },
    ]

    return pd.DataFrame(contracts)


def generate_procurement_data() -> pd.DataFrame:
    """
    Generate procurement workflow.

    Deliberately, there is no active procurement opportunity for the
    Phoenix contract gap.

    This creates the final missing piece in the cross-team signal.
    """

    today = date.today()

    records = [
        {
            "opportunity_code": "PROC-001",
            "region": "ERCOT",
            "required_mw": 150,
            "required_by_date": today + timedelta(days=120),
            "procurement_stage": "market_scan",
            "owner_team": "Procurement",
            "expected_price_usd_mwh": 58,
            "estimated_value_usd": 4_200_000,
            "blocker": None,
        },
        {
            "opportunity_code": "PROC-002",
            "region": "SOUTHEAST",
            "required_mw": 100,
            "required_by_date": today + timedelta(days=180),
            "procurement_stage": "not_started",
            "owner_team": "Procurement",
            "expected_price_usd_mwh": None,
            "estimated_value_usd": None,
            "blocker": None,
        },
    ]

    return pd.DataFrame(records)


def generate_initiative_data() -> pd.DataFrame:
    """
    Generate program-management data.

    The flagship procurement initiative is blocked by a dependency
    owned by another team.
    """

    today = date.today()

    records = [
        {
            "initiative_code": "INIT-001",
            "initiative_name": "WEST Renewable Coverage Expansion",
            "primary_owner": "Origination",
            "participating_teams": [
                "Origination",
                "Wholesale",
                "Analytics",
                "Procurement",
            ],
            "status": "at_risk",
            "completion_pct": 38,
            "target_date": today + timedelta(days=90),
            "dependency_count": 2,
            "blocker": "Updated load forecast not formally approved",
            "priority": "critical",
        },
        {
            "initiative_code": "INIT-002",
            "initiative_name": "ERCOT Market Optimization",
            "primary_owner": "Wholesale",
            "participating_teams": [
                "Wholesale",
                "Analytics",
            ],
            "status": "in_progress",
            "completion_pct": 64,
            "target_date": today + timedelta(days=120),
            "dependency_count": 1,
            "blocker": None,
            "priority": "high",
        },
    ]

    return pd.DataFrame(records)


def generate_all_sources(
    seed: int | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Generate the complete fragmented organization.

    Returns separate DataFrames rather than one normalized dataset.

    That is intentional.

    The integration pipeline must perform the organizational
    connective-tissue work.
    """

    asset_data = generate_asset_management_data(seed)

    return {
        "asset_management": asset_data,
        "analytics": generate_analytics_data(
            asset_data,
            seed,
        ),
        "wholesale": generate_wholesale_data(seed),
        "origination": generate_origination_data(),
        "procurement": generate_procurement_data(),
        "initiatives": generate_initiative_data(),
    }