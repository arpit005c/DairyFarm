from typing import Any

from backend.app.services.cattle_service import CattleService


class CattleApplication:
    """Application use cases for cattle operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all cattle."""
        return CattleService.get_all()

    @staticmethod
    def get_by_id(cattle_id: int) -> dict[str, Any]:
        """Return cattle by ID."""
        return CattleService.get_by_id(cattle_id)

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all cattle belonging to a farmer."""
        return CattleService.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        tag_number: str,
        gender: str,
        name: str | None = None,
        breed: str | None = None,
        date_of_birth: Any | None = None,
        status: str = "active",
    ) -> dict[str, Any]:
        """Create cattle through the service layer."""
        return CattleService.create(
            farmer_id=farmer_id,
            tag_number=tag_number,
            gender=gender,
            name=name,
            breed=breed,
            date_of_birth=date_of_birth,
            status=status,
        )

    @staticmethod
    def update(
        cattle_id: int,
        farmer_id: int,
        tag_number: str,
        gender: str,
        name: str | None = None,
        breed: str | None = None,
        date_of_birth: Any | None = None,
        status: str = "active",
    ) -> dict[str, Any]:
        """Update cattle through the service layer."""
        return CattleService.update(
            cattle_id=cattle_id,
            farmer_id=farmer_id,
            tag_number=tag_number,
            gender=gender,
            name=name,
            breed=breed,
            date_of_birth=date_of_birth,
            status=status,
        )

    @staticmethod
    def delete(cattle_id: int) -> None:
        """Delete cattle through the service layer."""
        CattleService.delete(cattle_id)