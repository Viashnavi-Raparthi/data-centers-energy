"""
End-to-end GridPortfolio demonstration.

Run:

    python -m gridportfolio.pipeline

This executes:

    1. Generate fragmented source systems
    2. Assess data quality
    3. Integrate the sources
    4. Build canonical portfolio metrics
    5. Calculate portfolio health
    6. Detect cross-team signals
    7. Identify risks
    8. Identify organizational dependencies
    9. Generate executive decision brief
   10. Evaluate the AI output

The final output demonstrates the core thesis:

    Different teams can own different systems.

    Leadership should still have one coherent view of the portfolio.
"""

from __future__ import annotations

import json

from gridportfolio.agents.orchestrator import (
    PortfolioAgentOrchestrator,
)
from gridportfolio.data.generators import (
    generate_all_sources,
)
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
from gridportfolio.governance.evaluation import (
    evaluate_brief,
    evaluate_signal,
)


def run_demo() -> dict:
    """Run the complete portfolio integration demo."""

    # ---------------------------------------------------------------
    # 1. Generate fragmented enterprise source systems
    # ---------------------------------------------------------------

    sources = generate_all_sources()

    # ---------------------------------------------------------------
    # 2. Integrate source systems
    # ---------------------------------------------------------------

    integrated = integrate_sources(
        sources,
    )

    # ---------------------------------------------------------------
    # 3. Build canonical cross-functional portfolio view
    # ---------------------------------------------------------------

    cross_functional = build_cross_functional_view(
        integrated,
    )

    # ---------------------------------------------------------------
    # 4. Build portfolio metrics
    # ---------------------------------------------------------------

    metrics = build_metric_table(
        cross_functional,
    )

    # ---------------------------------------------------------------
    # 5. Calculate portfolio health
    # ---------------------------------------------------------------

    health = calculate_portfolio_health(
        metrics,
    )

    # ---------------------------------------------------------------
    # 6. Detect cross-functional signals
    # ---------------------------------------------------------------

    signals = detect_cross_functional_signals(
        cross_functional,
    )

    # ---------------------------------------------------------------
    # 7. Run the decision-support agent
    # ---------------------------------------------------------------

    orchestrator = PortfolioAgentOrchestrator()

    agent_results = orchestrator.run(
        signals=signals,
        initiatives=integrated.initiatives,
        health=health,
    )

    # ---------------------------------------------------------------
    # 8. Evaluate generated AI outputs
    # ---------------------------------------------------------------

    signal_evaluations = [
        evaluate_signal(signal)
        for signal in agent_results["signals"]
    ]

    brief_evaluation = evaluate_brief(
        agent_results["brief"],
    )

    # ---------------------------------------------------------------
    # 9. Return complete demonstration result
    # ---------------------------------------------------------------

    return {
        "source_systems": list(
            sources.keys(),
        ),
        "data_quality": [
            {
                "dataset": quality_result.source_name,
                "score": quality_result.quality_score,
                "status": (
                    "healthy"
                    if quality_result.is_healthy
                    else "needs_attention"
                ),
            }
            for quality_result in integrated.quality
        ],
        "portfolio_health": {
            "overall": health.overall_score,
            "renewable_coverage": (
                health.renewable_coverage_score
            ),
            "forecast_stability": (
                health.forecast_stability_score
            ),
            "market_exposure": (
                health.market_exposure_score
            ),
            "contract_coverage": (
                health.contract_coverage_score
            ),
            "execution_health": (
                health.execution_health_score
            ),
            "explanation": health.explanation,
        },
        "cross_functional_records": len(
            cross_functional,
        ),
        "signals": agent_results["signals"],
        "risks": agent_results["risks"],
        "operating_cadence": agent_results["cadence"],
        "executive_brief": agent_results["brief"],
        "evaluation": {
            "signals": signal_evaluations,
            "brief": brief_evaluation,
        },
    }


def main() -> None:
    """CLI entry point."""

    result = run_demo()

    print("=" * 80)
    print("GRIDPORTFOLIO — ENERGY INTEGRATION DEMONSTRATION")
    print("=" * 80)

    print("\nSOURCE SYSTEMS")

    for source in result["source_systems"]:
        print(f"  • {source}")

    print("\nDATA QUALITY")

    for quality in result["data_quality"]:
        print(
            f"  {quality['dataset']}: "
            f"{quality['score']:.1%} "
            f"({quality['status']})"
        )

    print("\nPORTFOLIO HEALTH")

    health = result["portfolio_health"]

    print(
        f"  Overall: {health['overall']:.1f}/100"
    )

    print(
        f"  Contract Coverage: "
        f"{health['contract_coverage']:.1f}"
    )

    print(
        f"  Market Exposure: "
        f"{health['market_exposure']:.1f}"
    )

    print(
        f"  Forecast Stability: "
        f"{health['forecast_stability']:.1f}"
    )

    print(
        f"  Renewable Coverage: "
        f"{health['renewable_coverage']:.1f}"
    )

    print(
        f"  Execution Health: "
        f"{health['execution_health']:.1f}"
    )

    print("\nCROSS-TEAM SIGNALS")

    if not result["signals"]:
        print("  No cross-functional signals detected.")

    for signal in result["signals"]:
        print(
            f"\n  [{signal['signal_id']}] "
            f"{signal['title']}"
        )

        print(
            f"  Teams: "
            f"{', '.join(signal['affected_teams'])}"
        )

        print(
            f"  Confidence: "
            f"{signal['confidence']:.0%}"
        )

        print(
            f"  Why it matters:\n"
            f"    {signal['description']}"
        )

    print("\nEXECUTIVE BRIEF")

    brief = result["executive_brief"]

    print(
        f"\n  {brief['headline']}"
    )

    print(
        f"\n  Portfolio Health: "
        f"{brief['portfolio_health']:.1f}/100"
    )

    print("\n  What Changed:")

    if brief["what_changed"]:
        for change in brief["what_changed"]:
            print(
                f"    • {change}"
            )
    else:
        print("    • None identified.")

    print("\n  Top Risks:")

    if brief["top_risks"]:
        for risk in brief["top_risks"]:
            print(
                f"    • {risk}"
            )
    else:
        print("    • None identified.")

    print("\n  Cross-Team Impacts:")

    if brief["cross_team_impacts"]:
        for impact in brief["cross_team_impacts"]:
            print(
                f"    • {impact}"
            )
    else:
        print("    • None identified.")

    print("\n  Decisions Needed:")

    if brief["decisions_needed"]:
        for decision in brief["decisions_needed"]:
            print(
                f"    • {decision}"
            )
    else:
        print("    • None identified.")

    print("\n  Recommended Actions:")

    for action in brief["recommended_actions"]:
        print(
            f"    • {action}"
        )

    print(
        "\n  Human Review Required: "
        f"{brief['human_review_required']}"
    )

    print(
        "  Approved: "
        f"{brief['approved']}"
    )

    print("\nAI EVALUATION")

    print(
        f"  Brief quality: "
        f"{result['evaluation']['brief']['score']:.0%}"
    )

    print(
        "\n" + "=" * 80
    )

    print(
        json.dumps(
            result,
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()