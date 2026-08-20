from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.repositories.utils import handle_db_errors


class FarmerRepository:
    """Repository for farmer database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all farmers."""
        query = """
            SELECT
                farmer_id,
                full_name,
                phone,
                email,
                address,
                created_at,
                updated_at
            FROM farmers
            ORDER BY farmer_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(farmer_id: int) -> dict[str, Any] | None:
        """Return a farmer by ID."""
        query = """
            SELECT
                farmer_id,
                full_name,
                phone,
                email,
                address,
                created_at,
                updated_at
            FROM farmers
            WHERE farmer_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (farmer_id,))
                return cursor.fetchone()

    @staticmethod
    @handle_db_errors
    def create(
        full_name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any]:
        """Create and return a farmer."""
        query = """
            INSERT INTO farmers (
                full_name,
                phone,
                email,
                address
            )
            VALUES (%s, %s, %s, %s)
            RETURNING
                farmer_id,
                full_name,
                phone,
                email,
                address,
                created_at,
                updated_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (full_name, phone, email, address),
                )
                farmer = cursor.fetchone()
                connection.commit()
                return farmer

    @staticmethod
    @handle_db_errors
    def update(
        farmer_id: int,
        full_name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
    ) -> dict[str, Any] | None:
        """Update and return a farmer."""
        query = """
            UPDATE farmers
            SET
                full_name = %s,
                phone = %s,
                email = %s,
                address = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE farmer_id = %s
            RETURNING
                farmer_id,
                full_name,
                phone,
                email,
                address,
                created_at,
                updated_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        full_name,
                        phone,
                        email,
                        address,
                        farmer_id,
                    ),
                )
                farmer = cursor.fetchone()
                connection.commit()
                return farmer

    @staticmethod
    @handle_db_errors
    def delete(farmer_id: int) -> bool:
        """Delete a farmer and return whether deletion occurred."""
        query = """
            DELETE FROM farmers
            WHERE farmer_id = %s
            RETURNING farmer_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (farmer_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None