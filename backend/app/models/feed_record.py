from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class FeedRecord:
    """Domain model representing a cattle/farm feed record."""

    feed_record_id: int | None
    farmer_id: int
    record_date: date
    feed_type: str
    quantity_kg: Decimal
    cost: Decimal
    cattle_id: int | None = None
    created_at: datetime | None = None