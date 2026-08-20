from typing import Any

from backend.app.repositories.milk_record_repository import MilkRecordRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class MilkRecordService:
    """Business logic for milk record operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all milk records."""
        return MilkRecordRepository.get_all()

    @staticmethod
    def get_by_id(milk_record_id: int) -> dict[str, Any]:
        """Return a milk record by ID."""
        if milk_record_id <= 0:
            raise ValidationError(
                "Milk record ID must be a positive integer."
            )

        record = MilkRecordRepository.get_by_id(milk_record_id)

        if record is None:
            raise NotFoundError(
                f"Milk record with ID {milk_record_id} not found."
            )

        return record

    @staticmethod
    def get_by_cattle_id(cattle_id: int) -> list[dict[str, Any]]:
        """Return all milk records for cattle."""
        if cattle_id <= 0:
            raise ValidationError(
                "Cattle ID must be a positive integer."
            )

        return MilkRecordRepository.get_by_cattle_id(cattle_id)

    @staticmethod
    def create(
        cattle_id: int,
        record_date: Any,
        session: str,
        quantity_litres: float,
    ) -> dict[str, Any]:
        """Validate and create a milk record."""
        if cattle_id <= 0:
            raise ValidationError(
                "Cattle ID must be a positive integer."
            )

        if record_date is not None and isinstance(record_date, str):
            if not record_date.strip():
                raise ValidationError("Milk record date cannot be empty.")
            record_date = record_date.strip()

        if not session or not session.strip():
            raise ValidationError("Milk session is required.")

        if quantity_litres < 0:
            raise ValidationError(
                "Milk quantity cannot be negative."
            )

        session = session.strip()

        return MilkRecordRepository.create(
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
        """Validate and update a milk record."""
        if milk_record_id <= 0:
            raise ValidationError(
                "Milk record ID must be a positive integer."
            )

        if cattle_id <= 0:
            raise ValidationError(
                "Cattle ID must be a positive integer."
            )

        if record_date is not None and isinstance(record_date, str):
            if not record_date.strip():
                raise ValidationError("Milk record date cannot be empty.")
            record_date = record_date.strip()

        if not session or not session.strip():
            raise ValidationError("Milk session is required.")

        if quantity_litres < 0:
            raise ValidationError(
                "Milk quantity cannot be negative."
            )

        session = session.strip()

        record = MilkRecordRepository.update(
            milk_record_id=milk_record_id,
            cattle_id=cattle_id,
            record_date=record_date,
            session=session,
            quantity_litres=quantity_litres,
        )

        if record is None:
            raise NotFoundError(
                f"Milk record with ID {milk_record_id} not found."
            )

        return record

    @staticmethod
    def delete(milk_record_id: int) -> None:
        """Delete a milk record."""
        if milk_record_id <= 0:
            raise ValidationError(
                "Milk record ID must be a positive integer."
            )

        deleted = MilkRecordRepository.delete(milk_record_id)

        if not deleted:
            raise NotFoundError(
                f"Milk record with ID {milk_record_id} not found."
            )