from typing import Any

from backend.app.services.feed_record_service import FeedRecordService


class FeedRecordApplication:
    """Application use cases for feed record operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all feed records."""
        return FeedRecordService.get_all()

    @staticmethod
    def get_by_id(feed_record_id: int) -> dict[str, Any]:
        """Return a feed record by ID."""
        return FeedRecordService.get_by_id(feed_record_id)

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all feed records for a farmer."""
        return FeedRecordService.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        record_date: Any,
        feed_type: str,
        quantity_kg: float,
        cost: float,
        cattle_id: int | None = None,
    ) -> dict[str, Any]:
        """Create a feed record through the service layer."""
        return FeedRecordService.create(
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
        """Update a feed record through the service layer."""
        return FeedRecordService.update(
            feed_record_id=feed_record_id,
            farmer_id=farmer_id,
            cattle_id=cattle_id,
            record_date=record_date,
            feed_type=feed_type,
            quantity_kg=quantity_kg,
            cost=cost,
        )

    @staticmethod
    def delete(feed_record_id: int) -> None:
        """Delete a feed record through the service layer."""
        FeedRecordService.delete(feed_record_id)