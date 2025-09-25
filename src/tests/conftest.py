"""Test configuration and fixtures for Goldilocks test suite."""

from __future__ import annotations

import json
from collections.abc import Callable, Generator
from typing import Any, cast

import pytest
from flask import Flask
from flask.testing import FlaskClient

# Import the Flask app from our package
from goldilocks.app import app as flask_app

# Import our models for fixtures
from goldilocks.models.database import User, db

# Cached terminal reporter and verbosity settings
_TR: Any = None
_QUIET = False


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with terminal reporter and verbosity settings."""
    global _TR, _QUIET  # pylint: disable=global-statement
    _TR = config.pluginmanager.get_plugin("terminalreporter")
    _QUIET = bool(getattr(config.option, "quiet", 0))


@pytest.fixture(scope="session", name="app")
def app_fixture() -> Flask:
    """Return the Flask app instance once per test session."""
    return flask_app


@pytest.fixture(autouse=True)
def _reset_database(app: Flask) -> Generator[None]:
    """Ensure a clean database state for every test."""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """Lightweight test client per test for isolation."""
    return app.test_client()


@pytest.fixture()
def json_of() -> Callable[[Any], dict[str, Any]]:
    """Decode a Flask response body to JSON."""

    def _json(resp: Any) -> dict[str, Any]:
        return cast(dict[str, Any], json.loads(resp.data.decode("utf-8")))

    return _json


@pytest.fixture()
def correlation_id_header() -> dict[str, str]:
    """Provide a stable correlation ID header for tests."""
    return {"X-Request-ID": "test-cid-123"}


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Emit a brief RAG status line per test when not in quiet mode."""
    if report.when != "call" or _TR is None or _QUIET:
        return

    outcome = report.outcome  # 'passed' | 'failed' | 'skipped'
    if outcome == "passed":
        rag = "GREEN"
    elif outcome == "failed":
        rag = "RED"
    else:
        rag = "AMBER"

    if getattr(report, "wasxfail", False):
        rag = "AMBER"

    _TR.write_line(
        f"{rag} {report.nodeid}",
        green=outcome == "passed",
        red=outcome == "failed",
        yellow=(outcome == "skipped" or getattr(report, "wasxfail", False)),
    )


def pytest_report_teststatus(
    report: pytest.TestReport,
    config: pytest.Config,  # pylint: disable=unused-argument
) -> tuple[str, str, str] | None:
    """Customize short progress output to R/A/G letters for -q mode."""
    if report.when != "call":
        # For setup/teardown failures or skips
        if report.skipped:
            return "skipped", "A", "AMBER"
        if report.failed:
            return "failed", "R", "RED"
        return None

    if report.passed:
        return "passed", "G", "GREEN"
    if report.skipped:
        return "skipped", "A", "AMBER"
    if report.failed:
        return "failed", "R", "RED"
    return None


@pytest.fixture()
def test_user() -> User:
    """Create a test user instance."""
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        role="user",
    )
    user.set_password("TestPassword123!")
    user.active = True
    user.is_verified = False
    return user


@pytest.fixture()
def admin_user() -> User:
    """Create a test admin user instance."""
    user = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        role="admin",
    )
    user.set_password("AdminPassword123!")
    user.active = True
    user.is_verified = True
    return user
