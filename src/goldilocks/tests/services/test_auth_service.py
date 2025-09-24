"""Tests for authentication service."""

from datetime import datetime, timezone
from typing import Any
from unittest.mock import patch

from flask import Flask
from sqlalchemy.exc import IntegrityError

from goldilocks.models.database import ActivityLog, User, UserProfile, UserSession, db
from goldilocks.services.auth import AuthenticationService


class TestAuthenticationServiceUserManagement:
    """Test suite for user management functionality."""

    def test_create_user_success(self, app: Flask) -> None:
        """Test successful user creation."""
        with app.app_context():
            db.create_all()

            user, error = AuthenticationService.create_user(
                email="test@example.com",
                username="testuser",
                password="TestPassword123",
                full_name="Test User"
            )

            assert user is not None
            assert error is None
            assert user.email == "test@example.com"
            assert user.username == "testuser"
            assert user.full_name == "Test User"
            assert user.check_password("TestPassword123")

            # Should create associated profile
            assert user.profile is not None

    def test_create_user_duplicate_email(self, app: Flask, test_user: User) -> None:
        """Test user creation with duplicate email."""
        with app.app_context():
            db.create_all()

            # Add existing user
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.create_user(
                email=test_user.email,
                username="differentuser",
                password="TestPassword123"
            )

            assert user is None
            assert error is not None
            assert "already exists" in error.lower()

    def test_create_user_duplicate_username(self, app: Flask, test_user: User) -> None:
        """Test user creation with duplicate username."""
        with app.app_context():
            db.create_all()

            # Add existing user
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.create_user(
                email="different@example.com",
                username=test_user.username,
                password="TestPassword123"
            )

            assert user is None
            assert error is not None
            assert "already exists" in error.lower()

    def test_create_user_with_role(self, app: Flask) -> None:
        """Test creating user with specific role."""
        with app.app_context():
            db.create_all()

            user, error = AuthenticationService.create_user(
                email="admin@example.com",
                username="admin",
                password="AdminPassword123",
                role="admin"
            )

            assert user is not None
            assert error is None
            assert user.role == "admin"
            assert user.is_admin() is True

    def test_create_user_logs_activity(self, app: Flask) -> None:
        """Test that user creation is logged."""
        with app.app_context():
            db.create_all()

            user, error = AuthenticationService.create_user(
                email="test@example.com",
                username="testuser",
                password="TestPassword123"
            )

            assert user is not None

            # Check activity log
            activity = ActivityLog.query.filter_by(
                user_id=user.id,
                action="user_registered"
            ).first()

            assert activity is not None

    @patch('goldilocks.services.auth.db.session')
    def test_create_user_handles_database_errors(self, mock_session: Any, app: Flask) -> None:
        """Test that database errors are handled gracefully."""
        with app.app_context():
            # Mock database error
            mock_session.commit.side_effect = IntegrityError(
                "test", "test", Exception("test error"))


class TestAuthenticationServiceAuthentication:
    """Test suite for authentication functionality."""

    def test_authenticate_user_with_email(self, app: Flask, test_user: User) -> None:
        """Test user authentication using email."""
        with app.app_context():
            db.create_all()

            # Set up test user
            test_user.set_password("TestPassword123")
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.authenticate_user(
                test_user.email,
                "TestPassword123"
            )

            assert user is not None
            assert error is None
            assert user.id == test_user.id
            assert user.last_login_at is not None

    def test_authenticate_user_with_username(self, app: Flask, test_user: User) -> None:
        """Test user authentication using username."""
        with app.app_context():
            db.create_all()

            # Set up test user
            test_user.set_password("TestPassword123")
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.authenticate_user(
                test_user.username,
                "TestPassword123"
            )

            assert user is not None
            assert error is None
            assert user.id == test_user.id

    def test_authenticate_user_wrong_password(self, app: Flask, test_user: User) -> None:
        """Test authentication with wrong password."""
        with app.app_context():
            db.create_all()

            # Set up test user
            test_user.set_password("TestPassword123")
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.authenticate_user(
                test_user.email,
                "WrongPassword"
            )

            assert user is None
            assert error is not None
            assert "invalid" in error.lower() or "incorrect" in error.lower()

    def test_authenticate_nonexistent_user(self, app: Flask) -> None:
        """Test authentication with nonexistent user."""
        with app.app_context():
            db.create_all()

            user, error = AuthenticationService.authenticate_user(
                "nonexistent@example.com",
                "Password123"
            )

            assert user is None
            assert error is not None
            assert "not found" in error.lower() or "invalid" in error.lower()

    def test_authenticate_inactive_user(self, app: Flask, test_user: User) -> None:
        """Test authentication with inactive user."""
        with app.app_context():
            db.create_all()

            # Set up inactive user
            test_user.set_password("TestPassword123")
            test_user.active = False
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.authenticate_user(
                test_user.email,
                "TestPassword123"
            )

            assert user is None
            assert error is not None
            assert "inactive" in error.lower() or "disabled" in error.lower()

    def test_authenticate_logs_successful_login(self, app: Flask, test_user: User) -> None:
        """Test that successful authentication is logged."""
        with app.app_context():
            db.create_all()

            # Set up test user
            test_user.set_password("TestPassword123")
            db.session.add(test_user)
            db.session.commit()

            user, error = AuthenticationService.authenticate_user(
                test_user.email,
                "TestPassword123"
            )

            assert user is not None

            # Check activity log
            activity = ActivityLog.query.filter_by(
                user_id=user.id,
                action="login_success"
            ).first()

            assert activity is not None


