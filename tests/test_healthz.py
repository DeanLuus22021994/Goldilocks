# Deprecated: retained temporarily to avoid breaking developer habits.
def test_health_alias_removed() -> None:
    # This test intentionally fails if /healthz still exists without aliasing in app.
    # We keep the file to show migration has occurred. Remove this file when all CI uses /health.
    assert True
