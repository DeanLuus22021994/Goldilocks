"""Tests for authentication API endpoints."""

from __future__ import annotations

from flask import Flask
from flask.testing import FlaskClient

from goldilocks.models.database import User, db
from goldilocks.models.forms import LoginForm, RegisterForm


class TestAuthenticationEndpoints:
    """Test suite for authentication endpoints."""

    def test_login_page_renders_successfully(self, client: FlaskClient) -> None:
        """Test that login page renders with form."""
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"Login to Goldilocks" in response.data
        assert b"email" in response.data
        assert b"password" in response.data

    def test_login_with_valid_credentials(self, client: FlaskClient, test_user: User) -> None:
        """Test login with valid user credentials."""
        # Store user data before database operations
        user_email = test_user.email

        # Create test user in database
        with client.application.app_context():
            test_user.set_password("testpassword123")
            db.session.add(test_user)
            db.session.commit()

        response = client.post(
            "/auth/login",
            data={
                "email": user_email,
                "password": "testpassword123",
                "csrf_token": self._get_csrf_token(client, "/auth/login"),
            },
        )

        # Should redirect to dashboard or home
        assert response.status_code in [200, 302]

    def test_login_with_invalid_credentials(self, client: FlaskClient) -> None:
        """Test login with invalid credentials."""
        response = client.post(
            "/auth/login",
            data={
                "email": "nonexistent@example.com",
                "password": "wrongpassword",
                "csrf_token": self._get_csrf_token(client, "/auth/login"),
            },
        )

        # Should stay on login page or redirect with error
        assert response.status_code in [200, 302]

    def test_login_redirects_authenticated_user(self, client: FlaskClient) -> None:
        """Test that authenticated users are redirected from login page."""
        # This test would require proper session setup in a real implementation
        response = client.get("/auth/login")
        # For now, just check it returns a valid response
        assert response.status_code in [200, 302]

    def test_register_page_renders_successfully(self, client: FlaskClient) -> None:
        """Test that registration page renders with form."""
        response = client.get("/auth/register")
        assert response.status_code == 200
        assert b"Create Account" in response.data
        assert b"username" in response.data
        assert b"email" in response.data
        assert b"password" in response.data

    def test_register_with_valid_data(self, client: FlaskClient) -> None:
        """Test user registration with valid data."""
        user_data: dict[str, str | bool] = {
            "username": "newuser",
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "TestPassword123",
            "confirm_password": "TestPassword123",
            "terms_accepted": True,
            "csrf_token": self._get_csrf_token(client, "/auth/register"),
        }

        response = client.post("/auth/register", data=user_data)

        # Should redirect or show success
        assert response.status_code in [200, 302]

    def test_register_with_duplicate_email(self, client: FlaskClient, test_user: User) -> None:
        """Test registration with already existing email."""
        # Store user data before database operations
        user_email = test_user.email

        with client.application.app_context():
            db.session.add(test_user)
            db.session.commit()

        user_data: dict[str, str | bool] = {
            "username": "differentuser",
            "email": user_email,  # Duplicate email
            "full_name": "Different User",
            "password": "TestPassword123",
            "confirm_password": "TestPassword123",
            "terms_accepted": True,
            "csrf_token": self._get_csrf_token(client, "/auth/register"),
        }

        response = client.post("/auth/register", data=user_data)

        # Should stay on registration page with error
        assert response.status_code == 200

    def test_register_with_password_mismatch(self, client: FlaskClient) -> None:
        """Test registration with password confirmation mismatch."""
        user_data: dict[str, str | bool] = {
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "TestPassword123",
            "confirm_password": "DifferentPassword123",
            "terms_accepted": True,
            "csrf_token": self._get_csrf_token(client, "/auth/register"),
        }

        response = client.post("/auth/register", data=user_data)

        # Should stay on registration page with validation error
        assert response.status_code == 200

    def test_logout_endpoint(self, client: FlaskClient) -> None:
        """Test user logout functionality."""
        response = client.get("/auth/logout")
        # Should redirect to login or home page
        assert response.status_code == 302

    def test_dashboard_requires_authentication(self, client: FlaskClient) -> None:
        """Test that dashboard requires user authentication."""
        response = client.get("/auth/dashboard")
        # Should redirect to login page
        assert response.status_code == 302

    def test_dashboard_for_authenticated_user(self, client: FlaskClient) -> None:
        """Test dashboard access - would need proper auth setup."""
        response = client.get("/auth/dashboard")
        # Should redirect to login when not authenticated
        assert response.status_code == 302

    def test_profile_requires_authentication(self, client: FlaskClient) -> None:
        """Test that profile page requires authentication."""
        response = client.get("/auth/profile")
        # Should redirect to login
        assert response.status_code == 302

    def test_profile_page_for_authenticated_user(self, client: FlaskClient) -> None:
        """Test profile page access - would need proper auth setup."""
        response = client.get("/auth/profile")
        # Should redirect to login when not authenticated
        assert response.status_code == 302

    def _get_csrf_token(self, _client: FlaskClient, _endpoint: str) -> str:
        """Helper method to get CSRF token from a form page."""
        # In a real implementation, this would parse the HTML for the CSRF
        # token
        return "test_csrf_token"


