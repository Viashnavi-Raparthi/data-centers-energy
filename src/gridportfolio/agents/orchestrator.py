"""
Agent orchestrator.

Coordinates the specialized agents.

The orchestration pattern is:

    Integration Agent
          ↓
    Risk Agent
          ↓
    Operating Cadence Agent
          ↓
    Decision Briefing Agent

Each agent has a bounded responsibility.
"""

from __future__ import annotations

from gridportfolio.agents.briefing import (
    DecisionBriefingAgent,
)
from gridportfolio.agents.cadence import (
    CadenceAgent,
)
from gridportfolio.agents.integration import (
    IntegrationAgent,
)
from gridportfolio.agents.risk import (
    RiskAgent,
)


class PortfolioAgentOrchestrator:
    """Run the complete decision-support workflow."""

    def __init__(self) -> None:
        self.integration_agent = IntegrationAgent()
        self.risk_agent = RiskAgent()
        self.cadence_agent = CadenceAgent()
        self.briefing_agent = DecisionBriefingAgent()

    def run(
        self,
        signals,
        initiatives,
        health,
    ) -> dict:
        """
        Execute the agent workflow.
        """

        integrated = self.integration_agent.analyze(
            signals,
        )

        risks = self.risk_agent.evaluate(
            integrated,
        )

        cadence = self.cadence_agent.evaluate(
            integrated,
            initiatives,
        )

        brief = self.briefing_agent.create_brief(
            health,
            integrated,
            risks,
            cadence,
        )

        return {
            "signals": integrated,
            "risks": risks,
            "cadence": cadence,
            "brief": brief,
        }