"""
Domain events — facts that happened in the domain, used for side-effect
decoupling (event-driven architecture).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class DomainEvent:
    """Base class for all domain events."""

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AnalysisRequested(DomainEvent):
    """A user submitted a new analysis request."""

    request_id: UUID
    user_id: str
    query: str


@dataclass
class AnalysisCompleted(DomainEvent):
    """An analysis finished processing."""

    request_id: UUID
    result: str


@dataclass
class MarketDataRefreshed(DomainEvent):
    """Market data was fetched and cached."""

    symbols: list[str]
    snapshot_count: int
