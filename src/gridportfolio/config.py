"""
Application configuration for GridPortfolio.

GridPortfolio is designed to run as an open-source reference
implementation using synthetic energy data.

The configuration layer keeps infrastructure concerns separate from
the business logic so that a user can run the project locally,
replace individual data sources, and eventually connect real systems
without rewriting the portfolio model.

Architecture:

    Configuration
          │
          ├── Data sources
          ├── Storage
          ├── AI / LLM
          ├── Application
          └── Governance
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.

    Environment variables can override these defaults.

    Example:

        GRIDPORTFOLIO_ENV=production

    Secrets should never be committed to the repository.
    """

    model_config = SettingsConfigDict(
        env_prefix="GRIDPORTFOLIO_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ========================================================
    # Application
    # ========================================================

    app_name: str = "GridPortfolio"

    environment: str = "development"

    debug: bool = True

    version: str = "0.1.0"

    # ========================================================
    # API
    # ========================================================

    api_host: str = "127.0.0.1"

    api_port: int = Field(
        default=8000,
        ge=1,
        le=65535,
    )

    # ========================================================
    # Data
    # ========================================================

    data_directory: str = "data"

    raw_data_directory: str = "data/raw"

    processed_data_directory: str = "data/processed"

    synthetic_data_directory: str = "data/synthetic"

    # ========================================================
    # Database
    # ========================================================

    database_url: str = "sqlite:///./gridportfolio.db"

    # ========================================================
    # AI
    # ========================================================

    llm_provider: str = "mock"

    llm_model: str = "local"

    llm_api_key: str | None = None

    llm_temperature: float = Field(
        default=0.0,
        ge=0,
        le=2,
    )

    # ========================================================
    # Agent Configuration
    # ========================================================

    enable_agents: bool = True

    require_human_review: bool = True

    allow_autonomous_actions: bool = False

    max_agent_iterations: int = Field(
        default=8,
        ge=1,
        le=50,
    )

    # ========================================================
    # Portfolio Configuration
    # ========================================================

    portfolio_refresh_minutes: int = Field(
        default=60,
        ge=1,
    )

    risk_threshold: float = Field(
        default=0.70,
        ge=0,
        le=1,
    )

    critical_risk_threshold: float = Field(
        default=0.90,
        ge=0,
        le=1,
    )

    data_quality_threshold: float = Field(
        default=0.95,
        ge=0,
        le=1,
    )

    # ========================================================
    # Governance
    # ========================================================

    enable_audit_logging: bool = True

    retain_agent_runs: bool = True

    require_evidence_for_recommendations: bool = True

    require_confidence_scores: bool = True

    # ========================================================
    # Development
    # ========================================================

    use_synthetic_data: bool = True

    seed: int = Field(
        default=42,
        description="Random seed for reproducible synthetic data.",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return the application settings singleton.

    Using a cached settings object ensures that all components of
    the application operate against the same configuration.
    """

    return Settings()