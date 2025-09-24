"""Tests for database models."""

import uuid
from datetime import datetime, timezone

from flask import Flask
from sqlalchemy.exc import IntegrityError

from goldilocks.models.database import ActivityLog, SystemSetting, User, UserProfile, UserSession, db


class TestUserModel:
    """Test suite for User model."""

    def test_user_creation(self, app: Flask) -> None:
        """Test creating a user with required fields."""
        with app.app_context():
            db.create_all()

            user = User(
                email="test@example.com",
                username="testuser",
                full_name="Test User"
            )
            user.set_password("testpassword123")

            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.username == "testuser"
            assert user.full_name == "Test User"
            assert user.uuid is not None
            assert user.created_at is not None

    def test_user_password_hashing(self, app: Flask) -> None:
        """Test password hashing and verification."""
        with app.app_context():
            user = User(email="test@example.com", username="testuser")
            password = "mysecretpassword"

            user.set_password(password)

            # Password should be hashed
            assert user.password_hash != password
            assert len(user.password_hash) > 20

            # Should verify correct password
            assert user.check_password(password) is True
            assert user.check_password("wrongpassword") is False

    def test_user_active_status(self, app: Flask) -> None:
        """Test user active status functionality."""
        with app.app_context():
            user = User(email="test@example.com", username="testuser")

            # Default should be active
            assert user.is_active() is True

            # Should handle explicit active status
            user.active = False
            assert user.is_active() is False

            user.active = True
            assert user.is_active() is True

    def test_user_admin_status(self, app: Flask) -> None:
        """Test user admin role functionality."""
        with app.app_context():
            # Regular user
            user = User(email="test@example.com", username="testuser")
            assert user.is_admin() is False

            # Admin user
            admin = User(email="admin@example.com",
                         username="admin", role="admin")
            assert admin.is_admin() is True

    def test_user_get_id_for_flask_login(self, app: Flask) -> None:
        """Test get_id method required by Flask-Login."""
        with app.app_context():
            db.create_all()

            user = User(email="test@example.com", username="testuser")
            db.session.add(user)
            db.session.commit()

            # Should return string representation of ID
            user_id = user.get_id()
            assert isinstance(user_id, str)
            assert int(user_id) == user.id

    def test_user_to_dict_serialization(self, app: Flask) -> None:
        """Test user serialization to dictionary."""
        with app.app_context():
            db.create_all()

            user = User(
                email="test@example.com",
                username="testuser",
                full_name="Test User",
                role="user"
            )
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()

            # Should contain expected keys
            expected_keys = {
                "id", "uuid", "email", "username", "full_name",
                "avatar_url", "is_active", "is_verified", "role",
                "created_at", "updated_at"
            }
            assert set(user_dict.keys()).issuperset(expected_keys)

    def test_user_unique_constraints(self, app: Flask) -> None:
        """Test that email and username must be unique."""
        with app.app_context():
            db.create_all()

            # Create first user
            user1 = User(email="test@example.com", username="testuser")
            user1.set_password("password")
            db.session.add(user1)
            db.session.commit()

            # Try to create user with same email
            user2 = User(email="test@example.com", username="differentuser")
            user2.set_password("password")
            db.session.add(user2)

            try:
                db.session.commit()
                assert False, "Should have raised IntegrityError"
            except IntegrityError:
                db.session.rollback()

            # Try to create user with same username
            user3 = User(email="different@example.com", username="testuser")
            user3.set_password("password")
            db.session.add(user3)

            try:
                db.session.commit()
                assert False, "Should have raised IntegrityError"
            except IntegrityError:
                db.session.rollback()

    def test_user_uuid_generation(self, app: Flask) -> None:
        """Test that UUID is automatically generated for users."""
        with app.app_context():
            db.create_all()

            user = User(email="test@example.com", username="testuser")
            db.session.add(user)
            db.session.commit()

            # UUID should be generated automatically
            assert user.uuid is not None
            assert len(user.uuid) == 36  # Standard UUID length

            # Should be a valid UUID
            uuid.UUID(user.uuid)  # Should not raise exception


