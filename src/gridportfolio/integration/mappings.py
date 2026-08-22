"""
Source-to-canonical mappings.

This file is where fragmented organizational definitions become
explicit mappings into the shared portfolio model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FieldMapping:
    """Mapping from source terminology to canonical terminology."""

    source_team: str
    source_field: str
    canonical_field: str
    transformation: str | None = None


FIELD_MAPPINGS = [
    FieldMapping(
        source_team="Asset Management",
        source_field="asset_code",
        canonical_field="asset_id",
    ),
    FieldMapping(
        source_team="Asset Management",
        source_field="installed_capacity_mw",
        canonical_field="capacity_mw",
    ),
    FieldMapping(
        source_team="Asset Management",
        source_field="current_load_mw",
        canonical_field="load_mw",
    ),
    FieldMapping(
        source_team="Analytics",
        source_field="predicted_load_mw",
        canonical_field="forecast_mw",
    ),
    FieldMapping(
        source_team="Wholesale",
        source_field="real_time_price_usd_mwh",
        canonical_field="market_price_per_mwh",
    ),
    FieldMapping(
        source_team="Origination",
        source_field="contract_code",
        canonical_field="contract_id",
    ),
    FieldMapping(
        source_team="Origination",
        source_field="contracted_mw",
        canonical_field="contract_capacity_mw",
    ),
]


def get_mapping(
    source_team: str,
    source_field: str,
) -> FieldMapping | None:
    """Return the canonical mapping for a source field."""

    for mapping in FIELD_MAPPINGS:
        if (
            mapping.source_team == source_team
            and mapping.source_field == source_field
        ):
            return mapping

    return None