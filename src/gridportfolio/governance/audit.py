"""
AI governance and audit logging.

The AI system should be inspectable.

Every recommendation should be traceable to:

    source data
    detected signal
    evidence
    reasoning context
    human review
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AuditEvent:
    event_type: str
    timestamp: datetime
    actor: str
    description: str
    evidence_ids: list[str] = field(
        default_factory=list,
    )


class AuditLogger:
    """Simple in-memory audit logger for the MVP."""

    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def log(
        self,
        event_type: str,
        actor: str,
        description: str,
        evidence_ids: list[str] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_type=event_type,
            timestamp=datetime.utcnow(),
            actor=actor,
            description=description,
            evidence_ids=evidence_ids or [],
        )

        self.events.append(event)

        return event

    def all_events(self) -> list[AuditEvent]:
        return list(self.events)