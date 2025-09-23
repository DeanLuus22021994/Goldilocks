"""Goldilocks Flask app: structured logging, correlation ID, health and
version endpoints.
"""

from __future__ import annotations

import importlib
import logging
import os
import sys
import time
import uuid
import warnings
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from logging import StreamHandler, getLogger

import flask as flask_module
from flask import Flask, Response, g, jsonify, request

# Get the path to the frontend static directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_FOLDER = os.path.join(BASE_DIR, "frontend", "static")

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="/static")


class CorrelationIdFilter(logging.Filter):
    """Ensure every log record contains a correlation_id field."""

    def filter(self, record: logging.LogRecord) -> bool:
        # pragma: no cover - thin shim
        try:
            record.correlation_id = getattr(g, "correlation_id", "-")
        except RuntimeError:  # outside request context
            record.correlation_id = "-"
        return True


# Logging: prefer JSON logs if python-json-logger is available
logger = getLogger("goldilocks")
handler = StreamHandler()
handler.addFilter(CorrelationIdFilter())

formatter: logging.Formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s"
)
try:
    jsonlogger_mod = importlib.import_module("pythonjsonlogger.jsonlogger")
    JsonFormatter = jsonlogger_mod.JsonFormatter
    log_format = "%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s"
    formatter = JsonFormatter(log_format)
except (ImportError, AttributeError):  # pragma: no cover
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


@app.before_request
def add_correlation_id_and_timing() -> None:
    """Attach a correlation ID and start time to the request context."""
    cid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    g.correlation_id = cid
    g.start_time = time.perf_counter()


@app.after_request
def add_response_headers(resp: Response) -> Response:
    """Add correlation ID and timing headers to response."""
    # Correlation ID and simple timing
    cid = getattr(g, "correlation_id", None)
    if cid:
        resp.headers["X-Request-ID"] = cid
    start = getattr(g, "start_time", None)
    if start is not None:
        dur_ms = (time.perf_counter() - start) * 1000.0
        resp.headers["X-Response-Time-ms"] = f"{dur_ms:.2f}"
        logger.info(
            "request",
            extra={
                "path": request.path,
                "method": request.method,
                "status": resp.status_code,
                "duration_ms": round(dur_ms, 2),
            },
        )
    return resp


@app.get("/")
def index() -> Response:
    """Serve the static index page."""
    return app.send_static_file("index.html")


@app.get("/health")
def health() -> tuple[Response, int]:
    """Return health status of the application."""
    return jsonify({"status": "ok"}), 200


@app.get("/version")
def version() -> tuple[Response, int]:
    """Return versions for the app, Python, Flask, and platform."""
    # app version can be provided via env APP_VERSION, else package metadata,
    # else fallback
    app_version = os.environ.get("APP_VERSION")
    if not app_version:
        try:
            # Prefer package metadata for our distribution name if installed
            app_version = pkg_version("goldilocks")
        except PackageNotFoundError:
            # Fallback to package variable defined in __init__
            try:
                # Import at module level to avoid pylint warning
                import goldilocks

                app_version = getattr(goldilocks, "__version__", "0.1.0")
            except (ImportError, AttributeError):  # pragma: no cover
                app_version = "0.1.0"  # pragma: no cover

    try:
        flask_version = pkg_version("Flask")
    except PackageNotFoundError:  # pragma: no cover
        # Fallback for unusual environments
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            flask_version = getattr(flask_module, "__version__", "unknown")

    data = {
        "app": app_version,
        "python": sys.version.split()[0],
        "flask": flask_version,
        "platform": sys.platform,
    }
    return jsonify(data), 200


@app.errorhandler(404)
def not_found(_: Exception) -> tuple[Response, int]:
    """Handle 404 errors with JSON response."""
    return jsonify({"message": "Not Found"}), 404


# Explicit exports for typing and tests
__all__ = ["app", "pkg_version"]
