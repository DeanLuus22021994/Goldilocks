"""Goldilocks business services layer.

Contains business logic services, external integrations,
and application services for the Goldilocks Flask application.

This module provides:
- Business logic service classes
- External API integrations and clients
- Data processing and transformation services
- Background task and job processing
- Caching and performance optimization services
"""

from typing import Any, Protocol

__all__: list[str] = ["BaseService", "ServiceError", "service_registry"]


class BaseService(Protocol):
    """Protocol for all application services."""

    def initialize(self) -> None:
        """Initialize service resources and connections."""
        raise NotImplementedError("Subclasses must implement initialize")

    def cleanup(self) -> None:
        """Clean up service resources and connections."""
        raise NotImplementedError("Subclasses must implement cleanup")


class ServiceError(Exception):
    """Custom error for service layer operations."""

    def __init__(self, message: str, service: str | None = None) -> None:
        self.message = message
        self.service = service
        super().__init__(self.message)


# Service registry for dependency injection
service_registry: dict[str, Any] = {}


def register_service(name: str, service: Any) -> None:
    """Register a service in the global service registry."""
    service_registry[name] = service


def get_service(name: str) -> Any:
    """Get a service from the global service registry."""
    service = service_registry.get(name)
    if service is None:
        raise ServiceError(f"Service '{name}' not found in registry")
    return service
