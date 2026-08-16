from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Cattle:
    """Domain model representing cattle owned by a farmer."""

    cattle_id: int | None
    farmer_id: int
    tag_number: str
    gender: str
    name: str | None = None
    breed: str | None = None
    date_of_birth: date | None = None
    status: str = "active"
    created_at: datetime | None = None
    updated_at: datetime | None = None