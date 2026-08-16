from typing import Any

from backend.app.repositories.cattle_repository import CattleRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class CattleService:
    """Business logic for cattle operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all cattle."""
        return CattleRepository.get_all()

    @staticmethod
    def get_by_id(cattle_id: int) -> dict[str, Any]:
        """Return cattle by ID."""
        if cattle_id <= 0:
            raise ValidationError("Cattle ID must be a positive integer.")

        cattle = CattleRepository.get_by_id(cattle_id)

        if cattle is None:
            raise NotFoundError(f"Cattle with ID {cattle_id} not found.")

        return cattle

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all cattle belonging to a farmer."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        return CattleRepository.get_by_farmer_id(farmer_id)

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
        """Validate and create cattle."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if not tag_number or not tag_number.strip():
            raise ValidationError("Cattle tag number is required.")

        if not gender or not gender.strip():
            raise ValidationError("Cattle gender is required.")

        tag_number = tag_number.strip()
        gender = gender.strip()

        if name is not None:
            name = name.strip() or None

        if breed is not None:
            breed = breed.strip() or None

        if status is not None:
            status = status.strip() or "active"

        return CattleRepository.create(
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
        """Validate and update cattle."""
        if cattle_id <= 0:
            raise ValidationError("Cattle ID must be a positive integer.")

        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if not tag_number or not tag_number.strip():
            raise ValidationError("Cattle tag number is required.")

        if not gender or not gender.strip():
            raise ValidationError("Cattle gender is required.")

        tag_number = tag_number.strip()
        gender = gender.strip()

        if name is not None:
            name = name.strip() or None

        if breed is not None:
            breed = breed.strip() or None

        if status is not None:
            status = status.strip() or "active"

        cattle = CattleRepository.update(
            cattle_id=cattle_id,
            farmer_id=farmer_id,
            tag_number=tag_number,
            gender=gender,
            name=name,
            breed=breed,
            date_of_birth=date_of_birth,
            status=status,
        )

        if cattle is None:
            raise NotFoundError(f"Cattle with ID {cattle_id} not found.")

        return cattle

    @staticmethod
    def delete(cattle_id: int) -> None:
        """Delete cattle."""
        if cattle_id <= 0:
            raise ValidationError("Cattle ID must be a positive integer.")

        deleted = CattleRepository.delete(cattle_id)

        if not deleted:
            raise NotFoundError(f"Cattle with ID {cattle_id} not found.")