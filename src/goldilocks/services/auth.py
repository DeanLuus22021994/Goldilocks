"""Authentication service for user management."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from flask import current_app, request
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from goldilocks.models.database import (
    ActivityLog,
    User,
    UserProfile,
    UserSession,
    db,
)


class AuthenticationService:
    """Service for handling user authentication operations."""

    @staticmethod
    def create_user(
        email: str,
        username: str,
        password: str,
        full_name: str | None = None,
        role: str = "user",
    ) -> tuple[User | None, str | None]:
        """Create a new user account."""
        try:
            # Check if user already exists
            existing_user = (
                db.session.query(User)
                .filter((User.email == email) | (User.username == username))
                .first()
            )
            if existing_user:
                if existing_user.email == email:
                    return None, "An account with this email already exists"
                else:
                    return None, "This username is already taken"

            # Create new user
            user = User(
                email=email.lower().strip(),
                username=username.strip(),
                full_name=full_name.strip() if full_name else None,
                role=role,
            )
            user.set_password(password)

            db.session.add(user)
            db.session.flush()  # Get user ID

            # Create user profile
            profile = UserProfile(user_id=user.id)
            db.session.add(profile)

            # Log activity
            AuthenticationService.log_activity(
                user_id=user.id,
                action="user_registered",
                metadata={"email": email, "username": username, "role": role},
            )

            db.session.commit()
            return user, None

        except IntegrityError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error creating user: {e}")
            return None, "An error occurred while creating your account"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error creating user: {e}")
            return None, "An unexpected error occurred"

    @staticmethod
    def authenticate_user(
        email_or_username: str, password: str
    ) -> tuple[User | None, str | None]:
        """Authenticate user with email/username and password."""
        try:
            # Find user by email or username
            user = (
                db.session.query(User)
                .filter(
                    (User.email == email_or_username.lower().strip())
                    | (User.username == email_or_username.strip())
                )
                .first()
            )

            if not user:
                return None, "Invalid email/username or password"

            if not user.is_active:
                return None, "Your account has been deactivated"

            if not user.check_password(password):
                # Log failed login attempt
                AuthenticationService.log_activity(
                    user_id=user.id,
                    action="login_failed",
                    metadata={
                        "reason": "invalid_password",
                        "email": email_or_username,
                    },
                )
                return None, "Invalid email/username or password"

            # Update last login
            user.last_login_at = datetime.now(timezone.utc)

            # Log successful login
            AuthenticationService.log_activity(
                user_id=user.id,
                action="login_success",
                metadata={"email": user.email, "username": user.username},
            )

            db.session.commit()
            return user, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Authentication error: {e}")
            return None, "An error occurred during authentication"

    @staticmethod
    def create_session(user_id: int, remember_me: bool = False) -> str:
        """Create a new user session."""
        session_id = secrets.token_urlsafe(32)
        expires_delta = timedelta(days=30 if remember_me else 1)
        expires_at = datetime.now(timezone.utc) + expires_delta

        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
            expires_at=expires_at,
        )

        db.session.add(session)
        db.session.commit()

        return session_id

    @staticmethod
    def invalidate_session(session_id: str) -> bool:
        """Invalidate a user session."""
        try:
            session = (
                db.session.query(UserSession)
                .filter_by(session_id=session_id)
                .first()
            )
            if session:
                session.is_active = False
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error invalidating session: {e}")
            return False

    @staticmethod
    def invalidate_all_user_sessions(user_id: int) -> bool:
        """Invalidate all sessions for a user."""
        try:
            db.session.query(UserSession).filter_by(user_id=user_id).update(
                {"is_active": False}
            )
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error invalidating user sessions: {e}")
            return False

    @staticmethod
    def get_user_by_id(user_id: int) -> User | None:
        """Get user by ID."""
        return db.session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        """Get user by email."""
        return (
            db.session.query(User)
            .filter_by(email=email.lower().strip())
            .first()
        )

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        """Get user by username."""
        return (
            db.session.query(User).filter_by(username=username.strip()).first()
        )

    @staticmethod
    def update_user_profile(
        user_id: int,
        full_name: str | None = None,
        bio: str | None = None,
        location: str | None = None,
        website: str | None = None,
        company: str | None = None,
        job_title: str | None = None,
    ) -> tuple[bool, str | None]:
        """Update user profile information."""
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return False, "User not found"

            # Update user basic info
            if full_name is not None:
                user.full_name = full_name.strip() if full_name else None

            # Update or create profile
            profile = user.profile
            if not profile:
                profile = UserProfile(user_id=user_id)
                db.session.add(profile)

            if bio is not None:
                profile.bio = bio.strip() if bio else None
            if location is not None:
                profile.location = location.strip() if location else None
            if website is not None:
                profile.website = website.strip() if website else None
            if company is not None:
                profile.company = company.strip() if company else None
            if job_title is not None:
                profile.job_title = job_title.strip() if job_title else None

            # Log activity
            AuthenticationService.log_activity(
                user_id=user_id,
                action="profile_updated",
                metadata={
                    "updated_fields": [
                        k
                        for k, v in locals().items()
                        if k != "user_id" and v is not None
                    ]
                },
            )

            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating profile: {e}")
            return False, "An error occurred while updating your profile"

    @staticmethod
    def change_password(
        user_id: int, current_password: str, new_password: str
    ) -> tuple[bool, str | None]:
        """Change user password."""
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return False, "User not found"

            if not user.check_password(current_password):
                return False, "Current password is incorrect"

            user.set_password(new_password)

            # Invalidate all sessions except current one
            current_session_id = getattr(current_user, "_session_id", None)
            query = db.session.query(UserSession).filter_by(user_id=user_id)
            if current_session_id:
                query = query.filter(
                    UserSession.session_id != current_session_id
                )
            query.update({"is_active": False})

            # Log activity
            AuthenticationService.log_activity(
                user_id=user_id,
                action="password_changed",
                metadata={"sessions_invalidated": True},
            )

            db.session.commit()
            return True, None

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error changing password: {e}")
            return False, "An error occurred while changing your password"

    @staticmethod
    def get_user_stats() -> dict[str, Any]:
        """Get user statistics for dashboard."""
        try:
            total_users = db.session.query(User).count()
            active_users = (
                db.session.query(User).filter_by(is_active=True).count()
            )
            verified_users = (
                db.session.query(User).filter_by(is_verified=True).count()
            )
            admin_users = (
                db.session.query(User).filter_by(role="admin").count()
            )

            recent_logins = (
                db.session.query(User)
                .filter(
                    User.last_login_at
                    >= datetime.now(timezone.utc) - timedelta(days=7)
                )
                .count()
            )

            return {
                "total_users": total_users,
                "active_users": active_users,
                "verified_users": verified_users,
                "admin_users": admin_users,
                "recent_logins": recent_logins,
            }

        except Exception as e:
            current_app.logger.error(f"Error getting user stats: {e}")
            return {
                "total_users": 0,
                "active_users": 0,
                "verified_users": 0,
                "admin_users": 0,
                "recent_logins": 0,
            }

    @staticmethod
    def log_activity(
        action: str,
        user_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Log user activity."""
        try:
            activity = ActivityLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=request.remote_addr if request else None,
                user_agent=(
                    request.headers.get("User-Agent") if request else None
                ),
                metadata=metadata,
            )
            db.session.add(activity)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error logging activity: {e}")

    @staticmethod
    def cleanup_expired_sessions() -> int:
        """Clean up expired sessions."""
        try:
            count = (
                db.session.query(UserSession)
                .filter(UserSession.expires_at < datetime.now(timezone.utc))
                .update({"is_active": False})
            )
            db.session.commit()
            return count

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error cleaning up sessions: {e}")
            return 0
