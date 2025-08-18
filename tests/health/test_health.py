def test_health_status_ok(client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_body_ok(client, json_of) -> None:
    resp = client.get("/health")
    assert json_of(resp) == {"status": "ok"}


def test_health_sets_correlation_header_when_provided(client, correlation_id_header) -> None:
    resp = client.get("/health", headers=correlation_id_header)
    assert resp.headers.get("X-Request-ID") == correlation_id_header["X-Request-ID"]


def test_health_generates_correlation_header_when_missing(client) -> None:
    resp = client.get("/health")
    cid = resp.headers.get("X-Request-ID")
    assert isinstance(cid, str) and len(cid) >= 16


def test_health_has_response_time_header(client) -> None:
    resp = client.get("/health")
    val = resp.headers.get("X-Response-Time-ms")
    assert val is not None and float(val) >= 0.0


def test_health_head_ok(client) -> None:
    resp = client.head("/health")
    assert resp.status_code == 200
