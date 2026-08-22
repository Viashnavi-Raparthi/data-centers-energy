"""
Evaluation framework for the AI decision-support layer.

The goal is not merely:

    "Did the LLM generate a good paragraph?"

The system should evaluate:

    factual grounding
    evidence coverage
    cross-team completeness
    recommendation quality
    appropriate human escalation
"""

from __future__ import annotations


def evaluate_signal(
    signal: dict,
) -> dict:
    """Evaluate whether a signal is sufficiently grounded."""

    checks = {
        "has_description": bool(
            signal.get("description")
        ),
        "has_affected_teams": bool(
            signal.get("affected_teams")
        ),
        "has_components": bool(
            signal.get("components")
        ),
        "has_confidence": signal.get(
            "confidence"
        )
        is not None,
    }

    score = sum(
        checks.values()
    ) / len(checks)

    return {
        "score": score,
        "checks": checks,
        "passed": score >= 0.75,
    }


def evaluate_brief(
    brief: dict,
) -> dict:
    """Evaluate executive-brief completeness."""

    required = [
        "headline",
        "what_changed",
        "top_risks",
        "cross_team_impacts",
        "decisions_needed",
        "recommended_actions",
    ]

    checks = {
        field: bool(brief.get(field))
        for field in required
    }

    score = sum(
        checks.values()
    ) / len(checks)

    return {
        "score": score,
        "checks": checks,
        "passed": score >= 0.80,
    }