"""
Integration Agent.

The Integration Agent asks:

    "What signals from different teams are actually connected?"

This is the most important agent for the Meta-style use case.
"""

from __future__ import annotations

from gridportfolio.signals.cross_team import (
    build_signal_narrative,
)


class IntegrationAgent:
    """Connects fragmented specialist observations."""

    name = "integration_agent"

    def analyze(
        self,
        signals: list[dict],
    ) -> list[dict]:
        """Enrich detected signals with organizational context."""

        enriched = []

        for signal in signals:
            enriched_signal = signal.copy()

            enriched_signal["narrative"] = (
                build_signal_narrative(
                    signal,
                )
            )

            enriched_signal["integration_question"] = (
                "Which teams need to coordinate because of this signal?"
            )

            enriched.append(
                enriched_signal,
            )

        return enriched