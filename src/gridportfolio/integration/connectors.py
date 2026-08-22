"""
Source connectors.

For the open-source MVP these connectors consume pandas DataFrames.

The interface intentionally resembles what a production connector
would do: retrieve data from one specialist system and expose it to
the integration pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class SourceConnector(ABC):
    """Base connector interface."""

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load records from a source system."""
        raise NotImplementedError


class DataFrameConnector(SourceConnector):
    """Connector backed by an in-memory DataFrame."""

    def __init__(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        self.dataframe = dataframe

    def load(self) -> pd.DataFrame:
        return self.dataframe.copy()


class SourceRegistry:
    """
    Registry of specialist data sources.

    This models the integration manager's role:

        not owning every source,

        but knowing how all sources connect.
    """

    def __init__(self) -> None:
        self._connectors: dict[str, SourceConnector] = {}

    def register(
        self,
        name: str,
        connector: SourceConnector,
    ) -> None:
        self._connectors[name] = connector

    def load(
        self,
        name: str,
    ) -> pd.DataFrame:
        if name not in self._connectors:
            raise KeyError(
                f"No connector registered for '{name}'."
            )

        return self._connectors[name].load()

    def load_all(self) -> dict[str, pd.DataFrame]:
        return {
            name: connector.load()
            for name, connector in self._connectors.items()
        }