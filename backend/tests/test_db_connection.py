from backend.app.db.connection import get_connection


def test_database_connection():
    """Verify that the application can connect to PostgreSQL."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

    assert result == (1,)