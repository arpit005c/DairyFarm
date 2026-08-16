from typing import Any

from backend.app.repositories.revenue_repository import RevenueRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class RevenueService:
    """Business logic for revenue operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all revenue records."""
        return RevenueRepository.get_all()

    @staticmethod
    def get_by_id(revenue_id: int) -> dict[str, Any]:
        """Return a revenue record by ID."""
        if revenue_id <= 0:
            raise ValidationError("Revenue ID must be a positive integer.")

        revenue = RevenueRepository.get_by_id(revenue_id)

        if revenue is None:
            raise NotFoundError(f"Revenue with ID {revenue_id} not found.")

        return revenue

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all revenue records for a farmer."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        return RevenueRepository.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        sale_date: Any,
        quantity_litres: float,
        price_per_litre: float,
        buyer_name: str | None = None,
    ) -> dict[str, Any]:
        """Validate and create a revenue record."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if quantity_litres <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        if price_per_litre <= 0:
            raise ValidationError("Price per litre must be greater than zero.")

        if buyer_name is not None:
            buyer_name = buyer_name.strip() or None

        return RevenueRepository.create(
            farmer_id=farmer_id,
            sale_date=sale_date,
            quantity_litres=quantity_litres,
            price_per_litre=price_per_litre,
            buyer_name=buyer_name,
        )

    @staticmethod
    def update(
        revenue_id: int,
        farmer_id: int,
        sale_date: Any,
        quantity_litres: float,
        price_per_litre: float,
        buyer_name: str | None = None,
    ) -> dict[str, Any]:
        """Validate and update a revenue record."""
        if revenue_id <= 0:
            raise ValidationError("Revenue ID must be a positive integer.")

        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if quantity_litres <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        if price_per_litre <= 0:
            raise ValidationError("Price per litre must be greater than zero.")

        if buyer_name is not None:
            buyer_name = buyer_name.strip() or None

        revenue = RevenueRepository.update(
            revenue_id=revenue_id,
            farmer_id=farmer_id,
            sale_date=sale_date,
            quantity_litres=quantity_litres,
            price_per_litre=price_per_litre,
            buyer_name=buyer_name,
        )

        if revenue is None:
            raise NotFoundError(f"Revenue with ID {revenue_id} not found.")

        return revenue

    @staticmethod
    def delete(revenue_id: int) -> None:
        """Delete a revenue record."""
        if revenue_id <= 0:
            raise ValidationError("Revenue ID must be a positive integer.")

        deleted = RevenueRepository.delete(revenue_id)

        if not deleted:
            raise NotFoundError(f"Revenue with ID {revenue_id} not found.")