"""Tests for API endpoints."""

from __future__ import annotations

from typing import Any

from flask import Flask
from flask.testing import FlaskClient


class TestAPIEndpoints:
    """Test suite for core API endpoints."""

    def test_health_endpoint_returns_ok_status(self, client: FlaskClient[Any]) -> None:
        """Test that health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data == {"status": "ok"}

    def test_health_endpoint_includes_correlation_id(
        self, client: FlaskClient[Any], correlation_id_header: dict[str, str]
    ) -> None:
        """Test that health endpoint handles correlation ID properly."""
        response = client.get("/health", headers=correlation_id_header)
        assert response.status_code == 200
        expected_id = correlation_id_header["X-Request-ID"]
        assert response.headers.get("X-Request-ID") == expected_id

    def test_version_endpoint_returns_app_info(
        self, client: FlaskClient[Any]
    ) -> None:
        """Test that version endpoint returns expected data structure."""
        response = client.get("/version")
        assert response.status_code == 200
        assert response.is_json

        data = response.get_json()
        required_keys = {"app", "python", "flask", "platform"}
        assert required_keys.issubset(data.keys())

        # Validate data types
        assert isinstance(data["app"], str)
        assert isinstance(data["python"], str)
        assert isinstance(data["flask"], str)
        assert isinstance(data["platform"], str)

    def test_version_endpoint_python_version_format(
        self, client: FlaskClient
    ) -> None:
        """Test that Python version follows expected format."""
        response = client.get("/version")
        data = response.get_json()

        python_version = data["python"]
        # Should be in format "3.12.7"
        parts = python_version.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_version_endpoint_with_correlation_id(
        self, client: FlaskClient[Any], correlation_id_header: dict[str, str]
    ) -> None:
        """Test version endpoint with correlation ID header."""
        response = client.get("/version", headers=correlation_id_header)
        assert response.status_code == 200
        expected_id = correlation_id_header["X-Request-ID"]
        assert response.headers.get("X-Request-ID") == expected_id

    def test_api_endpoints_include_timing_headers(self, client: FlaskClient[Any]) -> None:
        """Test that API endpoints include response timing headers."""
        response = client.get("/health")
        assert "X-Response-Time-ms" in response.headers

        timing = response.headers["X-Response-Time-ms"]
        # Should be a valid float
        assert float(timing) >= 0.0

    def test_api_endpoints_content_type_headers(self, client: FlaskClient[Any]) -> None:
        """Test that API endpoints return proper content-type headers."""
        response = client.get("/health")
        assert response.content_type.startswith("application/json")

        response = client.get("/version")
        assert response.content_type.startswith("application/json")

    def test_nonexistent_api_endpoint_returns_404(self, client: FlaskClient[Any]) -> None:
        """Test that nonexistent API endpoints return 404 with JSON error."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        assert response.is_json

        data = response.get_json()
        assert "message" in data
        assert data["message"] == "Not Found"


class TestAPIUtilities:
    """Test suite for API utility functions."""

    def test_create_error_response_basic(self) -> None:
        """Test creating basic error response."""
        from goldilocks.api import create_error_response

        response = create_error_response("Test error", 400)

        expected = {
            "error": True,
            "message": "Test error",
            "status_code": 400,
        }
        assert response == expected

    def test_create_error_response_with_details(self) -> None:
        """Test creating error response with details."""
        from goldilocks.api import create_error_response

        details = {"field": "email", "reason": "invalid format"}
        response = create_error_response("Validation error", 422, details)

        expected = {
            "error": True,
            "message": "Validation error",
            "status_code": 422,
            "details": details,
        }
        assert response == expected

    def test_create_error_response_defaults(self) -> None:
        """Test error response with default parameters."""
        from goldilocks.api import create_error_response

        response = create_error_response("Default error")

        assert response["status_code"] == 400
        assert "details" not in response

    def test_api_constants_exist(self) -> None:
        """Test that API constants are properly defined."""
        from goldilocks.api import API_VERSION, ENDPOINTS

        assert isinstance(API_VERSION, str)
        assert isinstance(ENDPOINTS, dict)

        # Check expected endpoints
        expected_endpoints = {"health", "version", "status"}
        assert expected_endpoints.issubset(ENDPOINTS.keys())


class TestAPIBlueprint:
    """Test suite for API blueprint registration."""

    def test_api_blueprint_is_registered(self, app: Flask) -> None:
        """Test that API blueprint is properly registered."""
        blueprints = [bp.name for bp in app.iter_blueprints()]
        assert "api" in blueprints

    def test_api_blueprint_url_rules(self, app: Flask) -> None:
        """Test that API blueprint has expected URL rules."""
        rules = [rule.rule for rule in app.url_map.iter_rules()]

        # Check that our API endpoints are registered
        assert "/health" in rules
        assert "/version" in rules

    def test_api_blueprint_methods(self, app: Flask) -> None:
        """Test that API endpoints support expected HTTP methods."""
        for rule in app.url_map.iter_rules():
            if rule.rule in ["/health", "/version"]:
                assert "GET" in rule.methods
                # Should not support POST/PUT/DELETE by default
                assert "POST" not in rule.methods
                assert "PUT" not in rule.methods
                assert "DELETE" not in rule.methods
