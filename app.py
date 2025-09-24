#!/usr/bin/env python3
"""Goldilocks Flask Application - Modern Python 3.13.7 Implementation."""

from __future__ import annotations

import json
import logging
import platform
import time
import uuid

import flask
from flask import Flask, g, request, send_from_directory

# Configure structured logging with modern Python 3.13 features
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Create and configure Flask application with modern Python 3.13.7."""
    app = Flask(
        __name__,
        static_folder='frontend/static',
        static_url_path='/',
    )

    @app.before_request
    def before_request() -> None:
        """Process request with structured logging and correlation ID."""
        g.start_time = time.perf_counter()  # More precise timing
        g.request_id = str(uuid.uuid4())[:8]

        logger.info(
            json.dumps(
                {
                    'timestamp': time.time(),
                    'request_id': g.request_id,
                    'method': request.method,
                    'path': request.path,
                    'remote_addr': request.remote_addr,
                    'user_agent': request.headers.get('User-Agent', ''),
                    'event': 'request_start',
                },
                separators=(',', ':'),  # Compact JSON
            )
        )

    @app.after_request
    def after_request(response: flask.Response) -> flask.Response:
        """Add response headers and logging with modern timing."""
        duration = time.perf_counter() - g.start_time
        duration_ms = round(duration * 1000, 2)

        logger.info(
            json.dumps(
                {
                    'timestamp': time.time(),
                    'request_id': g.request_id,
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_ms': duration_ms,
                    'response_size': len(response.get_data()),
                    'event': 'request_complete',
                },
                separators=(',', ':'),
            )
        )

        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-Response-Time'] = f'{duration:.3f}s'

        return response

    @app.route('/')
    def index() -> flask.Response:
        """Serve the main application page."""
        static_folder = app.static_folder or 'frontend/static'
        return send_from_directory(static_folder, 'index.html')

    @app.route('/health')
    def health() -> dict[str, str | float]:
        """Health check endpoint with typed response."""
        return {
            'status': 'healthy',
            'timestamp': time.time(),
        }

    @app.route('/version')
    def version() -> dict[str, str | float]:
        """Version information endpoint with modern Python detection."""
        flask_version = getattr(flask, '__version__', 'unknown')

        return {
            'app': '1.0.0',
            'python': platform.python_version(),
            'flask': flask_version,
            'timestamp': time.time(),
        }

    @app.errorhandler(404)
    def not_found(_error: Exception) -> tuple[dict[str, str], int]:
        """Handle 404 errors with structured JSON response."""
        return {
            'error': 'Not Found',
            'message': 'The requested resource was not found',
        }, 404

    return app


# Create the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=9000,
        debug=True,
        use_reloader=True,
        threaded=True,
    )
