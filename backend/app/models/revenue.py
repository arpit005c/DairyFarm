from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class Revenue:
    """Domain model representing milk sales revenue."""

    revenue_id: int | None
    farmer_id: int
    sale_date: date
    quantity_litres: Decimal
    price_per_litre: Decimal
    buyer_name: str | None = None
    created_at: datetime | None = None