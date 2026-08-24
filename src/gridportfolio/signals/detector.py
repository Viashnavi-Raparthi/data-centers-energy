"""
Portfolio signal detection.

The key difference between this and ordinary anomaly detection:

    ordinary anomaly detection:
        "Something changed."

    GridPortfolio:
        "Something changed, here is who it affects, and here is
         why the combination matters."
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pandas as pd

from gridportfolio.portfolio.metrics import build_metric_table


def detect_cross_functional_signals(
    cross_functional_view: pd.DataFrame,
) -> list[dict]:
    """
    Detect cross-functional portfolio signals.

    Signals are generated using a risk-component score rather than
    requiring every possible condition to be simultaneously true.

    This allows the system to identify meaningful combinations such as:

        high forecast uncertainty
        + elevated market exposure
        + expiring renewable coverage

    even when one component is not independently extreme.
    """

    metrics = build_metric_table(
        cross_functional_view,
    )

    signals: list[dict] = []

    for _, row in metrics.iterrows():

        # -----------------------------------------------------------
        # Individual risk components
        # -----------------------------------------------------------

        load_growth_signal = (
            row["current_load_mw"]
            > row["forecast_load_mw"]
        )

        forecast_signal = (
            row["forecast_uncertainty"] >= 0.10
        )

        market_signal = (
            row["market_risk"] >= 0.25
        )

        contract_signal = (
            row["contract_expiration_risk"] >= 0.25
        )

        coverage_signal = (
            row["contract_coverage"] < 0.80
        )

        renewable_signal = (
            row["renewable_coverage"] < 0.80
        )

        # -----------------------------------------------------------
        # Composite cross-functional exposure score
        # -----------------------------------------------------------

        component_score = sum(
            [
                load_growth_signal,
                forecast_signal,
                market_signal,
                contract_signal,
                coverage_signal,
                renewable_signal,
            ]
        )

        # Require at least three independent indicators.
        if component_score < 3:
            continue

        # -----------------------------------------------------------
        # Determine affected teams
        # -----------------------------------------------------------

        affected_teams = [
            "Asset Management",
            "Data & Analytics",
        ]

        if market_signal:
            affected_teams.append("Wholesale")

        if contract_signal or renewable_signal or coverage_signal:
            affected_teams.append("Origination")

        if contract_signal or coverage_signal or renewable_signal:
            affected_teams.append("Procurement")

        # -----------------------------------------------------------
        # Build explanation
        # -----------------------------------------------------------

        reasons: list[str] = []

        if load_growth_signal:
            reasons.append(
                "current load is above forecast"
            )

        if forecast_signal:
            reasons.append(
                "forecast uncertainty is elevated"
            )

        if market_signal:
            reasons.append(
                "market volatility/exposure is elevated"
            )

        if contract_signal:
            reasons.append(
                "a renewable contract is approaching expiration"
            )

        if coverage_signal:
            reasons.append(
                "contract coverage is below the target level"
            )

        if renewable_signal:
            reasons.append(
                "renewable coverage is below the target level"
            )

        days_to_expiration = row.get(
            "days_to_contract_expiration"
        )

        if pd.notna(days_to_expiration):
            expiration_text = (
                f"the nearest contract expires in "
                f"{int(days_to_expiration)} days"
            )
        else:
            expiration_text = (
                "contract expiration timing requires validation"
            )

        description = (
            f"{row['asset_code']} shows a cross-functional "
            f"procurement exposure: "
            f"{'; '.join(reasons)}; "
            f"{expiration_text}."
        )

        # -----------------------------------------------------------
        # Confidence
        # -----------------------------------------------------------

        confidence = min(
            0.99,
            0.65 + (component_score * 0.05),
        )

        signals.append(
            {
                "signal_id": (
                    f"SIG-{uuid4().hex[:8]}"
                ),
                "title": (
                    "Emerging procurement exposure "
                    f"for {row['asset_code']}"
                ),
                "description": description,
                "detected_at": datetime.utcnow(),
                "asset_code": row["asset_code"],
                "market_code": row.get(
                    "market_code"
                ),
                "affected_teams": affected_teams,
                "components": [
                    "load_growth",
                    "forecast_uncertainty",
                    "market_volatility",
                    "contract_expiration",
                    "contract_coverage",
                    "renewable_coverage",
                ],
                "confidence": confidence,
                "business_impact": (
                    "Potential renewable coverage gap, "
                    "increased market exposure, and a need "
                    "for coordinated procurement action."
                ),
                "recommended_next_step": (
                    "Coordinate Asset Management, Analytics, "
                    "Wholesale, Origination, and Procurement "
                    "to validate the exposure and evaluate "
                    "replacement or sourcing options."
                ),
            }
        )

    return signals
