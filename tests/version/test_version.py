def test_version_response_includes_expected_keys(client, json_of) -> None:
    resp = client.get("/version")
    assert resp.status_code == 200
    data = json_of(resp)
    assert {"app", "python", "flask", "platform"}.issubset(data.keys())