class TestUserSessionModel:
    """Test suite for UserSession model."""

    def test_user_session_creation(self, app: Flask, test_user: User) -> None:
        """Test creating a user session."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            session = UserSession(
                session_id="test_session_123",
                user_id=test_user.id,
                ip_address="127.0.0.1",
                user_agent="Test Browser",
                expires_at=datetime.now(timezone.utc)
            )

            db.session.add(session)
            db.session.commit()

            assert session.id is not None
            assert session.session_id == "test_session_123"
            assert session.user_id == test_user.id
            assert session.ip_address == "127.0.0.1"

    def test_user_session_expiration(self, app: Flask, test_user: User) -> None:
        """Test session expiration functionality."""
        with app.app_context():
            db.create_all()
            db.session.add(test_user)
            db.session.commit()

            # Create expired session
            expired_time = datetime.now(
                timezone.utc).replace(year=2020)  # Past date
            session = UserSession(
                session_id="expired_session",
                user_id=test_user.id,
                expires_at=expired_time
            )

            assert session.is_expired() is True

            # Create future session
            future_time = datetime.now(timezone.utc).replace(
                year=2030)  # Future date
            session.expires_at = future_time

            assert session.is_expired() is False

    def test_user_session_relationship(self, app: Flask, test_user: User) -> None:
        """Test relationship between user and session."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            session = UserSession(
                session_id="test_session",
                user_id=test_user.id,
                expires_at=datetime.now(timezone.utc)
            )

            db.session.add(session)
            db.session.commit()

            # Test relationship
            assert session.user.id == test_user.id
            assert session.user.email == test_user.email


