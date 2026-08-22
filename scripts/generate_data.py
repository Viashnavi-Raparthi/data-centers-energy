"""
Generate a completely synthetic energy portfolio for GridPortfolio.

Purpose
-------
This script creates realistic-but-fake energy portfolio data that can be
used to demonstrate:

    DATA
      ↓
    SHARED PORTFOLIO TRUTH
      ↓
    ANALYTICS
      ↓
    CROSS-TEAM IMPACT
      ↓
    DECISION INTELLIGENCE
      ↓
    EXECUTION

The generated data intentionally contains relationships between:

- organizations
- assets
- markets
- contracts
- hourly load
- generation
- forecasts
- market prices
- risks
- initiatives
- decisions
- actions

No proprietary or real customer/employer data is used.

Usage
-----
From the repository root:

    python scripts/generate_data.py

Or:

    python -m scripts.generate_data

The random seed is configurable through the RANDOM_SEED environment variable.

Output
------
data/raw/
    organizations.csv
    assets.csv
    markets.csv
    contracts.csv
    initiatives.csv
    decisions.csv
    actions.csv
    hourly_portfolio.csv

The generated data is deterministic when the same seed is used.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]

DATA_DIR: Final[Path] = PROJECT_ROOT / os.getenv("DATA_DIR", "data")
RAW_DATA_DIR: Final[Path] = DATA_DIR / "raw"

DEFAULT_RANDOM_SEED: Final[int] = int(
    os.getenv("RANDOM_SEED", "42")
)

DEFAULT_HISTORICAL_HOURS: Final[int] = int(
    os.getenv("HISTORICAL_HOURS", "8760")
)


# ============================================================
# Organization
# ============================================================

ORGANIZATIONS: Final[list[dict[str, object]]] = [
    {
        "organization_id": "ORG-DATA",
        "name": "Data & Analytics",
        "organization_type": "analytics",
        "description": (
            "Owns data, analytics, forecasting, models, reporting, "
            "and data quality."
        ),
    },
    {
        "organization_id": "ORG-ASSET",
        "name": "Asset Management",
        "organization_type": "operations",
        "description": (
            "Owns physical asset performance, availability, "
            "load, generation, and operational assumptions."
        ),
    },
    {
        "organization_id": "ORG-ORIG",
        "name": "Energy Origination",
        "organization_type": "commercial",
        "description": (
            "Owns renewable procurement opportunities, PPAs, "
            "VPPAs, and contract pipeline."
        ),
    },
    {
        "organization_id": "ORG-WHOLESALE",
        "name": "Wholesale",
        "organization_type": "market",
        "description": (
            "Owns market exposure, hedging, congestion, "
            "and wholesale purchases."
        ),
    },
    {
        "organization_id": "ORG-PROC",
        "name": "Procurement",
        "organization_type": "commercial",
        "description": (
            "Owns procurement strategy, sourcing decisions, "
            "and commercial execution."
        ),
    },
    {
        "organization_id": "ORG-SUST",
        "name": "Sustainability",
        "organization_type": "strategy",
        "description": (
            "Owns renewable coverage, carbon intensity, "
            "and sustainability targets."
        ),
    },
    {
        "organization_id": "ORG-FIN",
        "name": "Finance",
        "organization_type": "finance",
        "description": (
            "Owns financial exposure, budgeting, valuation, "
            "and financial risk."
        ),
    },
    {
        "organization_id": "ORG-LEAD",
        "name": "Leadership",
        "organization_type": "executive",
        "description": (
            "Consumes integrated portfolio intelligence and "
            "makes strategic decisions."
        ),
    },
]


# ============================================================
# Markets
# ============================================================

MARKETS: Final[list[dict[str, object]]] = [
    {
        "market_id": "MKT-ERCOT",
        "name": "ERCOT",
        "iso": "ERCOT",
        "region": "Texas",
        "currency": "USD",
        "base_price": 52.0,
        "price_volatility": 0.35,
    },
    {
        "market_id": "MKT-MISO",
        "name": "MISO",
        "iso": "MISO",
        "region": "Midwest",
        "currency": "USD",
        "base_price": 42.0,
        "price_volatility": 0.25,
    },
    {
        "market_id": "MKT-PJM",
        "name": "PJM",
        "iso": "PJM",
        "region": "Mid-Atlantic",
        "currency": "USD",
        "base_price": 58.0,
        "price_volatility": 0.28,
    },
    {
        "market_id": "MKT-WECC",
        "name": "WECC",
        "iso": "WECC",
        "region": "Western US",
        "currency": "USD",
        "base_price": 61.0,
        "price_volatility": 0.32,
    },
]


# ============================================================
# Assets
# ============================================================

ASSETS: Final[list[dict[str, object]]] = [
    {
        "asset_id": "TX-DC-01",
        "name": "Texas Data Center 01",
        "asset_type": "data_center",
        "market_id": "MKT-ERCOT",
        "capacity_mw": 500.0,
        "expected_load_factor": 0.72,
        "renewable_target": 0.95,
    },
    {
        "asset_id": "TX-DC-02",
        "name": "Texas Data Center 02",
        "asset_type": "data_center",
        "market_id": "MKT-ERCOT",
        "capacity_mw": 750.0,
        "expected_load_factor": 0.76,
        "renewable_target": 0.95,
    },
    {
        "asset_id": "AZ-DC-01",
        "name": "Arizona Data Center 01",
        "asset_type": "data_center",
        "market_id": "MKT-WECC",
        "capacity_mw": 400.0,
        "expected_load_factor": 0.68,
        "renewable_target": 0.90,
    },
    {
        "asset_id": "IA-DC-01",
        "name": "Iowa Data Center 01",
        "asset_type": "data_center",
        "market_id": "MKT-MISO",
        "capacity_mw": 300.0,
        "expected_load_factor": 0.70,
        "renewable_target": 0.95,
    },
    {
        "asset_id": "VA-DC-01",
        "name": "Virginia Data Center 01",
        "asset_type": "data_center",
        "market_id": "MKT-PJM",
        "capacity_mw": 600.0,
        "expected_load_factor": 0.74,
        "renewable_target": 0.95,
    },
    {
        "asset_id": "TX-SOLAR-01",
        "name": "Texas Solar Farm 01",
        "asset_type": "solar",
        "market_id": "MKT-ERCOT",
        "capacity_mw": 350.0,
        "expected_load_factor": 0.28,
        "renewable_target": None,
    },
    {
        "asset_id": "TX-WIND-01",
        "name": "Texas Wind Farm 01",
        "asset_type": "wind",
        "market_id": "MKT-ERCOT",
        "capacity_mw": 400.0,
        "expected_load_factor": 0.42,
        "renewable_target": None,
    },
    {
        "asset_id": "IA-WIND-01",
        "name": "Iowa Wind Farm 01",
        "asset_type": "wind",
        "market_id": "MKT-MISO",
        "capacity_mw": 300.0,
        "expected_load_factor": 0.40,
        "renewable_target": None,
    },
    {
        "asset_id": "AZ-SOLAR-01",
        "name": "Arizona Solar Farm 01",
        "asset_type": "solar",
        "market_id": "MKT-WECC",
        "capacity_mw": 250.0,
        "expected_load_factor": 0.27,
        "renewable_target": None,
    },
    {
        "asset_id": "VA-SOLAR-01",
        "name": "Virginia Solar Farm 01",
        "asset_type": "solar",
        "market_id": "MKT-PJM",
        "capacity_mw": 300.0,
        "expected_load_factor": 0.25,
        "renewable_target": None,
    },
]


# ============================================================
# Contract templates
# ============================================================

CONTRACT_TYPES: Final[list[str]] = [
    "PPA",
    "VPPA",
    "UTILITY_CONTRACT",
    "WHOLESALE_HEDGE",
]

CONTRACT_STATUSES: Final[list[str]] = [
    "active",
    "active",
    "active",
    "expiring",
]


# ============================================================
# Initiatives
# ============================================================

INITIATIVE_TEMPLATES: Final[list[dict[str, object]]] = [
    {
        "initiative_type": "renewable_procurement",
        "name_template": "Renewable Procurement Program {i:02d}",
        "primary_team": "ORG-PROC",
    },
    {
        "initiative_type": "data_center_expansion",
        "name_template": "Data Center Expansion {i:02d}",
        "primary_team": "ORG-ASSET",
    },
    {
        "initiative_type": "market_strategy",
        "name_template": "Market Exposure Optimization {i:02d}",
        "primary_team": "ORG-WHOLESALE",
    },
    {
        "initiative_type": "sustainability",
        "name_template": "Hourly Renewable Matching {i:02d}",
        "primary_team": "ORG-SUST",
    },
    {
        "initiative_type": "data_quality",
        "name_template": "Portfolio Data Quality Program {i:02d}",
        "primary_team": "ORG-DATA",
    },
]


# ============================================================
# Utility functions
# ============================================================


def get_rng(seed: int) -> np.random.Generator:
    """Return a reproducible NumPy random generator."""
    return np.random.default_rng(seed)


def ensure_directories() -> None:
    """Create required output directories."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_dataframe(
    dataframe: pd.DataFrame,
    filename: str,
) -> None:
    """Save a dataframe to the synthetic raw-data directory."""
    path = RAW_DATA_DIR / filename
    dataframe.to_csv(path, index=False)
    print(f"Generated {len(dataframe):,} rows → {path}")