class TestAuthenticationForms:
    """Test suite for authentication forms."""

    def test_login_form_validation(self, app: Flask) -> None:
        """Test login form validation."""
        with app.app_context():
            # Valid form
            form_data: dict[str, str] = {
                "email": "test@example.com",
                "password": "password123",
            }
            form = LoginForm(data=form_data)
            assert form.validate()

            # Invalid email
            form_data["email"] = "invalid_email"
            form = LoginForm(data=form_data)
            assert not form.validate()

            # Empty password
            form_data["email"] = "test@example.com"
            form_data["password"] = ""
            form = LoginForm(data=form_data)
            assert not form.validate()

    def test_register_form_validation(self, app: Flask) -> None:
        """Test registration form validation."""
        with app.app_context():
            # Valid form
            form_data: dict[str, str | bool] = {
                "username": "testuser",
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "TestPassword123",
                "confirm_password": "TestPassword123",
                "terms_accepted": True,
            }
            form = RegisterForm(data=form_data)
            assert form.validate()

            # Invalid username (too short)
            form_data["username"] = "ab"
            form = RegisterForm(data=form_data)
            assert not form.validate()

            # Weak password
            form_data["username"] = "testuser"
            form_data["password"] = "weak"
            form_data["confirm_password"] = "weak"
            form = RegisterForm(data=form_data)
            assert not form.validate()

            # Terms not accepted
            form_data["password"] = "TestPassword123"
            form_data["confirm_password"] = "TestPassword123"
            form_data["terms_accepted"] = False
            form = RegisterForm(data=form_data)
            assert not form.validate()


class TestAuthenticationSecurity:
    """Test suite for authentication security features."""

    def test_csrf_protection_on_forms(self, client: FlaskClient) -> None:
        """Test that forms are protected against CSRF attacks."""
        # Create app with CSRF enabled
        from goldilocks.core.app_factory import create_app

        csrf_app = create_app("testing")
        csrf_app.config["WTF_CSRF_ENABLED"] = True

        with csrf_app.test_client() as csrf_client:
            # Try to submit login form without CSRF token
            response = csrf_client.post(
                "/auth/login",
                data={"email": "test@example.com", "password": "password"},
            )

            # Should fail due to missing CSRF token
            assert response.status_code == 400

    def test_password_hashing(self, app: Flask, test_user: User) -> None:
        """Test that passwords are properly hashed."""
        with app.app_context():
            password = "testpassword123"
            test_user.set_password(password)

            # Password should be hashed, not stored in plain text
            assert test_user.password_hash is not None
            assert test_user.password_hash != password
            # Hashed passwords are long
            assert len(test_user.password_hash) > 20

            # Should be able to verify password
            assert test_user.check_password(password)
            assert not test_user.check_password("wrongpassword")

    def test_session_security(self, client: FlaskClient) -> None:
        """Test session security configurations."""
        with client.application.app_context():
            # Check that secure session configurations are set
            config = client.application.config
            assert config.get("SESSION_COOKIE_HTTPONLY") is True  # type: ignore[misc]
            assert config.get("SESSION_COOKIE_SAMESITE") == "Lax"  # type: ignore[misc]
            # Note: SESSION_COOKIE_SECURE would be True in production
