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

import platform
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from typing import Any

from flask import Blueprint

# Import fallback version
try:
    from goldilocks import __version__ as _FALLBACK_APP_VERSION
except ImportError:
    _FALLBACK_APP_VERSION = "0.1.0"

__all__: list[str] = [
    "API_VERSION",
    "ENDPOINTS",
    "create_error_response",
    "api_bp",
]

# API versioning and metadata
API_VERSION = "v1"
API_BASE_PATH = f"/api/{API_VERSION}"

# Available API endpoints registry
ENDPOINTS = {
    "health": "/health",
    "version": "/version",
    "status": "/status",
}

# Create API Blueprint
api_bp = Blueprint("api", __name__)


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


@api_bp.route("/health", methods=["GET"])
def health() -> tuple[dict[str, str], int]:
    """Health check endpoint."""
    return {"status": "ok"}, 200


@api_bp.route("/version", methods=["GET"])
def version() -> tuple[dict[str, Any], int]:
    """Version information endpoint."""

    def get_version(package_name: str) -> str:
        """Get package version with fallback."""
        try:
            return pkg_version(package_name)
        except PackageNotFoundError:
            if package_name == "Flask":
                # Fallback to Flask module version
                import flask

                return getattr(flask, "__version__", "unknown")
            return "unknown"

    return {
        "app": _FALLBACK_APP_VERSION,
        "python": (
            f"{sys.version_info.major}.{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        ),
        "flask": get_version("Flask"),
        "platform": platform.system().lower(),
    }, 200


def register_api_routes(app: Any) -> None:
    """Register all API routes with the Flask application."""
    app.register_blueprint(api_bp)
    return None
