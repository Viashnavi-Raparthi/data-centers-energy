"""
Data loading utilities.

The open-source project uses synthetic data by default.

The interfaces are intentionally simple so real connectors can later
replace them without changing the portfolio logic.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from gridportfolio.config import get_settings


def save_source_data(
    data: dict[str, pd.DataFrame],
    directory: str | Path | None = None,
) -> dict[str, Path]:
    """Persist source datasets as CSV files."""

    settings = get_settings()

    target = Path(
        directory or settings.synthetic_data_directory,
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    paths: dict[str, Path] = {}

    for name, dataframe in data.items():
        path = target / f"{name}.csv"

        dataframe.to_csv(
            path,
            index=False,
        )

        paths[name] = path

    return paths


def load_source_data(
    directory: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """Load previously generated source datasets."""

    settings = get_settings()

    target = Path(
        directory or settings.synthetic_data_directory,
    )

    data: dict[str, pd.DataFrame] = {}

    for path in target.glob("*.csv"):
        data[path.stem] = pd.read_csv(path)

    return data