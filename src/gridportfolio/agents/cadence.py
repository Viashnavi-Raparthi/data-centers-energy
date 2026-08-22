"""
Operating Cadence Agent.

This agent focuses on the organizational execution layer.

It asks:

    Who owns the issue?

    Who needs to participate?

    What dependency is blocking progress?

    What needs to happen next?

This demonstrates that GridPortfolio is more than analytics.
"""

from __future__ import annotations


class CadenceAgent:
    """Identifies ownership and execution dependencies."""

    name = "operating_cadence_agent"

    def evaluate(
        self,
        signals: list[dict],
        initiatives,
    ) -> list[dict]:
        results = []

        for signal in signals:
            relevant_initiatives = []

            for _, initiative in initiatives.iterrows():
                participating = initiative[
                    "participating_teams"
                ]

                if any(
                    team in signal["affected_teams"]
                    for team in participating
                ):
                    relevant_initiatives.append(
                        {
                            "initiative_code": initiative[
                                "initiative_code"
                            ],
                            "status": initiative[
                                "status"
                            ],
                            "blocker": initiative[
                                "blocker"
                            ],
                            "owner": initiative[
                                "primary_owner"
                            ],
                        }
                    )

            results.append(
                {
                    "signal_id": signal["signal_id"],
                    "teams": signal["affected_teams"],
                    "initiatives": relevant_initiatives,
                    "coordination_required": len(
                        signal["affected_teams"]
                    ) > 2,
                    "recommended_forum": (
                        "Weekly Energy Portfolio Review"
                    ),
                }
            )

        return results