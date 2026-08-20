from typing import Any

from backend.app.repositories.feed_record_repository import FeedRecordRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class FeedRecordService:
    """Business logic for feed record operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all feed records."""
        return FeedRecordRepository.get_all()

    @staticmethod
    def get_by_id(feed_record_id: int) -> dict[str, Any]:
        """Return a feed record by ID."""
        if feed_record_id <= 0:
            raise ValidationError(
                "Feed record ID must be a positive integer."
            )

        record = FeedRecordRepository.get_by_id(feed_record_id)

        if record is None:
            raise NotFoundError(
                f"Feed record with ID {feed_record_id} not found."
            )

        return record

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all feed records for a farmer."""
        if farmer_id <= 0:
            raise ValidationError(
                "Farmer ID must be a positive integer."
            )

        return FeedRecordRepository.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        record_date: Any,
        feed_type: str,
        quantity_kg: float,
        cost: float,
        cattle_id: int | None = None,
    ) -> dict[str, Any]:
        """Validate and create a feed record."""
        if farmer_id <= 0:
            raise ValidationError(
                "Farmer ID must be a positive integer."
            )

        if cattle_id is not None and cattle_id <= 0:
            raise ValidationError(
                "Cattle ID must be a positive integer."
            )

        if record_date is not None and isinstance(record_date, str):
            if not record_date.strip():
                raise ValidationError("Feed record date cannot be empty.")
            record_date = record_date.strip()

        if not feed_type or not feed_type.strip():
            raise ValidationError("Feed type is required.")

        if quantity_kg < 0:
            raise ValidationError(
                "Feed quantity cannot be negative."
            )

        if cost < 0:
            raise ValidationError(
                "Feed cost cannot be negative."
            )

        feed_type = feed_type.strip()

        return FeedRecordRepository.create(
            farmer_id=farmer_id,
            cattle_id=cattle_id,
            record_date=record_date,
            feed_type=feed_type,
            quantity_kg=quantity_kg,
            cost=cost,
        )

    @staticmethod
    def update(
        feed_record_id: int,
        farmer_id: int,
        record_date: Any,
        feed_type: str,
        quantity_kg: float,
        cost: float,
        cattle_id: int | None = None,
    ) -> dict[str, Any]:
        """Validate and update a feed record."""
        if feed_record_id <= 0:
            raise ValidationError(
                "Feed record ID must be a positive integer."
            )

        if farmer_id <= 0:
            raise ValidationError(
                "Farmer ID must be a positive integer."
            )

        if cattle_id is not None and cattle_id <= 0:
            raise ValidationError(
                "Cattle ID must be a positive integer."
            )

        if record_date is not None and isinstance(record_date, str):
            if not record_date.strip():
                raise ValidationError("Feed record date cannot be empty.")
            record_date = record_date.strip()

        if not feed_type or not feed_type.strip():
            raise ValidationError("Feed type is required.")

        if quantity_kg < 0:
            raise ValidationError(
                "Feed quantity cannot be negative."
            )

        if cost < 0:
            raise ValidationError(
                "Feed cost cannot be negative."
            )

        feed_type = feed_type.strip()

        record = FeedRecordRepository.update(
            feed_record_id=feed_record_id,
            farmer_id=farmer_id,
            cattle_id=cattle_id,
            record_date=record_date,
            feed_type=feed_type,
            quantity_kg=quantity_kg,
            cost=cost,
        )

        if record is None:
            raise NotFoundError(
                f"Feed record with ID {feed_record_id} not found."
            )

        return record

    @staticmethod
    def delete(feed_record_id: int) -> None:
        """Delete a feed record."""
        if feed_record_id <= 0:
            raise ValidationError(
                "Feed record ID must be a positive integer."
            )

        deleted = FeedRecordRepository.delete(feed_record_id)

        if not deleted:
            raise NotFoundError(
                f"Feed record with ID {feed_record_id} not found."
            )