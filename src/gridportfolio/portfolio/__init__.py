"""
Portfolio intelligence layer.

This package provides the analytical and graph-based components used to
turn specialist data into shared portfolio context.
"""

from gridportfolio.portfolio.graph import (
    GraphEdge,
    GraphNode,
    PortfolioGraph,
    build_portfolio_graph,
)

from gridportfolio.portfolio.health import (
    PortfolioHealthResult,
    calculate_portfolio_health,
)

from gridportfolio.portfolio.metrics import (
    build_metric_table,
    contract_expiration_risk,
    forecast_uncertainty,
    market_risk,
    renewable_coverage,
)

__all__ = [
    "GraphEdge",
    "GraphNode",
    "PortfolioGraph",
    "build_portfolio_graph",
    "PortfolioHealthResult",
    "build_metric_table",
    "calculate_portfolio_health",
    "contract_expiration_risk",
    "forecast_uncertainty",
    "market_risk",
    "renewable_coverage",
]