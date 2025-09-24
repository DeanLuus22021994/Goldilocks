"""Simplified database models for user authentication - Compatible version."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    avatar_url = db.Column(db.String(500))
    # Renamed to avoid conflict with UserMixin
    active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    # Simplified to avoid enum issues
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime(timezone=True),
                           default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
    last_login_at = db.Column(db.DateTime(timezone=True))

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

    def is_active(self) -> bool:  # type: ignore[override]
        """Override UserMixin property - required by Flask-Login."""
        return self.active

    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.role == "admin"

    # Relationships
    profile = db.relationship(
        "UserProfile", back_populates="user", uselist=False, lazy="select")
    sessions = db.relationship(
        "UserSession", back_populates="user", lazy="dynamic")
    activity_logs = db.relationship(
        "ActivityLog", back_populates="user", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

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


class UserSession(db.Model):
    """User session model for authentication management."""

    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship("User", back_populates="sessions")

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
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
        }

    def __repr__(self) -> str:
        return f"<UserSession {self.session_id}>"


class UserProfile(db.Model):
    """Extended user profile information."""

    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), unique=True, nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(255))
    website = db.Column(db.String(500))
    company = db.Column(db.String(255))
    job_title = db.Column(db.String(255))
    timezone = db.Column(db.String(64), default="UTC")
    language = db.Column(db.String(8), default="en")
    theme = db.Column(db.String(20), default="auto")
    created_at = db.Column(db.DateTime(timezone=True),
                           default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", back_populates="profile")

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
    """Activity log for audit and analytics."""

    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.String(100))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    metadata_json = db.Column(db.Text)  # JSON string instead of JSON type
    created_at = db.Column(db.DateTime(timezone=True),
                           default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", back_populates="activity_logs")

    def to_dict(self) -> dict[str, Any]:
        """Convert activity log to dictionary."""
        return {
            "id": self.id,
            "action": self.action,
            "user_id": self.user_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "metadata_json": self.metadata_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<ActivityLog {self.action}>"
