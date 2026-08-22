"""
Cross-team signal synthesis.

Transforms independent specialist observations into one
portfolio-level business narrative.
"""

from __future__ import annotations


TEAM_RESPONSIBILITIES = {
    "Asset Management": [
        "asset state",
        "load",
        "availability",
        "operations",
    ],
    "Data & Analytics": [
        "forecasting",
        "modeling",
        "data quality",
        "analytics",
    ],
    "Wholesale": [
        "market exposure",
        "market prices",
        "hedging",
        "market risk",
    ],
    "Origination": [
        "contracts",
        "renewable supply",
        "counterparties",
        "commercial opportunities",
    ],
    "Procurement": [
        "sourcing",
        "procurement execution",
        "supplier selection",
    ],
    "Program Management": [
        "dependencies",
        "execution",
        "ownership",
        "operating cadence",
    ],
}


def identify_team_roles(
    teams: list[str],
) -> dict[str, list[str]]:
    """Return the responsibilities relevant to each team."""

    return {
        team: TEAM_RESPONSIBILITIES.get(
            team,
            [],
        )
        for team in teams
    }


def build_signal_narrative(
    signal: dict,
) -> str:
    """
    Create the human-readable explanation of a cross-team signal.
    """

    teams = ", ".join(
        signal["affected_teams"],
    )

    return (
        f"{signal['title']}. "
        f"This signal spans {teams}. "
        f"The issue is not isolated to a single function: "
        f"operational load growth increases the importance of "
        f"forecast accuracy, while market volatility and contract "
        f"timing change the commercial exposure. "
        f"GridPortfolio therefore treats this as a coordinated "
        f"portfolio decision rather than an individual team alert."
    )