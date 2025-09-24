"""Database models for user authentication and management."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, cast

# from flask_login import UserMixin  # removed to avoid subclassing Any
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    event,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash


# Introduce a typed declarative base and use it with Flask-SQLAlchemy
class Base(DeclarativeBase):
    pass


# db = SQLAlchemy()
db = SQLAlchemy(model_class=Base)

# Typed wrappers for werkzeug functions to satisfy mypy
_generate_password_hash: Callable[..., str] = cast(Any, generate_password_hash)
_check_password_hash: Callable[[str, str], bool] = cast(
    Any, check_password_hash
)


class User(Base):  # ← Type checker happy, fully modern
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    # Renamed to avoid UserMixin conflict
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[str] = mapped_column(
        Enum("user", "admin", "moderator", name="user_role"), default="user"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    # Relationships
    sessions: Mapped[list[UserSession]] = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )
    profile: Mapped[UserProfile | None] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    activity_logs: Mapped[list[ActivityLog]] = relationship(
        "ActivityLog", back_populates="user", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize user with UUID generation."""
        if "uuid" not in kwargs:
            kwargs["uuid"] = str(uuid.uuid4())
        super().__init__(**kwargs)

    def set_password(self, password: str) -> None:
        """Set password hash."""
        self.password_hash = _generate_password_hash(
            password, method="pbkdf2:sha256"
        )

    def check_password(self, password: str) -> bool:
        """Check password against hash."""
        return _check_password_hash(self.password_hash, password)

    def get_id(self) -> str:
        """Required by Flask-Login."""
        return str(self.id)

    @property
    def is_active(self) -> bool:
        """Check if user account is active (required by Flask-Login)."""
        return self.active

    # Minimal Flask-Login interface without UserMixin
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
            "last_login_at": (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def is_admin(self) -> bool:
        """Return True if the user has the admin role."""
        return (self.role or "").lower() == "admin"


class UserSession(Base):
    """User session model for authentication management."""

    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="sessions")

    def __init__(self, **kwargs: Any) -> None:
        """Initialize UserSession with proper parameter handling."""
        super().__init__(**kwargs)

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "expires_at": (
                self.expires_at.isoformat() if self.expires_at else None
            ),
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
        }

    def __repr__(self) -> str:
        return f"<UserSession {self.session_id}>"


class UserProfile(Base):
    """Extended user profile information."""

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    bio: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(String(255))
    website: Mapped[str | None] = mapped_column(String(500))
    company: Mapped[str | None] = mapped_column(String(255))
    job_title: Mapped[str | None] = mapped_column(String(255))
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    language: Mapped[str] = mapped_column(String(8), default="en")
    theme: Mapped[str] = mapped_column(
        Enum("light", "dark", "auto", name="theme_type"), default="auto"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="profile")

    def __init__(self, **kwargs: Any) -> None:
        """Initialize UserProfile with proper parameter handling."""
        super().__init__(**kwargs)

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }

    def __repr__(self) -> str:
        return f"<UserProfile {self.user_id}>"


class ActivityLog(Base):
    """Activity logging for audit and analytics."""

    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_type: Mapped[str | None] = mapped_column(String(64))
    resource_id: Mapped[str | None] = mapped_column(String(255))
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON
    )  # Renamed to avoid SQLAlchemy conflict
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped[User | None] = relationship(
        "User", back_populates="activity_logs"
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize ActivityLog with proper parameter handling."""
        # Handle metadata parameter -> metadata_json mapping
        if 'metadata' in kwargs:
            kwargs['metadata_json'] = kwargs.pop('metadata')
        super().__init__(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert activity log to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "ip_address": self.ip_address,
            "metadata": self.metadata_json,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
        }

    def __repr__(self) -> str:
        return f"<ActivityLog {self.action}>"


class SystemSetting(Base):
    """System configuration settings."""

    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    key_name: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    value_text: Mapped[str | None] = mapped_column(Text)
    value_type: Mapped[str] = mapped_column(
        Enum("string", "integer", "boolean", "json", name="setting_type"),
        default="string",
    )
    description: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __init__(self, **kwargs: Any) -> None:
        """Initialize SystemSetting with proper parameter handling."""
        super().__init__(**kwargs)

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
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            ),
        }

    def __repr__(self) -> str:
        return f"<SystemSetting {self.key_name}>"


# Event listeners for automatic UUID generation
@event.listens_for(User, "before_insert")
def generate_uuid(_mapper: Any, _connection: Any, target: User) -> None:
    """Generate UUID for new users if not provided."""
    if not target.uuid:
        target.uuid = str(uuid.uuid4())
