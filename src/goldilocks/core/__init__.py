"""Goldilocks core functionality.

Contains the core business logic, configuration management,
and shared utilities for the Goldilocks Flask application.

This module provides:
- Configuration management and environment setup
- Core application utilities and helpers
- Shared constants and application state management
- Base classes for business logic components
"""

import os
from typing import Any


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://goldilocks_user:goldilocks_pass_2024@" "localhost:3306/goldilocks",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
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
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Configuration mapping
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


# Core configuration constants
DEFAULT_CONFIG = {
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
