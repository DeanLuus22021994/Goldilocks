def test_version_has_expected_keys(client, json_of):
    resp = client.get("/version")
    assert resp.status_code == 200
    data = json_of(resp)
    for key in ("app", "python", "flask", "platform"):
        assert key in data
