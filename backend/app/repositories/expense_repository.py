from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection


class ExpenseRepository:
    """Repository for expense database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all expenses."""
        query = """
            SELECT
                expense_id,
                farmer_id,
                expense_date,
                category,
                description,
                amount,
                created_at
            FROM expenses
            ORDER BY expense_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(expense_id: int) -> dict[str, Any] | None:
        """Return an expense by ID."""
        query = """
            SELECT
                expense_id,
                farmer_id,
                expense_date,
                category,
                description,
                amount,
                created_at
            FROM expenses
            WHERE expense_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (expense_id,))
                return cursor.fetchone()

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return expenses for a farmer."""
        query = """
            SELECT
                expense_id,
                farmer_id,
                expense_date,
                category,
                description,
                amount,
                created_at
            FROM expenses
            WHERE farmer_id = %s
            ORDER BY expense_date, expense_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (farmer_id,))
                return cursor.fetchall()

    @staticmethod
    def create(
        farmer_id: int,
        expense_date: Any,
        category: str,
        amount: float,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create and return an expense."""
        query = """
            INSERT INTO expenses (
                farmer_id,
                expense_date,
                category,
                description,
                amount
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING
                expense_id,
                farmer_id,
                expense_date,
                category,
                description,
                amount,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        expense_date,
                        category,
                        description,
                        amount,
                    ),
                )
                expense = cursor.fetchone()
                connection.commit()
                return expense

    @staticmethod
    def update(
        expense_id: int,
        farmer_id: int,
        expense_date: Any,
        category: str,
        amount: float,
        description: str | None = None,
    ) -> dict[str, Any] | None:
        """Update and return an expense."""
        query = """
            UPDATE expenses
            SET
                farmer_id = %s,
                expense_date = %s,
                category = %s,
                description = %s,
                amount = %s
            WHERE expense_id = %s
            RETURNING
                expense_id,
                farmer_id,
                expense_date,
                category,
                description,
                amount,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        expense_date,
                        category,
                        description,
                        amount,
                        expense_id,
                    ),
                )
                expense = cursor.fetchone()
                connection.commit()
                return expense

    @staticmethod
    def delete(expense_id: int) -> bool:
        """Delete an expense."""
        query = """
            DELETE FROM expenses
            WHERE expense_id = %s
            RETURNING expense_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (expense_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None