from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.repositories.utils import handle_db_errors


class CattleRepository:
    """Repository for cattle database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all cattle."""
        query = """
            SELECT
                cattle_id,
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status,
                created_at,
                updated_at
            FROM cattle
            ORDER BY cattle_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(cattle_id: int) -> dict[str, Any] | None:
        """Return cattle by ID."""
        query = """
            SELECT
                cattle_id,
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status,
                created_at,
                updated_at
            FROM cattle
            WHERE cattle_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (cattle_id,))
                return cursor.fetchone()

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return all cattle belonging to a farmer."""
        query = """
            SELECT
                cattle_id,
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status,
                created_at,
                updated_at
            FROM cattle
            WHERE farmer_id = %s
            ORDER BY cattle_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (farmer_id,))
                return cursor.fetchall()

    @staticmethod
    @handle_db_errors
    def create(
        farmer_id: int,
        tag_number: str,
        gender: str,
        name: str | None = None,
        breed: str | None = None,
        date_of_birth: Any | None = None,
        status: str = "active",
    ) -> dict[str, Any]:
        """Create and return cattle."""
        query = """
            INSERT INTO cattle (
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING
                cattle_id,
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status,
                created_at,
                updated_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        tag_number,
                        name,
                        breed,
                        gender,
                        date_of_birth,
                        status,
                    ),
                )
                cattle = cursor.fetchone()
                connection.commit()
                return cattle

    @staticmethod
    @handle_db_errors
    def update(
        cattle_id: int,
        farmer_id: int,
        tag_number: str,
        gender: str,
        name: str | None = None,
        breed: str | None = None,
        date_of_birth: Any | None = None,
        status: str = "active",
    ) -> dict[str, Any] | None:
        """Update and return cattle."""
        query = """
            UPDATE cattle
            SET
                farmer_id = %s,
                tag_number = %s,
                name = %s,
                breed = %s,
                gender = %s,
                date_of_birth = %s,
                status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE cattle_id = %s
            RETURNING
                cattle_id,
                farmer_id,
                tag_number,
                name,
                breed,
                gender,
                date_of_birth,
                status,
                created_at,
                updated_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        tag_number,
                        name,
                        breed,
                        gender,
                        date_of_birth,
                        status,
                        cattle_id,
                    ),
                )
                cattle = cursor.fetchone()
                connection.commit()
                return cattle

    @staticmethod
    @handle_db_errors
    def delete(cattle_id: int) -> bool:
        """Delete cattle and return whether deletion occurred."""
        query = """
            DELETE FROM cattle
            WHERE cattle_id = %s
            RETURNING cattle_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (cattle_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None