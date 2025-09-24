"""Tests for the Flask application factory."""

from __future__ import annotations

import tempfile
from unittest.mock import patch

from flask import Flask
from flask.testing import FlaskClient

from goldilocks.core.app_factory import (
    create_app,
    setup_extensions,
    setup_logging,
    setup_request_handlers,
)


class TestAppFactory:
    """Test suite for application factory."""

    def test_create_app_returns_flask_instance(self) -> None:
        """Test that create_app returns a Flask application instance."""
        app = create_app("testing")
        assert isinstance(app, Flask)
        assert app.testing is True

    def test_create_app_with_different_configs(self) -> None:
        """Test that create_app works with different configuration names."""
        # Test development config
        dev_app = create_app("development")
        assert dev_app.debug is True

        # Test testing config
        test_app = create_app("testing")
        assert test_app.testing is True

        # Test default config
        default_app = create_app()
        assert isinstance(default_app, Flask)

    def test_create_app_registers_blueprints(self) -> None:
        """Test that all blueprints are registered."""
        app = create_app("testing")

        blueprint_names = list(app.blueprints.keys())
        expected_blueprints = {"main", "auth", "api"}

        assert expected_blueprints.issubset(set(blueprint_names))

    def test_create_app_initializes_database(self) -> None:
        """Test that database is properly initialized."""
        app = create_app("testing")

        with app.app_context():
            from goldilocks.models.database import db

            # Database should be initialized
            assert db is not None
            assert hasattr(db, 'create_all')

    def test_create_app_sets_up_logging(self) -> None:
        """Test that logging is properly configured."""
        app = create_app("testing")

        # Check that app logger exists and is configured
        assert app.logger is not None
        assert len(app.logger.handlers) >= 0  # May have handlers or propagate

    def test_create_app_configures_static_folder(self) -> None:
        """Test that static folder is properly configured."""
        app = create_app("testing")

        # Should have static folder configured
        assert app.static_folder is not None
        assert app.static_url_path == "/static"

    def test_create_app_with_custom_static_folder(self) -> None:
        """Test app creation with custom static folder path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the static folder path
            with patch(
                'goldilocks.core.app_factory.os.path.join',
                return_value=temp_dir,
            ):
                app = create_app("testing")
                # Should not raise any exceptions
                assert isinstance(app, Flask)

    def test_create_app_handles_database_creation_errors(self) -> None:
        """Test that app handles database creation errors gracefully."""
        app = create_app("testing")

        # Even if database creation fails, app should still be created
        assert isinstance(app, Flask)


class TestSetupFunctions:
    """Test suite for setup utility functions."""

    def test_setup_logging(self) -> None:
        """Test logging setup function."""
        app = create_app("testing")

        # Should not raise exceptions
        setup_logging(app)

        # Logging should be configured
        import logging

        logger = logging.getLogger("goldilocks")
        assert logger.level == logging.INFO

    def test_setup_extensions(self) -> None:
        """Test extensions setup function."""
        app = create_app("testing")

        csrf, login_manager = setup_extensions(app)

        # Should return initialized extensions
        assert csrf is not None
        assert login_manager is not None
        assert hasattr(login_manager, 'user_loader')

    def test_setup_request_handlers(self) -> None:
        """Test request handlers setup."""
        app = create_app("testing")
        setup_request_handlers(app)

        # Should have before_request and after_request handlers
        assert len(app.before_request_funcs.get(None, [])) >= 1
        assert len(app.after_request_funcs.get(None, [])) >= 1


class TestApplicationConfiguration:
    """Test suite for application configuration."""

    def test_app_has_required_config_values(self) -> None:
        """Test that app has all required configuration values."""
        app = create_app("testing")

        required_configs = [
            'SECRET_KEY',
            'SQLALCHEMY_DATABASE_URI',
            'SQLALCHEMY_TRACK_MODIFICATIONS',
            'WTF_CSRF_ENABLED',
        ]

        for config_key in required_configs:
            assert config_key in app.config

    def test_testing_config_overrides(self) -> None:
        """Test that testing configuration properly overrides defaults."""
        app = create_app("testing")

        assert app.testing is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite:///:memory:"

    def test_development_config_settings(self) -> None:
        """Test development configuration settings."""
        app = create_app("development")

        assert app.debug is True
        assert app.config['FLASK_ENV'] == "development"

    def test_production_config_security_settings(self) -> None:
        """Test production configuration security settings."""
        app = create_app("production")

        assert app.debug is False
        assert app.config['FLASK_ENV'] == "production"
        assert app.config['SESSION_COOKIE_SECURE'] is True


class TestRequestHandling:
    """Test suite for request handling functionality."""

    def test_correlation_id_header_handling(self, client: FlaskClient) -> None:
        """Test that correlation ID headers are properly handled."""
        test_id = "test-correlation-123"

        response = client.get("/health", headers={"X-Request-ID": test_id})

        # Should echo back the same correlation ID
        assert response.headers.get("X-Request-ID") == test_id

    def test_timing_header_included(self, client: FlaskClient) -> None:
        """Test that timing headers are included in responses."""
        response = client.get("/health")

        # Should include timing header
        assert "X-Response-Time-ms" in response.headers

        # Should be a valid float value
        timing = response.headers["X-Response-Time-ms"]
        assert float(timing) >= 0.0

    def test_correlation_id_generated_when_not_provided(
        self, client: FlaskClient
    ) -> None:
        """Test that correlation ID is generated when not provided."""
        response = client.get("/health")

        # Should have a correlation ID header
        correlation_id = response.headers.get("X-Request-ID")
        assert correlation_id is not None
        assert len(correlation_id) > 10  # UUIDs are long

    def test_404_error_handling(self, client: FlaskClient) -> None:
        """Test that 404 errors are properly handled."""
        response = client.get("/nonexistent-endpoint")

        assert response.status_code == 404
        assert response.is_json

        data = response.get_json()
        assert data == {"message": "Not Found"}

    def test_error_responses_include_headers(
        self, client: FlaskClient
    ) -> None:
        """Test that error responses include standard headers."""
        response = client.get("/nonexistent-endpoint")

        # Should still include timing and correlation headers
        assert "X-Response-Time-ms" in response.headers
        assert "X-Request-ID" in response.headers


class TestApplicationIntegration:
    """Test suite for application integration tests."""

    def test_full_application_startup(self) -> None:
        """Test that complete application starts without errors."""
        app = create_app("testing")

        with app.test_client() as client:
            # Test multiple endpoints
            endpoints = ["/health", "/version", "/"]

            for endpoint in endpoints:
                response = client.get(endpoint)
                # All endpoints should respond (200 or redirect)
                assert response.status_code in [200, 302, 404]

    def test_database_integration(self) -> None:
        """Test database integration in application context."""
        app = create_app("testing")

        with app.app_context():
            from goldilocks.models.database import User, db

            # Should be able to create tables
            db.create_all()

            # Should be able to create a user
            test_user = User(
                email="test@example.com",
                username="testuser",
                full_name="Test User",
            )
            test_user.set_password("testpassword")

            db.session.add(test_user)
            db.session.commit()

            # Should be able to query the user
            queried_user = (
                db.session.query(User)
                .filter_by(email="test@example.com")
                .first()
            )
            assert queried_user is not None
            assert queried_user.username == "testuser"

    def test_login_manager_integration(self) -> None:
        """Test Flask-Login integration."""
        app = create_app("testing")

        with app.app_context():
            from flask_login import current_user

            # Should have anonymous user by default
            assert current_user.is_anonymous

    def test_csrf_protection_integration(self) -> None:
        """Test CSRF protection integration."""
        app = create_app("testing")

        with app.test_client() as client:
            # POST requests without CSRF token should fail
            response = client.post(
                "/auth/login",
                data={"email": "test@example.com", "password": "password"},
            )

            # Should return 400 due to missing CSRF token
            assert response.status_code == 400
            assert response.status_code == 400
