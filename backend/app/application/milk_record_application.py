from typing import Any

from backend.app.services.milk_record_service import MilkRecordService


class MilkRecordApplication:
    """Application use cases for milk record operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all milk records."""
        return MilkRecordService.get_all()

    @staticmethod
    def get_by_id(milk_record_id: int) -> dict[str, Any]:
        """Return a milk record by ID."""
        return MilkRecordService.get_by_id(milk_record_id)

    @staticmethod
    def get_by_cattle_id(cattle_id: int) -> list[dict[str, Any]]:
        """Return all milk records for cattle."""
        return MilkRecordService.get_by_cattle_id(cattle_id)

    @staticmethod
    def create(
        cattle_id: int,
        record_date: Any,
        session: str,
        quantity_litres: float,
    ) -> dict[str, Any]:
        """Create a milk record through the service layer."""
        return MilkRecordService.create(
            cattle_id=cattle_id,
            record_date=record_date,
            session=session,
            quantity_litres=quantity_litres,
        )

    @staticmethod
    def update(
        milk_record_id: int,
        cattle_id: int,
        record_date: Any,
        session: str,
        quantity_litres: float,
    ) -> dict[str, Any]:
        """Update a milk record through the service layer."""
        return MilkRecordService.update(
            milk_record_id=milk_record_id,
            cattle_id=cattle_id,
            record_date=record_date,
            session=session,
            quantity_litres=quantity_litres,
        )

    @staticmethod
    def delete(milk_record_id: int) -> None:
        """Delete a milk record through the service layer."""
        MilkRecordService.delete(milk_record_id)