# ============================================================
# Generate contracts
# ============================================================


def generate_contracts(
    rng: np.random.Generator,
    assets: pd.DataFrame,
    number_of_contracts: int = 40,
) -> pd.DataFrame:
    """
    Generate synthetic energy contracts.

    Contracts intentionally connect:

        Asset
          ↓
        Market
          ↓
        Origination / Wholesale
          ↓
        Procurement
          ↓
        Sustainability
    """

    rows: list[dict[str, object]] = []

    renewable_assets = assets[
        assets["asset_type"].isin(["solar", "wind"])
    ]

    for index in range(number_of_contracts):
        contract_id = f"CTR-{index + 1:04d}"

        contract_type = rng.choice(CONTRACT_TYPES)

        if contract_type in {"PPA", "VPPA"}:
            asset = renewable_assets.iloc[
                int(rng.integers(0, len(renewable_assets)))
            ]

            capacity_mw = float(
                rng.uniform(50, min(float(asset["capacity_mw"]), 250))
            )

            renewable = True

        else:
            asset = assets.iloc[
                int(rng.integers(0, len(assets)))
            ]

            capacity_mw = float(
                rng.uniform(50, 300)
            )

            renewable = False

        start_date = pd.Timestamp("2025-01-01") + pd.Timedelta(
            days=int(rng.integers(0, 365))
        )

        duration_years = int(
            rng.choice([2, 3, 5, 7, 10])
        )

        end_date = start_date + pd.DateOffset(
            years=duration_years
        )

        rows.append(
            {
                "contract_id": contract_id,
                "contract_type": contract_type,
                "asset_id": asset["asset_id"],
                "market_id": asset["market_id"],
                "counterparty": f"Counterparty-{rng.integers(1, 15):02d}",
                "capacity_mw": round(capacity_mw, 2),
                "price_per_mwh": round(
                    rng.uniform(28, 85),
                    2,
                ),
                "renewable": renewable,
                "start_date": start_date.date(),
                "end_date": end_date.date(),
                "status": rng.choice(CONTRACT_STATUSES),
                "expected_annual_mwh": round(
                    capacity_mw * 8760 * rng.uniform(0.20, 0.50),
                    2,
                ),
                "performance_factor": round(
                    rng.uniform(0.82, 1.02),
                    4,
                ),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Generate hourly portfolio data
# ============================================================


def generate_hourly_portfolio(
    rng: np.random.Generator,
    assets: pd.DataFrame,
    markets: pd.DataFrame,
    historical_hours: int,
) -> pd.DataFrame:
    """
    Generate hourly synthetic portfolio observations.

    The dataset deliberately contains realistic signals:

    - daily seasonality
    - annual seasonality
    - noise
    - forecast error
    - renewable generation variability
    - market price volatility
    - occasional anomalies
    - occasional outages
    """

    end_timestamp = pd.Timestamp("2026-01-01")

    timestamps = pd.date_range(
        end=end_timestamp,
        periods=historical_hours,
        freq="h",
    )

    rows: list[dict[str, object]] = []

    market_lookup = markets.set_index("market_id").to_dict("index")

    for _, asset in assets.iterrows():

        asset_id = str(asset["asset_id"])
        asset_type = str(asset["asset_type"])
        market_id = str(asset["market_id"])

        market = market_lookup[market_id]

        capacity_mw = float(asset["capacity_mw"])
        load_factor = float(asset["expected_load_factor"])

        for timestamp in timestamps:

            hour = timestamp.hour
            day_of_year = timestamp.dayofyear

            daily_cycle = np.sin(
                2 * np.pi * (hour - 7) / 24
            )

            annual_cycle = np.sin(
                2 * np.pi * day_of_year / 365
            )

            # ------------------------------------------------
            # Data-center load
            # ------------------------------------------------

            if asset_type == "data_center":

                baseline_load = (
                    capacity_mw
                    * load_factor
                )

                load = (
                    baseline_load
                    * (
                        1
                        + 0.06 * daily_cycle
                        + 0.08 * annual_cycle
                    )
                )

                load += rng.normal(
                    0,
                    baseline_load * 0.025,
                )

                forecast = (
                    baseline_load
                    * (
                        1
                        + 0.05 * daily_cycle
                        + 0.07 * annual_cycle
                    )
                )

                forecast += rng.normal(
                    0,
                    baseline_load * 0.015,
                )

                generation = 0.0

                # ------------------------------------------------
                # Occasionally inject load anomalies.
                # ------------------------------------------------

                if rng.random() < 0.0008:
                    load *= rng.uniform(1.20, 1.45)

            # ------------------------------------------------
            # Solar
            # ------------------------------------------------

            elif asset_type == "solar":

                solar_shape = max(
                    0,
                    np.sin(
                        np.pi
                        * (hour - 6)
                        / 12
                    ),
                )

                generation = (
                    capacity_mw
                    * load_factor
                    * solar_shape
                    * (1 + 0.15 * annual_cycle)
                )

                generation += rng.normal(
                    0,
                    capacity_mw * 0.03,
                )

                generation = max(
                    0,
                    generation,
                )

                load = 0.0

                forecast = generation * (
                    1 + rng.normal(0, 0.08)
                )

            # ------------------------------------------------
            # Wind
            # ------------------------------------------------

            elif asset_type == "wind":

                wind_factor = (
                    0.65
                    + 0.25
                    * np.sin(
                        2 * np.pi * day_of_year / 14
                    )
                    + rng.normal(0, 0.12)
                )

                generation = (
                    capacity_mw
                    * load_factor
                    * np.clip(
                        wind_factor,
                        0.05,
                        1.20,
                    )
                )

                load = 0.0

                forecast = generation * (
                    1 + rng.normal(0, 0.12)
                )

            else:
                load = 0.0
                generation = 0.0
                forecast = 0.0

            # ------------------------------------------------
            # Outages
            # ------------------------------------------------

            outage_flag = False

            if rng.random() < 0.0004:
                outage_flag = True

                if asset_type == "data_center":
                    load *= rng.uniform(0.10, 0.50)
                else:
                    generation *= rng.uniform(0.00, 0.20)

            # ------------------------------------------------
            # Market price
            # ------------------------------------------------

            base_price = float(
                market["base_price"]
            )

            volatility = float(
                market["price_volatility"]
            )

            price = (
                base_price
                * (
                    1
                    + volatility
                    * 0.20
                    * annual_cycle
                    + volatility
                    * 0.15
                    * daily_cycle
                )
            )

            price += rng.normal(
                0,
                base_price * volatility * 0.12,
            )

            # ------------------------------------------------
            # Rare market price spikes
            # ------------------------------------------------

            if rng.random() < 0.001:
                price *= rng.uniform(
                    2.0,
                    5.0,
                )

            price = max(
                0,
                price,
            )

            # ------------------------------------------------
            # Data quality
            # ------------------------------------------------

            data_quality_score = 1.0

            if rng.random() < 0.002:
                data_quality_score = float(
                    rng.uniform(0.50, 0.85)
                )

            rows.append(
                {
                    "timestamp": timestamp,
                    "asset_id": asset_id,
                    "market_id": market_id,
                    "asset_type": asset_type,
                    "load_mw": round(
                        max(load, 0),
                        3,
                    ),
                    "generation_mw": round(
                        max(generation, 0),
                        3,
                    ),
                    "forecast_mw": round(
                        max(forecast, 0),
                        3,
                    ),
                    "market_price_per_mwh": round(
                        price,
                        3,
                    ),
                    "outage_flag": outage_flag,
                    "data_quality_score": round(
                        data_quality_score,
                        3,
                    ),
                }
            )

    return pd.DataFrame(rows)


# ============================================================
# Generate initiatives
# ============================================================


def generate_initiatives(
    rng: np.random.Generator,
    number_of_initiatives: int = 20,
) -> pd.DataFrame:
    """
    Generate cross-functional initiatives.

    Every initiative has multiple participating teams.

    This is critical to demonstrating that the project is not
    merely an energy analytics dashboard.
    """

    team_ids = [
        organization["organization_id"]
        for organization in ORGANIZATIONS
        if organization["organization_type"] != "executive"
    ]

    rows: list[dict[str, object]] = []

    statuses = [
        "not_started",
        "planning",
        "in_progress",
        "at_risk",
        "blocked",
        "completed",
    ]

    priorities = [
        "low",
        "medium",
        "high",
        "critical",
    ]

    for index in range(number_of_initiatives):

        template = INITIATIVE_TEMPLATES[
            index % len(INITIATIVE_TEMPLATES)
        ]

        participating_team_count = int(
            rng.integers(2, 6)
        )

        participating_teams = rng.choice(
            team_ids,
            size=participating_team_count,
            replace=False,
        ).tolist()

        owner = str(
            template["primary_team"]
        )

        if owner not in participating_teams:
            participating_teams[0] = owner

        rows.append(
            {
                "initiative_id": f"INIT-{index + 1:03d}",
                "name": str(
                    template["name_template"]
                ).format(i=index + 1),
                "initiative_type": template[
                    "initiative_type"
                ],
                "primary_owner": owner,
                "participating_teams": "|".join(
                    participating_teams
                ),
                "status": rng.choice(statuses),
                "priority": rng.choice(priorities),
                "completion_pct": round(
                    float(
                        rng.uniform(
                            0,
                            100,
                        )
                    ),
                    1,
                ),
                "target_date": (
                    pd.Timestamp("2026-01-01")
                    + pd.Timedelta(
                        days=int(
                            rng.integers(
                                30,
                                720,
                            )
                        )
                    )
                ).date(),
                "risk_score": round(
                    float(
                        rng.uniform(
                            0.05,
                            0.85,
                        )
                    ),
                    3,
                ),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Generate decisions
# ============================================================


def generate_decisions(
    rng: np.random.Generator,
    initiatives: pd.DataFrame,
) -> pd.DataFrame:

    decision_types = [
        "procurement",
        "hedging",
        "contract",
        "capacity",
        "sustainability",
        "portfolio_strategy",
    ]

    statuses = [
        "draft",
        "pending",
        "approved",
        "implemented",
    ]

    rows: list[dict[str, object]] = []

    for index in range(max(10, len(initiatives) // 2)):

        initiative = initiatives.iloc[
            index % len(initiatives)
        ]

        rows.append(
            {
                "decision_id": f"DEC-{index + 1:03d}",
                "initiative_id": initiative[
                    "initiative_id"
                ],
                "decision_type": rng.choice(
                    decision_types
                ),
                "decision_owner": initiative[
                    "primary_owner"
                ],
                "status": rng.choice(
                    statuses
                ),
                "decision_title": (
                    f"Portfolio Decision "
                    f"{index + 1:03d}"
                ),
                "financial_exposure_usd": round(
                    float(
                        rng.uniform(
                            1_000_000,
                            25_000_000,
                        )
                    ),
                    2,
                ),
                "confidence_score": round(
                    float(
                        rng.uniform(
                            0.65,
                            0.98,
                        )
                    ),
                    3,
                ),
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# Generate actions
# ============================================================


def generate_actions(
    rng: np.random.Generator,
    decisions: pd.DataFrame,
) -> pd.DataFrame:

    action_statuses = [
        "not_started",
        "in_progress",
        "blocked",
        "completed",
    ]

    rows: list[dict[str, object]] = []

    for _, decision in decisions.iterrows():

        number_of_actions = int(
            rng.integers(2, 5)
        )

        for action_number in range(
            number_of_actions
        ):

            rows.append(
                {
                    "action_id": (
                        f"ACTION-"
                        f"{len(rows) + 1:04d}"
                    ),
                    "decision_id": decision[
                        "decision_id"
                    ],
                    "owner_team": rng.choice(
                        [
                            "ORG-ASSET",
                            "ORG-ORIG",
                            "ORG-WHOLESALE",
                            "ORG-PROC",
                            "ORG-SUST",
                            "ORG-FIN",
                        ]
                    ),
                    "action_description": (
                        f"Cross-functional action "
                        f"{action_number + 1}"
                    ),
                    "status": rng.choice(
                        action_statuses
                    ),
                    "due_date": (
                        pd.Timestamp("2026-01-01")
                        + pd.Timedelta(
                            days=int(
                                rng.integers(
                                    7,
                                    120,
                                )
                            )
                        )
                    ).date(),
                }
            )

    return pd.DataFrame(rows)


# ============================================================
# Main generation pipeline
# ============================================================


def generate_portfolio(
    seed: int = DEFAULT_RANDOM_SEED,
    historical_hours: int = DEFAULT_HISTORICAL_HOURS,
) -> None:
    """
    Generate the complete synthetic GridPortfolio dataset.
    """

    print("=" * 70)
    print("GridPortfolio Synthetic Portfolio Generator")
    print("=" * 70)

    print(f"Random seed: {seed}")
    print(f"Historical hours: {historical_hours}")
    print(f"Output directory: {RAW_DATA_DIR}")
    print()

    ensure_directories()

    rng = get_rng(seed)

    # --------------------------------------------------------
    # Organizations
    # --------------------------------------------------------

    organizations_df = pd.DataFrame(
        ORGANIZATIONS
    )

    save_dataframe(
        organizations_df,
        "organizations.csv",
    )

    # --------------------------------------------------------
    # Markets
    # --------------------------------------------------------

    markets_df = pd.DataFrame(
        MARKETS
    )

    save_dataframe(
        markets_df,
        "markets.csv",
    )

    # --------------------------------------------------------
    # Assets
    # --------------------------------------------------------

    assets_df = pd.DataFrame(
        ASSETS
    )

    save_dataframe(
        assets_df,
        "assets.csv",
    )

    # --------------------------------------------------------
    # Contracts
    # --------------------------------------------------------

    number_of_contracts = int(
        os.getenv(
            "NUM_CONTRACTS",
            "40",
        )
    )

    contracts_df = generate_contracts(
        rng=rng,
        assets=assets_df,
        number_of_contracts=number_of_contracts,
    )

    save_dataframe(
        contracts_df,
        "contracts.csv",
    )

    # --------------------------------------------------------
    # Hourly portfolio
    # --------------------------------------------------------

    hourly_df = generate_hourly_portfolio(
        rng=rng,
        assets=assets_df,
        markets=markets_df,
        historical_hours=historical_hours,
    )

    save_dataframe(
        hourly_df,
        "hourly_portfolio.csv",
    )

    # --------------------------------------------------------
    # Initiatives
    # --------------------------------------------------------

    number_of_initiatives = int(
        os.getenv(
            "NUM_INITIATIVES",
            "20",
        )
    )

    initiatives_df = generate_initiatives(
        rng=rng,
        number_of_initiatives=number_of_initiatives,
    )

    save_dataframe(
        initiatives_df,
        "initiatives.csv",
    )

    # --------------------------------------------------------
    # Decisions
    # --------------------------------------------------------

    decisions_df = generate_decisions(
        rng=rng,
        initiatives=initiatives_df,
    )

    save_dataframe(
        decisions_df,
        "decisions.csv",
    )

    # --------------------------------------------------------
    # Actions
    # --------------------------------------------------------

    actions_df = generate_actions(
        rng=rng,
        decisions=decisions_df,
    )

    save_dataframe(
        actions_df,
        "actions.csv",
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("Generation complete")
    print("=" * 70)

    print(
        f"Organizations: {len(organizations_df):,}"
    )

    print(
        f"Markets:       {len(markets_df):,}"
    )

    print(
        f"Assets:        {len(assets_df):,}"
    )

    print(
        f"Contracts:     {len(contracts_df):,}"
    )

    print(
        f"Hourly rows:   {len(hourly_df):,}"
    )

    print(
        f"Initiatives:   {len(initiatives_df):,}"
    )

    print(
        f"Decisions:     {len(decisions_df):,}"
    )

    print(
        f"Actions:       {len(actions_df):,}"
    )

    print()
    print(
        "Synthetic data is ready for GridPortfolio."
    )


# ============================================================
# CLI entry point
# ============================================================


if __name__ == "__main__":
    generate_portfolio()