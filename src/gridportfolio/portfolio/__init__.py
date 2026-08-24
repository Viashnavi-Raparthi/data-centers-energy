"""
Portfolio layer.

Provides portfolio-level metrics, health assessment, and graph utilities.
"""

from gridportfolio.portfolio.health import (
    PortfolioHealthResult,
    calculate_portfolio_health,
)

from gridportfolio.portfolio.metrics import (
    build_metric_table,
    contract_coverage,
    contract_expiration_risk,
    forecast_error_risk,
    forecast_uncertainty,
    market_risk,
    market_volatility_risk,
    renewable_coverage,
)

__all__ = [
    "PortfolioHealthResult",
    "calculate_portfolio_health",
    "build_metric_table",
    "forecast_uncertainty",
    "contract_expiration_risk",
    "forecast_error_risk",
    "market_volatility_risk",
    "market_risk",
    "contract_coverage",
    "renewable_coverage",
]
