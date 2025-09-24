"""Goldilocks data models and schemas.

Contains data models, database schemas, validation classes,
and serialization logic for the Goldilocks Flask application.

This module provides:
- Pydantic models for request/response validation
- Database ORM models (SQLAlchemy when used)
- Data transformation and serialization utilities
- Schema validation and error handling
"""

from typing import Any, Protocol

__all__: list[str] = ["BaseModel", "ValidationError", "validate_data"]


class BaseModel(Protocol):
    """Protocol for all application data models."""

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary representation."""
        raise NotImplementedError("Subclasses must implement to_dict")

    def validate(self) -> bool:
        """Validate model data and return True if valid."""
        raise NotImplementedError("Subclasses must implement validate")


class ValidationError(Exception):
    """Custom validation error for model data."""

    def __init__(self, message: str, field: str | None = None) -> None:
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_data(data: dict[str, Any], required_fields: list[str]) -> None:
    """Validate that all required fields are present in data."""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
