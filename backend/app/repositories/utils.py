import functools
import psycopg
from backend.app.services.exceptions import ConflictError, ValidationError

def handle_db_errors(func):
    """
    Decorator to catch PostgreSQL errors and translate them into
    controlled business layer exceptions without interfering with transactions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except psycopg.errors.UniqueViolation as e:
            # e.g., duplicate tag number, duplicate email
            raise ConflictError("Duplicate record. A record with this unique identifier already exists.") from e
        except psycopg.errors.ForeignKeyViolation as e:
            # e.g., missing farmer_id, missing cattle_id
            raise ValidationError("A referenced record (e.g., Farmer or Cattle) does not exist.") from e
        except psycopg.errors.InvalidDatetimeFormat as e:
            raise ValidationError("Invalid date or time format provided.") from e
        except psycopg.errors.NumericValueOutOfRange as e:
            raise ValidationError("A numeric value is out of the allowed range.") from e
    return wrapper