class TestUserProfileModel:
    """Test suite for UserProfile model."""

    def test_user_profile_creation(self, app: Flask, test_user: User) -> None:
        """Test creating a user profile."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            profile = UserProfile(
                user_id=test_user.id,
                bio="Test bio",
                location="Test City",
                website="https://example.com",
                company="Test Company",
                job_title="Test Developer"
            )

            db.session.add(profile)
            db.session.commit()

            assert profile.id is not None
            assert profile.bio == "Test bio"
            assert profile.location == "Test City"
            assert profile.website == "https://example.com"

    def test_user_profile_relationship(self, app: Flask, test_user: User) -> None:
        """Test relationship between user and profile."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            profile = UserProfile(user_id=test_user.id, bio="Test bio")
            db.session.add(profile)
            db.session.commit()

            # Test relationship
            assert profile.user.id == test_user.id
            assert test_user.profile.id == profile.id

    def test_user_profile_defaults(self, app: Flask, test_user: User) -> None:
        """Test default values for profile fields."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            profile = UserProfile(user_id=test_user.id)
            db.session.add(profile)
            db.session.commit()

            # Check defaults
            assert profile.timezone == "UTC"
            assert profile.language == "en"
            assert profile.theme == "auto"


class TestActivityLogModel:
    """Test suite for ActivityLog model."""

    def test_activity_log_creation(self, app: Flask, test_user: User) -> None:
        """Test creating an activity log entry."""
        with app.app_context():
            db.create_all()

            db.session.add(test_user)
            db.session.commit()

            log = ActivityLog(
                user_id=test_user.id,
                action="test_action",
                resource_type="test_resource",
                resource_id="123",
                ip_address="127.0.0.1",
                metadata_json={"key": "value"}
            )

            db.session.add(log)
            db.session.commit()

            assert log.id is not None
            assert log.action == "test_action"
            assert log.resource_type == "test_resource"
            assert log.user_id == test_user.id

    def test_activity_log_without_user(self, app: Flask) -> None:
        """Test creating activity log without user (anonymous actions)."""
        with app.app_context():
            db.create_all()

            log = ActivityLog(
                action="anonymous_action",
                resource_type="public_resource",
                ip_address="192.168.1.1"
            )

            db.session.add(log)
            db.session.commit()

            assert log.id is not None
            assert log.user_id is None
            assert log.action == "anonymous_action"


class TestSystemSettingModel:
    """Test suite for SystemSetting model."""

    def test_system_setting_creation(self, app: Flask) -> None:
        """Test creating system settings."""
        with app.app_context():
            db.create_all()

            setting = SystemSetting(
                key_name="test_setting",
                value_text="test_value",
                value_type="string",
                description="Test setting description"
            )

            db.session.add(setting)
            db.session.commit()

            assert setting.id is not None
            assert setting.key_name == "test_setting"
            assert setting.value_text == "test_value"

    def test_system_setting_value_handling(self, app: Flask) -> None:
        """Test setting and getting values with type conversion."""
        with app.app_context():
            db.create_all()

            # String setting
            string_setting = SystemSetting(key_name="string_setting")
            string_setting.set_value("test_string")
            db.session.add(string_setting)

            # Integer setting
            int_setting = SystemSetting(key_name="int_setting")
            int_setting.set_value(42)
            db.session.add(int_setting)

            # Boolean setting
            bool_setting = SystemSetting(key_name="bool_setting")
            bool_setting.set_value(True)
            db.session.add(bool_setting)

            db.session.commit()

            # Test retrieval
            assert string_setting.get_value() == "test_string"
            assert int_setting.get_value() == 42
            assert bool_setting.get_value() is True

    def test_system_setting_unique_key(self, app: Flask) -> None:
        """Test that setting keys must be unique."""
        with app.app_context():
            db.create_all()

            setting1 = SystemSetting(
                key_name="duplicate_key", value_text="value1")
            db.session.add(setting1)
            db.session.commit()

            setting2 = SystemSetting(
                key_name="duplicate_key", value_text="value2")
            db.session.add(setting2)

            try:
                db.session.commit()
                assert False, "Should have raised IntegrityError"
            except IntegrityError:
                db.session.rollback()


class TestDatabaseIntegration:
    """Test suite for database integration and relationships."""

    def test_user_with_complete_profile(self, app: Flask) -> None:
        """Test creating user with complete related data."""
        with app.app_context():
            db.create_all()

            # Create user
            user = User(email="test@example.com", username="testuser")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # Create profile
            profile = UserProfile(
                user_id=user.id,
                bio="Test developer",
                location="Test City"
            )
            db.session.add(profile)

            # Create session
            session = UserSession(
                session_id="test_session",
                user_id=user.id,
                expires_at=datetime.now(timezone.utc)
            )
            db.session.add(session)

            # Create activity log
            log = ActivityLog(
                user_id=user.id,
                action="profile_created"
            )
            db.session.add(log)

            db.session.commit()

            # Test all relationships
            assert user.profile.bio == "Test developer"
            assert len(list(user.sessions)) == 1
            assert len(list(user.activity_logs)) == 1
            assert user.sessions.first().session_id == "test_session"
            assert user.activity_logs.first().action == "profile_created"

    def test_cascade_deletion(self, app: Flask) -> None:
        """Test that related records are properly deleted."""
        with app.app_context():
            db.create_all()

            # Create user with related data
            user = User(email="test@example.com", username="testuser")
            db.session.add(user)
            db.session.commit()

            profile = UserProfile(user_id=user.id, bio="Test")
            session = UserSession(
                session_id="test_session",
                user_id=user.id,
                expires_at=datetime.now(timezone.utc)
            )
            log = ActivityLog(user_id=user.id, action="test_action")

            db.session.add_all([profile, session, log])
            db.session.commit()

            user_id = user.id

            # Delete user - should cascade to related records
            db.session.delete(user)
            db.session.commit()

            # Verify cascaded deletion
            assert UserProfile.query.filter_by(user_id=user_id).first() is None
            assert UserSession.query.filter_by(user_id=user_id).first() is None
            assert ActivityLog.query.filter_by(user_id=user_id).first() is None
