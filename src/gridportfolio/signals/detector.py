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
    Detect signals that span multiple organizational functions.
    """

    metrics = build_metric_table(
        cross_functional_view,
    )

    signals: list[dict] = []

    for _, row in metrics.iterrows():

        load_growth_signal = (
            row["current_load_mw"]
            > row["forecast_load_mw"] * 1.05
        )

        forecast_signal = (
            row["forecast_uncertainty"] > 0.25
        )

        market_signal = (
            row["market_risk"] > 0.50
        )

        contract_signal = (
            row["contract_expiration_risk"] > 0.60
        )

        if (
            load_growth_signal
            and forecast_signal
            and market_signal
            and contract_signal
        ):
            signals.append(
                {
                    "signal_id": f"SIG-{uuid4().hex[:8]}",
                    "title": (
                        "Emerging procurement exposure "
                        f"for {row['asset_code']}"
                    ),
                    "description": (
                        f"{row['asset_code']} is experiencing "
                        f"elevated load / forecast uncertainty "
                        f"while market volatility is elevated "
                        f"and its renewable contract expires in "
                        f"{int(row['days_to_contract_expiration'])} days."
                    ),
                    "detected_at": datetime.utcnow(),
                    "asset_code": row["asset_code"],
                    "market_code": row["market_code"],
                    "affected_teams": [
                        "Asset Management",
                        "Data & Analytics",
                        "Wholesale",
                        "Origination",
                        "Procurement",
                    ],
                    "components": [
                        "load_growth",
                        "forecast_uncertainty",
                        "market_volatility",
                        "contract_expiration",
                    ],
                    "confidence": 0.91,
                    "business_impact": (
                        "Potential renewable coverage gap and "
                        "increased market exposure."
                    ),
                    "recommended_next_step": (
                        "Coordinate Origination, Wholesale, "
                        "Analytics, and Procurement to evaluate "
                        "the procurement window before contract "
                        "expiration."
                    ),
                }
            )

    return signals