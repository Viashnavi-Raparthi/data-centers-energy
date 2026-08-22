"""
Data-quality checks for integrated portfolio data.

Trust is a first-class requirement.

A leadership dashboard should be able to distinguish:

    "portfolio risk increased"

from:

    "portfolio risk appears higher because one source is stale."
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class QualityResult:
    dataset: str
    score: float
    status: str
    checks: list[str]


def assess_dataframe_quality(
    name: str,
    dataframe: pd.DataFrame,
) -> QualityResult:
    """Run basic quality checks."""

    checks: list[str] = []

    if dataframe.empty:
        return QualityResult(
            dataset=name,
            score=0.0,
            status="fail",
            checks=["Dataset is empty."],
        )

    checks.append("Dataset contains records.")

    null_fraction = dataframe.isna().mean().mean()

    if null_fraction == 0:
        checks.append("No missing values detected.")
        missing_score = 1.0
    else:
        checks.append(
            f"Average missing-value fraction: {null_fraction:.2%}."
        )
        missing_score = max(
            0.0,
            1.0 - null_fraction,
        )

    duplicate_fraction = (
        dataframe.duplicated().mean()
    )

    if duplicate_fraction == 0:
        checks.append("No duplicate rows detected.")
        duplicate_score = 1.0
    else:
        checks.append(
            f"Duplicate-row fraction: {duplicate_fraction:.2%}."
        )
        duplicate_score = max(
            0.0,
            1.0 - duplicate_fraction,
        )

    score = (
        missing_score * 0.6
        + duplicate_score * 0.4
    )

    status = (
        "pass"
        if score >= 0.95
        else "warning"
        if score >= 0.80
        else "fail"
    )

    return QualityResult(
        dataset=name,
        score=score,
        status=status,
        checks=checks,
    )


def assess_all_sources(
    data: dict[str, pd.DataFrame],
) -> list[QualityResult]:
    """Assess every source dataset."""

    return [
        assess_dataframe_quality(
            name,
            dataframe,
        )
        for name, dataframe in data.items()
    ]