from typing import Any

from backend.app.services.revenue_service import RevenueService


class RevenueApplication:
    """Application use cases for revenue operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all revenue records."""
        return RevenueService.get_all()

    @staticmethod
    def get_by_id(revenue_id: int) -> dict[str, Any]:
        """Return a revenue record by ID."""
        return RevenueService.get_by_id(revenue_id)

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all revenue records for a farmer."""
        return RevenueService.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        sale_date: Any,
        quantity_litres: float,
        price_per_litre: float,
        buyer_name: str | None = None,
    ) -> dict[str, Any]:
        """Create a revenue record through the service layer."""
        return RevenueService.create(
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
        """Update a revenue record through the service layer."""
        return RevenueService.update(
            revenue_id=revenue_id,
            farmer_id=farmer_id,
            sale_date=sale_date,
            quantity_litres=quantity_litres,
            price_per_litre=price_per_litre,
            buyer_name=buyer_name,
        )

    @staticmethod
    def delete(revenue_id: int) -> None:
        """Delete a revenue record through the service layer."""
        RevenueService.delete(revenue_id)