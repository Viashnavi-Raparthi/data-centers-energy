"""
Synthetic source-system schemas.

These schemas intentionally represent different organizational
systems rather than one perfectly normalized database.

That distinction is important.

The project is designed to demonstrate the problem of integration:

    different teams
        ↓
    different systems
        ↓
    different schemas
        ↓
    different definitions
        ↓
    fragmented visibility

GridPortfolio's integration layer is responsible for transforming
these source-specific structures into the shared portfolio model.

The source schemas should therefore remain somewhat imperfect.
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# Asset Management
# ============================================================


class AssetManagementRecord(BaseModel):
    """
    Operational record originating from Asset Management.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    asset_code: str

    asset_name: str

    region: str

    asset_category: str

    installed_capacity_mw: float = Field(
        ge=0,
    )

    current_load_mw: float = Field(
        ge=0,
    )

    forecast_load_mw: float = Field(
        ge=0,
    )

    availability_pct: float = Field(
        ge=0,
        le=100,
    )

    outage_status: str

    observation_time: datetime


# ============================================================
# Data & Analytics
# ============================================================


class AnalyticsForecastRecord(BaseModel):
    """
    Forecast output originating from Data & Analytics.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    asset_code: str

    forecast_date: date

    predicted_load_mw: float = Field(
        ge=0,
    )

    forecast_lower_mw: float = Field(
        ge=0,
    )

    forecast_upper_mw: float = Field(
        ge=0,
    )

    model_name: str

    model_version: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    forecast_error_pct: float


# ============================================================
# Wholesale
# ============================================================


class WholesaleMarketRecord(BaseModel):
    """
    Market observation originating from Wholesale.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    market_code: str

    market_name: str

    region: str

    observation_time: datetime

    real_time_price_usd_mwh: float = Field(
        ge=0,
    )

    day_ahead_price_usd_mwh: float = Field(
        ge=0,
    )

    price_volatility: float = Field(
        ge=0,
    )

    exposure_mw: float = Field(
        ge=0,
    )


# ============================================================
# Origination
# ============================================================


class OriginationContractRecord(BaseModel):
    """
    Contract position originating from Origination.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    contract_code: str

    asset_code: str

    market_code: str

    counterparty_name: str

    contract_type: str

    contracted_mw: float = Field(
        ge=0,
    )

    contract_price_usd_mwh: float = Field(
        ge=0,
    )

    renewable_flag: bool

    start_date: date

    expiration_date: date

    contract_status: str


# ============================================================
# Procurement
# ============================================================


class ProcurementPipelineRecord(BaseModel):
    """
    Procurement workflow record.

    This source intentionally represents execution rather than
    analytical data.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    opportunity_code: str

    region: str

    required_mw: float = Field(
        ge=0,
    )

    required_by_date: date

    procurement_stage: str

    owner_team: str

    expected_price_usd_mwh: float | None = Field(
        default=None,
        ge=0,
    )

    estimated_value_usd: float | None = Field(
        default=None,
        ge=0,
    )

    blocker: str | None = None


# ============================================================
# Program Management
# ============================================================


class InitiativeRecord(BaseModel):
    """
    Cross-functional initiative record.

    This represents the operating-model side of the problem.

    A portfolio may have excellent data and analytics while execution
    still stalls because ownership and dependencies are unclear.

    This schema lets GridPortfolio model that problem.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    initiative_code: str

    initiative_name: str

    primary_owner: str

    participating_teams: list[str]

    status: str

    completion_pct: float = Field(
        ge=0,
        le=100,
    )

    target_date: date

    dependency_count: int = Field(
        ge=0,
    )

    blocker: str | None = None

    priority: str