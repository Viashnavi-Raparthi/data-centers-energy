"""
Integration layer.

Connects specialist source systems into shared portfolio context.
"""

from gridportfolio.integration.connectors import (
    DataFrameConnector,
    SourceConnector,
    SourceRegistry,
)

from gridportfolio.integration.pipeline import (
    IntegratedPortfolio,
    build_cross_functional_view,
    integrate_sources,
)

from gridportfolio.integration.quality import (
    QualityResult,
    assess_all_sources,
    assess_dataframe_quality,
)

__all__ = [
    "DataFrameConnector",
    "IntegratedPortfolio",
    "QualityResult",
    "SourceConnector",
    "SourceRegistry",
    "assess_all_sources",
    "assess_dataframe_quality",
    "build_cross_functional_view",
    "integrate_sources",
]