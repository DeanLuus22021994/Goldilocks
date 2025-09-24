#!/usr/bin/env python3
"""Goldilocks Flask Application - Simple Working Version."""

import json
import logging
import platform
import time
import uuid

import flask
from flask import Flask, g, request, send_from_directory

# Configure structured logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__, static_folder='frontend/static', static_url_path='/')

    @app.before_request
    def before_request():
        g.start_time = time.time()
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
                }
            )
        )

    @app.after_request
    def after_request(response):
        duration = time.time() - g.start_time

        logger.info(
            json.dumps(
                {
                    'timestamp': time.time(),
                    'request_id': g.request_id,
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_ms': round(duration * 1000, 2),
                    'response_size': len(response.get_data()),
                    'event': 'request_complete',
                }
            )
        )

        response.headers['X-Request-ID'] = g.request_id
        response.headers['X-Response-Time'] = f"{duration:.3f}s"

        return response

    @app.route('/')
    def index():
        """Serve the main application page."""
        static_folder = app.static_folder or 'frontend/static'
        return send_from_directory(static_folder, 'index.html')

    @app.route('/health')
    def health():
        """Health check endpoint."""
        return {'status': 'healthy', 'timestamp': time.time()}

    @app.route('/version')
    def version():
        """Version information endpoint."""
        return {
            'app': '1.0.0',
            'python': platform.python_version(),
            'flask': flask.__version__ if hasattr(flask, '__version__') else 'unknown',  # noqa
            'timestamp': time.time(),
        }

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors with JSON response."""
        return {'error': 'Not Found', 'message': 'The requested resource was not found'}, 404

    return app


# Create the Flask application
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
