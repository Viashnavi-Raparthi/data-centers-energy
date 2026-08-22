"""
Risk Agent.

Converts cross-team signals into prioritized portfolio risks.
"""

from __future__ import annotations


class RiskAgent:
    """Prioritizes and explains portfolio risk."""

    name = "risk_agent"

    def evaluate(
        self,
        signals: list[dict],
    ) -> list[dict]:
        risks = []

        for signal in signals:
            risk_score = (
                signal.get("confidence", 0)
                * 0.5
                + 0.5
            )

            risks.append(
                {
                    "risk_id": f"RISK-{signal['signal_id']}",
                    "title": signal["title"],
                    "description": signal["description"],
                    "score": min(
                        1.0,
                        risk_score,
                    ),
                    "affected_teams": signal[
                        "affected_teams"
                    ],
                    "business_impact": signal[
                        "business_impact"
                    ],
                    "evidence": signal[
                        "components"
                    ],
                }
            )

        return risks