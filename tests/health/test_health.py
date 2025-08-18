from typing import Any, Callable

from flask.testing import FlaskClient


def test_health_status_ok(client: FlaskClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_body_ok(client: FlaskClient, json_of: Callable[[Any], dict[str, Any]]) -> None:
    resp = client.get("/health")
    assert json_of(resp) == {"status": "ok"}


def test_health_sets_correlation_header_when_provided(
    client: FlaskClient, correlation_id_header: dict[str, str]
) -> None:
    resp = client.get("/health", headers=correlation_id_header)
    assert resp.headers.get("X-Request-ID") == correlation_id_header["X-Request-ID"]


def test_health_generates_correlation_header_when_missing(client: FlaskClient) -> None:
    resp = client.get("/health")
    cid = resp.headers.get("X-Request-ID")
    assert isinstance(cid, str) and len(cid) >= 16


def test_health_has_response_time_header(client: FlaskClient) -> None:
    resp = client.get("/health")
    val = resp.headers.get("X-Response-Time-ms")
    assert val is not None and float(val) >= 0.0


def test_health_head_ok(client: FlaskClient) -> None:
    resp = client.head("/health")
    assert resp.status_code == 200
