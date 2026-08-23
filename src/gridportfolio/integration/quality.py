"""
Data-quality assessment for integrated portfolio sources.

The quality layer intentionally operates independently of any specific
source system. It provides a common quality vocabulary across datasets
coming from asset management, analytics, wholesale, origination,
procurement, finance, and other specialist functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd


@dataclass
class DataQualityResult:
    """
    Quality assessment for a single dataset.

    Scores are normalized between 0 and 1.
    """

    source_name: str

    row_count: int

    column_count: int

    missing_rate: float

    duplicate_rate: float

    quality_score: float

    issues: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_healthy(self) -> bool:
        """Return whether the dataset passes the basic quality threshold."""

        return self.quality_score >= 0.80


def _safe_duplicate_rate(
    dataframe: pd.DataFrame,
) -> float:
    """
    Calculate duplicate-row rate safely.

    Pandas' standard DataFrame.duplicated() requires values to be
    hashable. Real-world enterprise datasets may contain nested values
    such as lists, dictionaries, or other Python objects.

    To make quality assessment robust, object values are normalized into
    deterministic representations before duplicate detection.
    """

    if dataframe.empty:
        return 0.0

    normalized = dataframe.copy()

    for column in normalized.columns:
        if normalized[column].dtype == "object":
            normalized[column] = normalized[column].map(
                _normalize_for_hashing
            )

    try:
        return float(normalized.duplicated().mean())

    except TypeError:
        # Final defensive fallback for unusual Python objects.
        serialized = normalized.astype(str)
        return float(serialized.duplicated().mean())


def _normalize_for_hashing(
    value: Any,
) -> Any:
    """
    Convert nested Python objects into hashable deterministic values.

    Lists become tuples.
    Dictionaries become sorted tuples of key/value pairs.
    Sets become sorted tuples.
    Nested structures are handled recursively.
    """

    if isinstance(value, dict):
        return tuple(
            sorted(
                (
                    str(key),
                    _normalize_for_hashing(item),
                )
                for key, item in value.items()
            )
        )

    if isinstance(value, (list, tuple)):
        return tuple(
            _normalize_for_hashing(item)
            for item in value
        )

    if isinstance(value, set):
        normalized_items = [
            _normalize_for_hashing(item)
            for item in value
        ]

        return tuple(
            sorted(
                normalized_items,
                key=str,
            )
        )

    return value


def _calculate_missing_rate(
    dataframe: pd.DataFrame,
) -> float:
    """Calculate the percentage of missing cells."""

    if dataframe.empty or dataframe.shape[1] == 0:
        return 0.0

    return float(
        dataframe.isna().mean().mean()
    )


def _build_quality_score(
    missing_rate: float,
    duplicate_rate: float,
) -> float:
    """
    Build a simple interpretable quality score.

    Missingness and duplication are currently the two baseline quality
    dimensions. Additional checks can be incorporated later without
    changing the public interface.
    """

    score = (
        1.0
        - (missing_rate * 0.60)
        - (duplicate_rate * 0.40)
    )

    return max(
        0.0,
        min(1.0, score),
    )


def assess_dataframe_quality(
    name: str,
    dataframe: pd.DataFrame,
) -> DataQualityResult:
    """
    Assess the quality of a single DataFrame.

    Parameters
    ----------
    name:
        Logical source or dataset name.

    dataframe:
        Source data to assess.

    Returns
    -------
    DataQualityResult
        Structured quality assessment.
    """

    row_count = len(dataframe)

    column_count = len(dataframe.columns)

    missing_rate = _calculate_missing_rate(
        dataframe
    )

    duplicate_rate = _safe_duplicate_rate(
        dataframe
    )

    quality_score = _build_quality_score(
        missing_rate=missing_rate,
        duplicate_rate=duplicate_rate,
    )

    issues: list[str] = []

    if missing_rate > 0.10:
        issues.append(
            f"High missingness: {missing_rate:.1%}"
        )

    if duplicate_rate > 0.05:
        issues.append(
            f"High duplicate rate: {duplicate_rate:.1%}"
        )

    if row_count == 0:
        issues.append(
            "Dataset contains no rows."
        )

    if column_count == 0:
        issues.append(
            "Dataset contains no columns."
        )

    return DataQualityResult(
        source_name=name,
        row_count=row_count,
        column_count=column_count,
        missing_rate=missing_rate,
        duplicate_rate=duplicate_rate,
        quality_score=quality_score,
        issues=issues,
    )


def assess_all_sources(
    sources: dict[str, pd.DataFrame],
) -> dict[str, DataQualityResult]:
    """
    Assess every source dataset.

    Parameters
    ----------
    sources:
        Mapping from logical source name to DataFrame.

    Returns
    -------
    dict[str, DataQualityResult]
        Quality results keyed by source name.
    """

    results: dict[str, DataQualityResult] = {}

    for name, dataframe in sources.items():
        results[name] = assess_dataframe_quality(
            name=name,
            dataframe=dataframe,
        )

    return results