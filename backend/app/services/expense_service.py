from typing import Any

from backend.app.repositories.expense_repository import ExpenseRepository
from backend.app.services.exceptions import NotFoundError, ValidationError


class ExpenseService:
    """Business logic for expense operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all expenses."""
        return ExpenseRepository.get_all()

    @staticmethod
    def get_by_id(expense_id: int) -> dict[str, Any]:
        """Return an expense by ID."""
        if expense_id <= 0:
            raise ValidationError("Expense ID must be a positive integer.")

        expense = ExpenseRepository.get_by_id(expense_id)

        if expense is None:
            raise NotFoundError(f"Expense with ID {expense_id} not found.")

        return expense

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all expenses for a farmer."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        return ExpenseRepository.get_by_farmer_id(farmer_id)

    @staticmethod
    def create(
        farmer_id: int,
        expense_date: Any,
        category: str,
        amount: float,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Validate and create an expense."""
        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if expense_date is not None and isinstance(expense_date, str):
            if not expense_date.strip():
                raise ValidationError("Expense date cannot be empty.")
            expense_date = expense_date.strip()

        if not category or not category.strip():
            raise ValidationError("Expense category is required.")

        if amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")

        category = category.strip()

        if description is not None:
            description = description.strip() or None

        return ExpenseRepository.create(
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
        """Validate and update an expense."""
        if expense_id <= 0:
            raise ValidationError("Expense ID must be a positive integer.")

        if farmer_id <= 0:
            raise ValidationError("Farmer ID must be a positive integer.")

        if expense_date is not None and isinstance(expense_date, str):
            if not expense_date.strip():
                raise ValidationError("Expense date cannot be empty.")
            expense_date = expense_date.strip()

        if not category or not category.strip():
            raise ValidationError("Expense category is required.")

        if amount <= 0:
            raise ValidationError("Expense amount must be greater than zero.")

        category = category.strip()

        if description is not None:
            description = description.strip() or None

        expense = ExpenseRepository.update(
            expense_id=expense_id,
            farmer_id=farmer_id,
            expense_date=expense_date,
            category=category,
            amount=amount,
            description=description,
        )

        if expense is None:
            raise NotFoundError(f"Expense with ID {expense_id} not found.")

        return expense

    @staticmethod
    def delete(expense_id: int) -> None:
        """Delete an expense."""
        if expense_id <= 0:
            raise ValidationError("Expense ID must be a positive integer.")

        deleted = ExpenseRepository.delete(expense_id)

        if not deleted:
            raise NotFoundError(f"Expense with ID {expense_id} not found.")