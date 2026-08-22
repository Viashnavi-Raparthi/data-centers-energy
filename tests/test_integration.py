from gridportfolio.data.generators import generate_all_sources
from gridportfolio.integration.pipeline import (
    build_cross_functional_view,
    integrate_sources,
)


def test_all_sources_generate() -> None:
    sources = generate_all_sources()

    assert "asset_management" in sources
    assert "analytics" in sources
    assert "wholesale" in sources
    assert "origination" in sources
    assert "procurement" in sources
    assert "initiatives" in sources


def test_sources_integrate() -> None:
    sources = generate_all_sources()

    portfolio = integrate_sources(
        sources,
    )

    assert not portfolio.assets.empty
    assert not portfolio.forecasts.empty
    assert not portfolio.markets.empty
    assert not portfolio.contracts.empty


def test_cross_functional_view_connects_sources() -> None:
    sources = generate_all_sources()

    portfolio = integrate_sources(
        sources,
    )

    view = build_cross_functional_view(
        portfolio,
    )

    assert "asset_code" in view.columns
    assert "predicted_load_mw" in view.columns
    assert "price_volatility" in view.columns
    assert "contracted_mw" in view.columns