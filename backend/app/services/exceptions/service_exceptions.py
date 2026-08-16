class ServiceError(Exception):
    """Base exception for service-layer errors."""


class ValidationError(ServiceError):
    """Raised when business input validation fails."""


class NotFoundError(ServiceError):
    """Raised when a requested entity does not exist."""


class ConflictError(ServiceError):
    """Raised when an operation conflicts with existing data."""