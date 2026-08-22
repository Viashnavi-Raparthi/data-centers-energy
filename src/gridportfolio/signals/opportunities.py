"""
Opportunity detection.

The system should not only identify things going wrong.

It should also identify situations where coordinated action could
create value.
"""

from __future__ import annotations


def detect_procurement_opportunities(
    signal: dict,
    market_price: float,
    contract_price: float,
) -> list[dict]:
    """
    Identify potential commercial opportunity.

    This is decision support, not autonomous procurement.
    """

    opportunities: list[dict] = []

    if (
        market_price < contract_price
        and signal["confidence"] > 0.75
    ):
        opportunities.append(
            {
                "title": "Potential favorable procurement window",
                "description": (
                    "Current market pricing is below the existing "
                    "contract reference price while a contract "
                    "replacement decision is approaching."
                ),
                "signal_id": signal["signal_id"],
                "teams": [
                    "Origination",
                    "Wholesale",
                    "Procurement",
                ],
                "recommended_action": (
                    "Evaluate procurement options and market "
                    "timing before executing a replacement."
                ),
                "requires_human_review": True,
            }
        )

    return opportunities