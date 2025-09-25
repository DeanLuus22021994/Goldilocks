"""Flask application factory and configuration setup."""

from __future__ import annotations

import importlib
import logging
import os
import time
import uuid
from logging import StreamHandler, getLogger
from typing import Any

from flask import Flask, Response, g, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from goldilocks.api import api_bp
from goldilocks.api.auth import auth_bp
from goldilocks.api.main import main_bp
from goldilocks.core import config
from goldilocks.models.database import User, db
from goldilocks.services.auth import AuthenticationService


class CorrelationIdFilter(logging.Filter):
    """Ensure every log record contains a correlation_id field."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            if not hasattr(g, "correlation_id"):
                g.correlation_id = str(uuid.uuid4())
            record.correlation_id = getattr(g, "correlation_id", "-")
        except RuntimeError:
            # Outside application context, use a placeholder
            record.correlation_id = "-"
        return True


def setup_logging(app: Flask) -> None:
    """Set up structured logging with modern Python features."""
    logger = getLogger("goldilocks")
    handler = StreamHandler()

    # Modern log format for Python 3.13
    log_format = "%(asctime)s %(levelname)s %(name)s %(message)s"
    formatter = logging.Formatter(log_format)
    try:
        jsonlogger_mod = importlib.import_module("pythonjsonlogger.jsonlogger")
        json_formatter = jsonlogger_mod.JsonFormatter
        formatter = json_formatter(log_format)
    except (ImportError, AttributeError):
        pass

    handler.setFormatter(formatter)

    # Avoid duplicate handlers on reload
    if not any(isinstance(h, StreamHandler) for h in logger.handlers):
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Do not propagate to root to avoid double-logging when root has handlers
    logger.propagate = False

    # Propagate Flask's logs to the root logger and ensure it has our handler
    app.logger.handlers = []
    app.logger.propagate = True
    root_logger = logging.getLogger()
    if not any(isinstance(h, StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)


def setup_extensions(app: Flask) -> tuple[CSRFProtect, LoginManager]:
    """Initialize Flask extensions."""
    # Initialize CSRF protection
    csrf = CSRFProtect(app)

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Configure login manager properties
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:  # type: ignore[misc]
        """Load user by ID for Flask-Login."""
        return AuthenticationService.get_user_by_id(int(user_id))

    return csrf, login_manager


def setup_request_handlers(app: Flask) -> None:
    """Set up request/response handlers with modern timing."""

    @app.before_request
    def add_correlation_id_and_timing() -> None:
        """Add correlation ID and start timing for each request."""
        # Use provided X-Request-ID header or generate new UUID
        g.correlation_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.start_time = time.perf_counter()  # More precise timing

    @app.after_request
    def add_response_headers(response: Response) -> Response:
        """Add response headers including timing and correlation ID."""
        # Add timing header with precise measurements
        duration_ms = 0.0
        if hasattr(g, "start_time"):
            duration_ms = (time.perf_counter() - g.start_time) * 1000
            response.headers["X-Response-Time-ms"] = f"{duration_ms:.2f}"

        # Add correlation ID header
        if hasattr(g, "correlation_id"):
            response.headers["X-Request-ID"] = g.correlation_id

        # Log the request with structured logging
        logger = getLogger("goldilocks")
        logger.info(
            "request",
            extra={
                "path": request.path,
                "method": request.method,
                "status": response.status_code,
                "duration_ms": f"{duration_ms:.2f}",
            },
        )

        return response

    @app.errorhandler(404)
    def not_found(_error: Any) -> tuple[dict[str, str], int]:
        """Handle 404 errors with proper typing."""
        response_data = {"message": "Not Found"}
        return response_data, 404


def create_app(config_name: str = "default") -> Flask:
    """Create and configure Flask application with modern Python 3.13.7."""
    # Get the path to the project root directory
    # app_factory.py is in src/goldilocks/core/app_factory.py
    # We need to go up 3 levels to get to project root
    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    static_folder = os.path.join(base_dir, "frontend", "static")

    # Templates are now located in frontend/static/templates
    templates_folder = os.path.join(static_folder, "templates")

    # Create Flask app with static and template folders
    app = Flask(
        __name__,
        static_folder=static_folder,
        static_url_path="/static",
        template_folder=templates_folder,
    )  # Load configuration
    config_obj = config.get(config_name, config["default"])
    app.config.from_object(config_obj)

    # Set up logging
    setup_logging(app)

    # Initialize database
    db.init_app(app)

    # Set up extensions
    _csrf, _login_manager = setup_extensions(app)

    # Set up request handlers
    setup_request_handlers(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning("Could not create database tables: %s", e)

    return app
