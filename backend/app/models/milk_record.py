from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class MilkRecord:
    """Domain model representing a cattle milk production record."""

    milk_record_id: int | None
    cattle_id: int
    record_date: date
    session: str
    quantity_litres: Decimal
    created_at: datetime | None = None