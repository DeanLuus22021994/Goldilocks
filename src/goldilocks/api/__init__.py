"""Goldilocks API layer.

Contains REST API endpoints, request/response handling,
and API-specific middleware for the Goldilocks Flask application.

This module provides:
- RESTful API endpoint definitions
- Request validation and serialization
- Response formatting and error handling
- API versioning and documentation support
- Authentication and authorization middleware
"""

from typing import Any

__all__: list[str] = ["API_VERSION", "ENDPOINTS", "create_error_response"]

# API versioning and metadata
API_VERSION = "v1"
API_BASE_PATH = f"/api/{API_VERSION}"

# Available API endpoints registry
ENDPOINTS = {
    "health": "/health",
    "version": "/version",
    "status": "/status",
}


def create_error_response(
    message: str,
    status_code: int = 400,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create standardized error response format."""
    response = {
        "error": True,
        "message": message,
        "status_code": status_code,
    }
    if details:
        response["details"] = details
    return response


def register_api_routes(app: Any) -> None:
    """Register all API routes with the Flask application."""
    # This would be implemented when API routes are added
    # Future: Add route registration logic here
    return None
