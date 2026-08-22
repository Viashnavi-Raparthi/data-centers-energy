from gridportfolio.agents.orchestrator import (
    PortfolioAgentOrchestrator,
)
from gridportfolio.data.generators import generate_all_sources
from gridportfolio.integration.pipeline import (
    build_cross_functional_view,
    integrate_sources,
)
from gridportfolio.portfolio.health import (
    calculate_portfolio_health,
)
from gridportfolio.portfolio.metrics import (
    build_metric_table,
)
from gridportfolio.signals.detector import (
    detect_cross_functional_signals,
)


def test_agent_orchestration() -> None:
    sources = generate_all_sources()

    portfolio = integrate_sources(
        sources,
    )

    view = build_cross_functional_view(
        portfolio,
    )

    metrics = build_metric_table(
        view,
    )

    health = calculate_portfolio_health(
        metrics,
    )

    signals = detect_cross_functional_signals(
        view,
    )

    orchestrator = PortfolioAgentOrchestrator()

    result = orchestrator.run(
        signals=signals,
        initiatives=portfolio.initiatives,
        health=health,
    )

    assert "signals" in result
    assert "risks" in result
    assert "cadence" in result
    assert "brief" in result

    assert result["brief"]["human_review_required"] is True