from typing import Any

from backend.app.repositories.farmer_repository import FarmerRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class FarmerService:
    """Business logic for farmer operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all farmers."""
        return FarmerRepository.get_all()

    @staticmethod
    def get_by_id(farmer_id: int) -> dict[str, Any]:
        """Return a farmer by ID."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        farmer = FarmerRepository.get_by_id(farmer_id)

        if farmer is None:
            raise NotFoundError(f"Farmer with ID {farmer_id} not found.")

        return farmer

    @staticmethod
    def create(
        full_name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any]:
        """Validate and create a farmer."""
        if not full_name or not full_name.strip():
            raise ValidationError("Farmer name is required.")

        if not phone or not phone.strip():
            raise ValidationError("Farmer phone is required.")

        full_name = full_name.strip()
        phone = phone.strip()

        if email is not None:
            email = email.strip() or None

        if address is not None:
            address = address.strip() or None

        return FarmerRepository.create(
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
        )

    @staticmethod
    def update(
        farmer_id: int,
        full_name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any]:
        """Validate and update a farmer."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if not full_name or not full_name.strip():
            raise ValidationError("Farmer name is required.")

        if not phone or not phone.strip():
            raise ValidationError("Farmer phone is required.")

        full_name = full_name.strip()
        phone = phone.strip()

        if email is not None:
            email = email.strip() or None

        if address is not None:
            address = address.strip() or None

        farmer = FarmerRepository.update(
            farmer_id=farmer_id,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
        )

        if farmer is None:
            raise NotFoundError(f"Farmer with ID {farmer_id} not found.")

        return farmer

    @staticmethod
    def delete(farmer_id: int) -> None:
        """Delete a farmer."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        deleted = FarmerRepository.delete(farmer_id)

        if not deleted:
            raise NotFoundError(f"Farmer with ID {farmer_id} not found.")