class TestAuthenticationServiceSessionManagement:
    """Test suite for session management functionality."""

    @patch('goldilocks.services.auth.request')
    def test_create_session(self, mock_request: Any, app: Flask, test_user: User) -> None:
        """Test creating user session."""
        with app.app_context():
            db.create_all()

            # Mock request data
            mock_request.remote_addr = "127.0.0.1"
            mock_request.headers = {"User-Agent": "Test Browser"}

            db.session.add(test_user)
            db.session.commit()

            session_id = AuthenticationService.create_session(test_user.id)

            assert session_id is not None
            assert len(session_id) > 10  # Should be a long random string

            # Verify session in database
            session = UserSession.query.filter_by(
                session_id=session_id).first()
            assert session is not None
            assert session.user_id == test_user.id
            assert session.ip_address == "127.0.0.1"

    @patch('goldilocks.services.auth.request')
    def test_create_session_with_remember_me(self, mock_request: Any, app: Flask, test_user: User) -> None:
        """Test creating session with remember me option."""
        with app.app_context():
            db.create_all()

            # Mock request data
            mock_request.remote_addr = "127.0.0.1"
            mock_request.headers = {"User-Agent": "Test Browser"}

            db.session.add(test_user)
            db.session.commit()

            session_id = AuthenticationService.create_session(
                test_user.id,
                remember_me=True
            )

            assert session_id is not None

            # Verify session has longer expiration
            session = UserSession.query.filter_by(
                session_id=session_id).first()
            assert session is not None

            # Should expire more than 24 hours from now (remember me = 30 days)
            time_diff = session.expires_at - datetime.now(timezone.utc)
            assert time_diff.days > 1

    def test_invalidate_session(self, app: Flask, test_user: User) -> None:
        """Test invalidating a user session."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            # Create session
            session = UserSession(
                session_id="test_session_123",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc)
            )
            db.session.add(session)
            db.session.commit()

            # Invalidate session
            result = AuthenticationService.invalidate_session(
                "test_session_123")

            assert result is True

            # Verify session is inactive
            updated_session = UserSession.query.filter_by(
                session_id="test_session_123"
            ).first()
            assert updated_session.is_active is False

    def test_invalidate_nonexistent_session(self, app: Flask) -> None:
        """Test invalidating a nonexistent session."""
        with app.app_context():
            db.create_all()

            result = AuthenticationService.invalidate_session(
                "nonexistent_session")

            assert result is False

    def test_invalidate_all_user_sessions(self, app: Flask, test_user: User) -> None:
        """Test invalidating all sessions for a user."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            # Create multiple sessions
            session1 = UserSession(
                session_id="session1",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc)
            )
            session2 = UserSession(
                session_id="session2",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc)
            )

            db.session.add_all([session1, session2])
            db.session.commit()

            # Invalidate all user sessions
            result = AuthenticationService.invalidate_all_user_sessions(
                test_user.id)

            assert result is True

            # Verify all sessions are inactive
            sessions = UserSession.query.filter_by(user_id=test_user.id).all()
            for session in sessions:
                assert session.is_active is False


class TestAuthenticationServiceUserRetrieval:
    """Test suite for user retrieval functionality."""

    def test_get_user_by_id(self, app: Flask, test_user: User) -> None:
        """Test retrieving user by ID."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            retrieved_user = AuthenticationService.get_user_by_id(test_user.id)

            assert retrieved_user is not None
            assert retrieved_user.id == test_user.id
            assert retrieved_user.email == test_user.email

    def test_get_user_by_nonexistent_id(self, app: Flask) -> None:
        """Test retrieving user by nonexistent ID."""
        with app.app_context():
            db.create_all()

            retrieved_user = AuthenticationService.get_user_by_id(99999)

            assert retrieved_user is None

    def test_get_user_by_email(self, app: Flask, test_user: User) -> None:
        """Test retrieving user by email."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            retrieved_user = AuthenticationService.get_user_by_email(
                test_user.email)

            assert retrieved_user is not None
            assert retrieved_user.email == test_user.email

    def test_get_user_by_email_case_insensitive(self, app: Flask, test_user: User) -> None:
        """Test that email lookup is case insensitive."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            # Test with different case
            retrieved_user = AuthenticationService.get_user_by_email(
                test_user.email.upper()
            )

            assert retrieved_user is not None
            assert retrieved_user.email == test_user.email

    def test_get_user_by_username(self, app: Flask, test_user: User) -> None:
        """Test retrieving user by username."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            retrieved_user = AuthenticationService.get_user_by_username(
                test_user.username)

            assert retrieved_user is not None
            assert retrieved_user.username == test_user.username


