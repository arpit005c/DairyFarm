from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.repositories.utils import handle_db_errors


class MilkRecordRepository:
    """Repository for milk record database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all milk records."""
        query = """
            SELECT
                milk_record_id,
                cattle_id,
                record_date,
                session,
                quantity_litres,
                created_at
            FROM milk_records
            ORDER BY milk_record_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(milk_record_id: int) -> dict[str, Any] | None:
        """Return a milk record by ID."""
        query = """
            SELECT
                milk_record_id,
                cattle_id,
                record_date,
                session,
                quantity_litres,
                created_at
            FROM milk_records
            WHERE milk_record_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (milk_record_id,))
                return cursor.fetchone()

    @staticmethod
    def get_by_cattle_id(cattle_id: int) -> list[dict[str, Any]]:
        """Return all milk records for cattle."""
        query = """
            SELECT
                milk_record_id,
                cattle_id,
                record_date,
                session,
                quantity_litres,
                created_at
            FROM milk_records
            WHERE cattle_id = %s
            ORDER BY record_date, session;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (cattle_id,))
                return cursor.fetchall()

    @staticmethod
    @handle_db_errors
    def create(
        cattle_id: int,
        record_date: Any,
        session: str,
        quantity_litres: float,
    ) -> dict[str, Any]:
        """Create and return a milk record."""
        query = """
            INSERT INTO milk_records (
                cattle_id,
                record_date,
                session,
                quantity_litres
            )
            VALUES (%s, %s, %s, %s)
            RETURNING
                milk_record_id,
                cattle_id,
                record_date,
                session,
                quantity_litres,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        cattle_id,
                        record_date,
                        session,
                        quantity_litres,
                    ),
                )
                record = cursor.fetchone()
                connection.commit()
                return record

    @staticmethod
    @handle_db_errors
    def update(
        milk_record_id: int,
        cattle_id: int,
        record_date: Any,
        session: str,
        quantity_litres: float,
    ) -> dict[str, Any] | None:
        """Update and return a milk record."""
        query = """
            UPDATE milk_records
            SET
                cattle_id = %s,
                record_date = %s,
                session = %s,
                quantity_litres = %s
            WHERE milk_record_id = %s
            RETURNING
                milk_record_id,
                cattle_id,
                record_date,
                session,
                quantity_litres,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        cattle_id,
                        record_date,
                        session,
                        quantity_litres,
                        milk_record_id,
                    ),
                )
                record = cursor.fetchone()
                connection.commit()
                return record

    @staticmethod
    @handle_db_errors
    def delete(milk_record_id: int) -> bool:
        """Delete a milk record."""
        query = """
            DELETE FROM milk_records
            WHERE milk_record_id = %s
            RETURNING milk_record_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (milk_record_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None