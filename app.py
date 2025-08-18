"""Goldilocks Flask app: structured logging, correlation ID, health and
version endpoints.
"""

import importlib
import logging
import platform
import time
import uuid
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from logging import StreamHandler, getLogger
from typing import Tuple

from flask import Flask, Response, g, jsonify, request

app = Flask(__name__)

logger = getLogger("goldilocks")
handler = StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

# Prefer JSON logs if available; fall back to plain text.
try:
    jsonlogger_mod = importlib.import_module("pythonjsonlogger.jsonlogger")
    JsonFormatter = getattr(jsonlogger_mod, "JsonFormatter")
    formatter = JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
except (ModuleNotFoundError, ImportError, AttributeError):  # pragma: no cover
    pass

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel("INFO")
app.logger.handlers = []
app.logger.propagate = True


@app.before_request
def add_correlation_id_and_timing() -> None:
    """Attach a correlation ID and start time to the request context."""
    g.start_time = time.perf_counter()
    g.correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())


@app.after_request
def add_response_headers(resp: Response) -> Response:
    """Add correlation ID/time headers and emit a structured access log."""
    resp.headers["X-Request-ID"] = getattr(g, "correlation_id", "")
    start_time = getattr(g, "start_time", time.perf_counter())
    duration_ms = int((time.perf_counter() - start_time) * 1000)
    resp.headers["X-Response-Time-ms"] = str(duration_ms)
    logger.info(
        "request",
        extra={
            "method": request.method,
            "path": request.path,
            "status": resp.status_code,
            "duration_ms": duration_ms,
            "remote_addr": request.remote_addr,
            "user_agent": request.headers.get("User-Agent", ""),
            "correlation_id": getattr(g, "correlation_id", ""),
        },
    )
    return resp


@app.get("/")
def index() -> Response:
    """Serve the static index page."""
    return app.send_static_file("index.html")


@app.get("/healthz")
def healthz() -> Tuple[Response, int]:
    """Readiness/liveness probe."""
    return jsonify(status="ok"), 200


@app.get("/version")
def version() -> Tuple[Response, int]:
    """Return application, Python, Flask, and platform versions."""
    try:
        flask_version = pkg_version("Flask")
    except PackageNotFoundError:  # pragma: no cover
        flask_version = "unknown"
    return (
        jsonify(
            app="goldilocks",
            python=platform.python_version(),
            flask=flask_version,
            platform=platform.platform(),
        ),
        200,
    )


@app.errorhandler(404)
def not_found(_: Exception) -> Tuple[Response, int]:
    """Return a structured 404 JSON response."""
    return jsonify(message="Not Found", status=404), 404
