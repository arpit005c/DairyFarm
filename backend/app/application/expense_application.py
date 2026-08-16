from typing import Any

from backend.app.services.expense_service import ExpenseService


class ExpenseApplication:
    """Application use cases for expense operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all expenses."""
        return ExpenseService.get_all()

    @staticmethod
    def get_by_id(expense_id: int) -> dict[str, Any]:
        """Return an expense by ID."""
        return ExpenseService.get_by_id(expense_id)

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all expenses for a farmer."""
        return ExpenseService.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        expense_date: Any,
        category: str,
        amount: float,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create an expense through the service layer."""
        return ExpenseService.create(
            farmer_id=farmer_id,
            expense_date=expense_date,
            category=category,
            amount=amount,
            description=description,
        )

    @staticmethod
    def update(
        expense_id: int,
        farmer_id: int,
        expense_date: Any,
        category: str,
        amount: float,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Update an expense through the service layer."""
        return ExpenseService.update(
            expense_id=expense_id,
            farmer_id=farmer_id,
            expense_date=expense_date,
            category=category,
            amount=amount,
            description=description,
        )

    @staticmethod
    def delete(expense_id: int) -> None:
        """Delete an expense through the service layer."""
        ExpenseService.delete(expense_id)