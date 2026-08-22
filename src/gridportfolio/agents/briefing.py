"""
Executive Decision Briefing Agent.

Transforms portfolio state into leadership-ready narrative.

The brief focuses on:

    What changed?
    Why does it matter?
    Who is affected?
    What decision is needed?
    What should happen next?
"""

from __future__ import annotations

from datetime import datetime


class DecisionBriefingAgent:
    """Produces executive portfolio briefs."""

    name = "decision_briefing_agent"

    def create_brief(
        self,
        health,
        signals,
        risks,
        cadence,
    ) -> dict:
        top_risk = (
            max(
                risks,
                key=lambda x: x["score"],
            )
            if risks
            else None
        )

        decisions = []

        for signal in signals:
            decisions.append(
                (
                    "Evaluate procurement timing for "
                    f"{signal['asset_code']} and determine "
                    "whether to open a sourcing process."
                )
            )

        actions = [
            (
                "Origination + Wholesale: assess contract "
                "replacement options and market conditions."
            ),
            (
                "Analytics + Asset Management: validate the "
                "accelerating load forecast."
            ),
            (
                "Procurement: prepare sourcing options if "
                "replacement coverage is required."
            ),
        ]

        return {
            "brief_id": "BRIEF-LATEST",
            "generated_at": datetime.utcnow(),
            "headline": (
                "Cross-functional procurement exposure "
                "requires coordinated action."
            ),
            "portfolio_health": health.overall_score,
            "what_changed": [
                signal["description"]
                for signal in signals
            ],
            "top_risks": [
                top_risk["description"]
            ]
            if top_risk
            else [],
            "cross_team_impacts": [
                (
                    f"{item['signal_id']}: "
                    f"{', '.join(item['teams'])}"
                )
                for item in cadence
            ],
            "decisions_needed": decisions,
            "recommended_actions": actions,
            "human_review_required": True,
            "approved": False,
        }