"""Goldilocks core functionality.

Contains the core business logic, configuration management,
and shared utilities for the Goldilocks Flask application.

This module provides:
- Configuration management and environment setup
- Core application utilities and helpers
- Shared constants and application state management
- Base classes for business logic components
"""

from __future__ import annotations

import os
from typing import Any

from sqlalchemy.pool import StaticPool


def get_engine_options(db_uri: str) -> dict[str, Any]:
    """Get appropriate engine options based on database URI."""
    if db_uri.startswith("sqlite"):
        return {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    else:
        return {
            "pool_size": 10,
            "pool_timeout": 30,
            "pool_recycle": 1800,  # Recycle connections every 30 minutes
            "max_overflow": 20,
            "pool_pre_ping": True,  # Test connections before use
            "connect_args": {
                "connect_timeout": 10,
                "read_timeout": 30,
                "write_timeout": 30,
                "charset": "utf8mb4",
                "use_unicode": True,
                "autocommit": False,
            },
        }


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://goldilocks_user:goldilocks_pass_2024@" "localhost:3306/goldilocks",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_SESSION_OPTIONS = {"expire_on_commit": False}

    # Set engine options based on current DATABASE_URL
    _db_uri = os.environ.get(
        "DATABASE_URL", "mysql+pymysql://goldilocks_user:goldilocks_pass_2024@localhost:3306/goldilocks"
    )
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, Any] = get_engine_options(_db_uri)

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    FLASK_ENV = "production"
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")

    # Override engine options for SQLite testing
    SQLALCHEMY_ENGINE_OPTIONS: dict[str, Any] = get_engine_options("sqlite:///:memory:")


# Configuration mapping
config: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


# Core configuration constants
DEFAULT_CONFIG: dict[str, Any] = {
    "FLASK_APP": "goldilocks.app",
    "FLASK_ENV": "production",
    "LOG_LEVEL": "INFO",
    "REQUEST_TIMEOUT": 30,
    "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,  # 16MB
}

# Application metadata for introspection
PACKAGE_INFO = {
    "name": "goldilocks",
    "description": "High-performance Flask application with optimization",
    "author": "Goldilocks Development Team",
    "license": "MIT",
}


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value with fallback to default."""
    return DEFAULT_CONFIG.get(key, default)
