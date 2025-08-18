import logging
import platform
import time
import uuid
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from logging import StreamHandler, getLogger

from flask import Flask, g, jsonify, request

app = Flask(__name__)

logger = getLogger("goldilocks")
handler = StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
try:
    from pythonjsonlogger import jsonlogger  # type: ignore

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s")
except Exception:  # pragma: no cover
    pass
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel("INFO")
app.logger.handlers = []
app.logger.propagate = True


@app.before_request
def add_correlation_id_and_timing():
    g.start_time = time.perf_counter()
    g.correlation_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())


@app.after_request
def add_response_headers(resp):
    resp.headers["X-Request-ID"] = getattr(g, "correlation_id", "")
    duration_ms = int(
        (time.perf_counter() - getattr(g, "start_time", time.perf_counter())) * 1000)
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
def index():
    return app.send_static_file("index.html")


@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200


@app.get("/version")
def version():
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
def not_found(_):
    return jsonify(message="Not Found", status=404), 404
