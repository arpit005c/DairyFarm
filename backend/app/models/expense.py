from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass
class Expense:
    """Domain model representing a farm expense."""

    expense_id: int | None
    farmer_id: int
    expense_date: date
    category: str
    amount: Decimal
    description: str | None = None
    created_at: datetime | None = None