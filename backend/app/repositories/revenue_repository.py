from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection


class RevenueRepository:
    """Repository for revenue database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all revenue records."""
        query = """
            SELECT
                revenue_id,
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name,
                created_at
            FROM revenue
            ORDER BY revenue_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(revenue_id: int) -> dict[str, Any] | None:
        """Return a revenue record by ID."""
        query = """
            SELECT
                revenue_id,
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name,
                created_at
            FROM revenue
            WHERE revenue_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (revenue_id,))
                return cursor.fetchone()

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return revenue records for a farmer."""
        query = """
            SELECT
                revenue_id,
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name,
                created_at
            FROM revenue
            WHERE farmer_id = %s
            ORDER BY sale_date, revenue_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (farmer_id,))
                return cursor.fetchall()

    @staticmethod
    def create(
        farmer_id: int,
        sale_date: Any,
        quantity_litres: float,
        price_per_litre: float,
        buyer_name: str | None = None,
    ) -> dict[str, Any]:
        """Create and return a revenue record."""
        query = """
            INSERT INTO revenue (
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING
                revenue_id,
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        sale_date,
                        quantity_litres,
                        price_per_litre,
                        buyer_name,
                    ),
                )
                revenue = cursor.fetchone()
                connection.commit()
                return revenue

    @staticmethod
    def update(
        revenue_id: int,
        farmer_id: int,
        sale_date: Any,
        quantity_litres: float,
        price_per_litre: float,
        buyer_name: str | None = None,
    ) -> dict[str, Any] | None:
        """Update and return a revenue record."""
        query = """
            UPDATE revenue
            SET
                farmer_id = %s,
                sale_date = %s,
                quantity_litres = %s,
                price_per_litre = %s,
                buyer_name = %s
            WHERE revenue_id = %s
            RETURNING
                revenue_id,
                farmer_id,
                sale_date,
                quantity_litres,
                price_per_litre,
                buyer_name,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        sale_date,
                        quantity_litres,
                        price_per_litre,
                        buyer_name,
                        revenue_id,
                    ),
                )
                revenue = cursor.fetchone()
                connection.commit()
                return revenue

    @staticmethod
    def delete(revenue_id: int) -> bool:
        """Delete a revenue record."""
        query = """
            DELETE FROM revenue
            WHERE revenue_id = %s
            RETURNING revenue_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (revenue_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None