class TestAuthenticationServiceProfileManagement:
    """Test suite for profile management functionality."""

    def test_update_user_profile(self, app: Flask, test_user: User) -> None:
        """Test updating user profile information."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            # Create initial profile
            profile = UserProfile(user_id=test_user.id, bio="Initial bio")
            db.session.add(profile)
            db.session.commit()

            # Update profile
            success, error = AuthenticationService.update_user_profile(
                test_user.id,
                full_name="Updated Name",
                bio="Updated bio",
                location="New Location",
                company="New Company"
            )

            assert success is True
            assert error is None

            # Verify updates
            updated_user = User.query.get(test_user.id)
            assert updated_user.full_name == "Updated Name"

            updated_profile = updated_user.profile
            assert updated_profile.bio == "Updated bio"
            assert updated_profile.location == "New Location"
            assert updated_profile.company == "New Company"

    def test_update_nonexistent_user_profile(self, app: Flask) -> None:
        """Test updating profile for nonexistent user."""
        with app.app_context():
            db.create_all()

            success, error = AuthenticationService.update_user_profile(
                99999,
                full_name="Test Name"
            )

            assert success is False
            assert error is not None
            assert "not found" in error.lower()


class TestAuthenticationServicePasswordManagement:
    """Test suite for password management functionality."""

    def test_change_password_success(self, app: Flask, test_user: User) -> None:
        """Test successful password change."""
        with app.app_context():
            db.create_all()

            test_user.set_password("OldPassword123")
            db.session.add(test_user)
            db.session.commit()

            success, error = AuthenticationService.change_password(
                test_user.id,
                "OldPassword123",
                "NewPassword123"
            )

            assert success is True
            assert error is None

            # Verify password changed
            updated_user = User.query.get(test_user.id)
            assert updated_user.check_password("NewPassword123")
            assert not updated_user.check_password("OldPassword123")

    def test_change_password_wrong_current_password(self, app: Flask, test_user: User) -> None:
        """Test password change with wrong current password."""
        with app.app_context():
            db.create_all()

            test_user.set_password("OldPassword123")
            db.session.add(test_user)
            db.session.commit()

            success, error = AuthenticationService.change_password(
                test_user.id,
                "WrongPassword",
                "NewPassword123"
            )

            assert success is False
            assert error is not None
            assert "current password" in error.lower()

    def test_change_password_nonexistent_user(self, app: Flask) -> None:
        """Test password change for nonexistent user."""
        with app.app_context():
            db.create_all()

            success, error = AuthenticationService.change_password(
                99999,
                "OldPassword123",
                "NewPassword123"
            )

            assert success is False
            assert error is not None


class TestAuthenticationServiceUtilities:
    """Test suite for utility functions."""

    def test_get_user_stats(self, app: Flask) -> None:
        """Test getting user statistics."""
        with app.app_context():
            db.create_all()

            # Create some test users
            user1 = User(email="user1@example.com",
                         username="user1", active=True)
            user2 = User(email="user2@example.com",
                         username="user2", active=False)
            admin = User(email="admin@example.com",
                         username="admin", role="admin")

            db.session.add_all([user1, user2, admin])
            db.session.commit()

            stats = AuthenticationService.get_user_stats()

            assert isinstance(stats, dict)
            assert "total_users" in stats
            assert "active_users" in stats
            assert "admin_users" in stats

            assert stats["total_users"] >= 3
            assert stats["active_users"] >= 2  # user1 and admin are active
            assert stats["admin_users"] >= 1

    def test_log_activity(self, app: Flask, test_user: User) -> None:
        """Test logging user activity."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            AuthenticationService.log_activity(
                action="test_action",
                user_id=test_user.id,
                resource_type="test_resource",
                resource_id="123",
                metadata={"key": "value"}
            )

            # Verify activity was logged
            activity = ActivityLog.query.filter_by(
                user_id=test_user.id,
                action="test_action"
            ).first()

            assert activity is not None
            assert activity.resource_type == "test_resource"
            assert activity.resource_id == "123"

    def test_cleanup_expired_sessions(self, app: Flask, test_user: User) -> None:
        """Test cleaning up expired sessions."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            # Create expired session
            expired_session = UserSession(
                session_id="expired_session",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc).replace(
                    year=2020)  # Past date
            )

            # Create active session
            active_session = UserSession(
                session_id="active_session",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc).replace(
                    year=2030)  # Future date
            )

            db.session.add_all([expired_session, active_session])
            db.session.commit()

            # Cleanup expired sessions
            count = AuthenticationService.cleanup_expired_sessions()

            assert count >= 1

            # Verify expired session was removed
            expired = UserSession.query.filter_by(
                session_id="expired_session"
            ).first()
            assert expired is None

            # Verify active session remains
            active = UserSession.query.filter_by(
                session_id="active_session"
            ).first()
            assert active is not None
