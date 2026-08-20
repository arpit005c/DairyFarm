from typing import Any

from psycopg.rows import dict_row

from backend.app.db.connection import get_connection
from backend.app.repositories.utils import handle_db_errors


class FeedRecordRepository:
    """Repository for feed record database operations."""

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        """Return all feed records."""
        query = """
            SELECT
                feed_record_id,
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost,
                created_at
            FROM feed_records
            ORDER BY feed_record_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                return cursor.fetchall()

    @staticmethod
    def get_by_id(feed_record_id: int) -> dict[str, Any] | None:
        """Return a feed record by ID."""
        query = """
            SELECT
                feed_record_id,
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost,
                created_at
            FROM feed_records
            WHERE feed_record_id = %s;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (feed_record_id,))
                return cursor.fetchone()

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> list[dict[str, Any]]:
        """Return feed records for a farmer."""
        query = """
            SELECT
                feed_record_id,
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost,
                created_at
            FROM feed_records
            WHERE farmer_id = %s
            ORDER BY record_date, feed_record_id;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (farmer_id,))
                return cursor.fetchall()

    @staticmethod
    @handle_db_errors
    def create(
        farmer_id: int,
        record_date: Any,
        feed_type: str,
        quantity_kg: float,
        cost: float,
        cattle_id: int | None = None,
    ) -> dict[str, Any]:
        """Create and return a feed record."""
        query = """
            INSERT INTO feed_records (
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING
                feed_record_id,
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        cattle_id,
                        record_date,
                        feed_type,
                        quantity_kg,
                        cost,
                    ),
                )
                record = cursor.fetchone()
                connection.commit()
                return record

    @staticmethod
    @handle_db_errors
    def update(
        feed_record_id: int,
        farmer_id: int,
        record_date: Any,
        feed_type: str,
        quantity_kg: float,
        cost: float,
        cattle_id: int | None = None,
    ) -> dict[str, Any] | None:
        """Update and return a feed record."""
        query = """
            UPDATE feed_records
            SET
                farmer_id = %s,
                cattle_id = %s,
                record_date = %s,
                feed_type = %s,
                quantity_kg = %s,
                cost = %s
            WHERE feed_record_id = %s
            RETURNING
                feed_record_id,
                farmer_id,
                cattle_id,
                record_date,
                feed_type,
                quantity_kg,
                cost,
                created_at;
        """

        with get_connection() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        farmer_id,
                        cattle_id,
                        record_date,
                        feed_type,
                        quantity_kg,
                        cost,
                        feed_record_id,
                    ),
                )
                record = cursor.fetchone()
                connection.commit()
                return record

    @staticmethod
    @handle_db_errors
    def delete(feed_record_id: int) -> bool:
        """Delete a feed record."""
        query = """
            DELETE FROM feed_records
            WHERE feed_record_id = %s
            RETURNING feed_record_id;
        """

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (feed_record_id,))
                deleted = cursor.fetchone()
                connection.commit()
                return deleted is not None