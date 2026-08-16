from dataclasses import dataclass
from datetime import datetime


@dataclass
class Farmer:
    """Domain model representing a dairy farmer."""

    farmer_id: int | None
    full_name: str
    phone: str
    email: str | None = None
    address: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None