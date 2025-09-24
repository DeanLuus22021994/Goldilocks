"""Database models for user authentication and management - SQLAlchemy 1.4 compatible."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False,
                  default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum("user", "admin", "moderator",
                  name="user_role"), default="user")
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login_at = Column(DateTime(timezone=True))

    # Relationships
    sessions = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user",
                           uselist=False, cascade="all, delete-orphan")
    activity_logs = relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Set password hash."""
        self.password_hash = generate_password_hash(
            password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """Required by Flask-Login."""
        return str(self.id)

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"

    def to_dict(self) -> dict[str, Any]:
        """Convert user to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "avatar_url": self.avatar_url,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class UserSession(db.Model):
    """User session model for authentication management."""

    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="sessions")

    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.now(timezone.utc) > self.expires_at

    def to_dict(self) -> dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
        }

    def __repr__(self) -> str:
        return f"<UserSession {self.session_id}>"


class UserProfile(db.Model):
    """Extended user profile information."""

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),
                     unique=True, nullable=False)
    bio = Column(Text)
    location = Column(String(255))
    website = Column(String(500))
    company = Column(String(255))
    job_title = Column(String(255))
    timezone = Column(String(64), default="UTC")
    language = Column(String(8), default="en")
    theme = Column(Enum("light", "dark", "auto",
                   name="theme_type"), default="auto")
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="profile")

    def to_dict(self) -> dict[str, Any]:
        """Convert profile to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "location": self.location,
            "website": self.website,
            "company": self.company,
            "job_title": self.job_title,
            "timezone": self.timezone,
            "language": self.language,
            "theme": self.theme,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<UserProfile {self.user_id}>"


class ActivityLog(db.Model):
    """Activity logging for audit and analytics."""

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(64), nullable=False)
    resource_type = Column(String(64))
    resource_id = Column(String(255))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    def to_dict(self) -> dict[str, Any]:
        """Convert activity log to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<ActivityLog {self.action}>"


class SystemSetting(db.Model):
    """System configuration settings."""

    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True)
    key_name = Column(String(255), unique=True, nullable=False)
    value_text = Column(Text)
    value_type = Column(Enum("string", "integer", "boolean",
                        "json", name="setting_type"), default="string")
    description = Column(Text)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def get_value(self) -> Any:
        """Get typed value based on value_type."""
        if self.value_text is None:
            return None

        if self.value_type == "integer":
            return int(self.value_text)
        elif self.value_type == "boolean":
            return self.value_text.lower() in ("true", "1", "yes", "on")
        elif self.value_type == "json":
            import json
            return json.loads(self.value_text)
        else:
            return self.value_text

    def set_value(self, value: Any) -> None:
        """Set value with automatic type detection."""
        if isinstance(value, bool):
            self.value_type = "boolean"
            self.value_text = str(value).lower()
        elif isinstance(value, int):
            self.value_type = "integer"
            self.value_text = str(value)
        elif isinstance(value, (dict, list)):
            self.value_type = "json"
            import json
            self.value_text = json.dumps(value)
        else:
            self.value_type = "string"
            self.value_text = str(value)

    def to_dict(self) -> dict[str, Any]:
        """Convert setting to dictionary."""
        return {
            "id": self.id,
            "key_name": self.key_name,
            "value": self.get_value(),
            "value_type": self.value_type,
            "description": self.description,
            "is_public": self.is_public,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<SystemSetting {self.key_name}>"
