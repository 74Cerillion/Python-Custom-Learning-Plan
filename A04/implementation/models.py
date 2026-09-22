from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MarketObservation:
    """Strongly typed internal domain object."""
    symbol: str
    price: float
    timestamp: datetime


@dataclass(frozen=True)
class IngestionContext:
    """Tracing context carried across operations."""
    correlation_id: str
    api_key: Optional[str] = None