"""Goldilocks Flask application entry point.

This module provides the main Flask application instance using the
application factory pattern for proper structure and testability.
"""

import os

from goldilocks.core.app_factory import create_app

# Create Flask application using factory pattern
config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

# For compatibility with existing deployment scripts
__all__ = ["app"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
