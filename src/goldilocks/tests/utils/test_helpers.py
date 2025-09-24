"""Test utilities for the Goldilocks application."""

import tempfile
from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from goldilocks.core.app_factory import create_app
from goldilocks.models.database import User, db


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create test Flask application."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create test client."""
    return app.test_client()


@pytest.fixture
def test_user() -> User:
    """Create a test user instance."""
    user = User()
    user.email = "test@example.com"
    user.username = "testuser"
    user.full_name = "Test User"
    user.role = "user"
    return user


@pytest.fixture
def admin_user() -> User:
    """Create a test admin user instance."""
    user = User()
    user.email = "admin@example.com"
    user.username = "admin"
    user.full_name = "Admin User"
    user.role = "admin"
    return user


@pytest.fixture
def authenticated_user(app: Flask) -> User:
    """Create an authenticated test user."""
    with app.app_context():
        user = User()
        user.email = "auth@example.com"
        user.username = "authuser"
        user.full_name = "Authenticated User"
        user.set_password("password123")

        db.session.add(user)
        db.session.commit()

        return user


@pytest.fixture
def correlation_id_header() -> dict[str, str]:
    """Provide correlation ID header for testing."""
    return {"X-Request-ID": "test-cid-123"}


class DatabaseTestMixin:
    """Mixin class for database tests."""

    @staticmethod
    def create_test_user(email: str = "test@example.com", username: str = "testuser") -> User:
        """Create a test user with specified email and username."""
        user = User()
        user.email = email
        user.username = username
        user.full_name = f"Test User {username}"
        user.set_password("password123")
        return user


class APITestMixin:
    """Mixin class for API tests."""

    @staticmethod
    def make_authenticated_request(client: FlaskClient, endpoint: str, user: User, method: str = "GET", **kwargs):
        """Make an authenticated request as a specific user."""
        # This would need proper session/auth implementation
        # For now, just make the request
        if method.upper() == "GET":
            return client.get(endpoint, **kwargs)
        elif method.upper() == "POST":
            return client.post(endpoint, **kwargs)
        else:
            raise ValueError(f"Unsupported method: {method}")

    @staticmethod
    def get_csrf_token(client: FlaskClient, endpoint: str) -> str:
        """Extract CSRF token from a form page."""
        # Simplified implementation for testing
        return "test_csrf_token"


def assert_valid_response(response, expected_status: int = 200, expected_content_type: str = "application/json"):
    """Assert that response has expected status and content type."""
    assert response.status_code == expected_status
    if expected_content_type:
        assert response.content_type.startswith(expected_content_type)


def assert_json_response(response, expected_keys: set | None = None, expected_status: int = 200):
    """Assert that response is valid JSON with expected keys."""
    assert response.status_code == expected_status
    assert response.is_json

    if expected_keys:
        data = response.get_json()
        assert isinstance(data, dict)
        assert expected_keys.issubset(data.keys())


def assert_error_response(response, expected_status: int = 400, expected_message: str | None = None):
    """Assert that response is a proper error response."""
    assert response.status_code == expected_status
    assert response.is_json

    data = response.get_json()
    assert "message" in data

    if expected_message:
        assert expected_message in data["message"]


def create_temp_database() -> str:
    """Create a temporary database file for testing."""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db.close()
    return f"sqlite:///{temp_db.name}"
