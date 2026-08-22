from gridportfolio.data.generators import generate_all_sources
from gridportfolio.integration.pipeline import (
    build_cross_functional_view,
    integrate_sources,
)
from gridportfolio.signals.detector import (
    detect_cross_functional_signals,
)


def test_cross_team_signal_is_detected() -> None:
    sources = generate_all_sources()

    portfolio = integrate_sources(
        sources,
    )

    view = build_cross_functional_view(
        portfolio,
    )

    signals = detect_cross_functional_signals(
        view,
    )

    assert len(signals) >= 1

    assert any(
        signal["asset_code"] == "DC-001"
        for signal in signals
    )


def test_signal_contains_multiple_teams() -> None:
    sources = generate_all_sources()

    portfolio = integrate_sources(
        sources,
    )

    view = build_cross_functional_view(
        portfolio,
    )

    signals = detect_cross_functional_signals(
        view,
    )

    assert any(
        len(signal["affected_teams"]) >= 4
        for signal in signals
    )