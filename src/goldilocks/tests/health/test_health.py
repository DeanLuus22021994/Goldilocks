"""Tests for /health endpoint responses and headers."""

from collections.abc import Callable
from typing import Any

from flask.testing import FlaskClient


def test_health_status_ok(client: FlaskClient[Any]) -> None:
    """Return HTTP 200 for GET /health."""
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_body_ok(
    client: FlaskClient[Any],
    json_of: Callable[[Any], dict[str, Any]],
) -> None:
    """Return JSON body {'status': 'ok'}."""
    resp = client.get("/health")
    assert json_of(resp) == {"status": "ok"}


def test_health_sets_correlation_header_when_provided(
    client: FlaskClient[Any], correlation_id_header: dict[str, str]
) -> None:
    """Echo provided X-Request-ID header."""
    resp = client.get("/health", headers=correlation_id_header)
    expected_id = correlation_id_header["X-Request-ID"]
    assert resp.headers.get("X-Request-ID") == expected_id


def test_health_generates_correlation_header_when_missing(
    client: FlaskClient[Any],
) -> None:
    """Generate X-Request-ID when missing."""
    resp = client.get("/health")
    cid = resp.headers.get("X-Request-ID")
    assert isinstance(cid, str) and len(cid) >= 16


def test_health_has_response_time_header(client: FlaskClient[Any]) -> None:
    """Include X-Response-Time-ms header >= 0.0."""
    resp = client.get("/health")
    val = resp.headers.get("X-Response-Time-ms")
    assert val is not None and float(val) >= 0.0


def test_health_head_ok(client: FlaskClient[Any]) -> None:
    """Return HTTP 200 for HEAD /health."""
    resp = client.head("/health")
    assert resp.status_code == 200
