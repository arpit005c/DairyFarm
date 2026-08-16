from typing import Any

from backend.app.services.farmer_service import FarmerService


class FarmerApplication:
    """Application use cases for farmer operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all farmers."""
        return FarmerService.get_all()

    @staticmethod
    def get_by_id(farmer_id: int) -> dict[str, Any]:
        """Return a farmer by ID."""
        return FarmerService.get_by_id(farmer_id)

    @staticmethod
    def create(
        full_name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any]:
        """Create a farmer through the service layer."""
        return FarmerService.create(
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
        """Update a farmer through the service layer."""
        return FarmerService.update(
            farmer_id=farmer_id,
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
        )

    @staticmethod
    def delete(farmer_id: int) -> None:
        """Delete a farmer through the service layer."""
        FarmerService.delete(farmer_id)