"""WTForms for user authentication and registration."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, Regexp


class LoginForm(FlaskForm):  # type: ignore[misc]
    """User login form."""

    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
        ],
        render_kw={"placeholder": "Enter your email address",
                   "autocomplete": "email"},
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Password is required")],
        render_kw={"placeholder": "Enter your password",
                   "autocomplete": "current-password"},
    )

    remember_me = BooleanField("Remember me")


class RegisterForm(FlaskForm):  # type: ignore[misc]
    """User registration form."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=64,
                   message="Username must be between 3 and 64 characters"),
            Regexp(
                r"^[a-zA-Z0-9_-]+$",
                message="Username can only contain letters, numbers, underscores, and hyphens",
            ),
        ],
        render_kw={"placeholder": "Choose a username",
                   "autocomplete": "username"},
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
        ],
        render_kw={"placeholder": "Enter your email address",
                   "autocomplete": "email"},
    )

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full name is required"),
            Length(min=2, max=255,
                   message="Full name must be between 2 and 255 characters"),
        ],
        render_kw={"placeholder": "Enter your full name",
                   "autocomplete": "name"},
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters"),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)",
                message="Password must contain at least one lowercase letter, one uppercase letter, and one number",
            ),
        ],
        render_kw={"placeholder": "Create a strong password",
                   "autocomplete": "new-password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm your password",
                   "autocomplete": "new-password"},
    )

    terms_accepted = BooleanField(
        "I accept the Terms of Service and Privacy Policy",
        validators=[DataRequired(
            message="You must accept the terms to register")],
    )


class ProfileForm(FlaskForm):  # type: ignore[misc]
    """User profile update form."""

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full name is required"),
            Length(min=2, max=255,
                   message="Full name must be between 2 and 255 characters"),
        ],
        render_kw={"placeholder": "Enter your full name",
                   "autocomplete": "name"},
    )

    bio = TextAreaField(
        "Bio",
        validators=[Optional(), Length(
            max=1000, message="Bio must be less than 1000 characters")],
        render_kw={"placeholder": "Tell us about yourself", "rows": 4},
    )

    location = StringField(
        "Location",
        validators=[Optional(), Length(
            max=255, message="Location must be less than 255 characters")],
        render_kw={"placeholder": "City, Country",
                   "autocomplete": "address-level1"},
    )

    website = StringField(
        "Website",
        validators=[Optional(), Length(
            max=500, message="Website URL must be less than 500 characters")],
        render_kw={"placeholder": "https://example.com", "type": "url"},
    )

    company = StringField(
        "Company",
        validators=[Optional(), Length(
            max=255, message="Company name must be less than 255 characters")],
        render_kw={"placeholder": "Company name",
                   "autocomplete": "organization"},
    )

    job_title = StringField(
        "Job Title",
        validators=[Optional(), Length(
            max=255, message="Job title must be less than 255 characters")],
        render_kw={"placeholder": "Job title",
                   "autocomplete": "organization-title"},
    )


class ChangePasswordForm(FlaskForm):  # type: ignore[misc]
    """Change password form."""

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired(message="Current password is required")],
        render_kw={"placeholder": "Enter your current password",
                   "autocomplete": "current-password"},
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="New password is required"),
            Length(min=8, message="Password must be at least 8 characters"),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)",
                message="Password must contain at least one lowercase letter, one uppercase letter, and one number",
            ),
        ],
        render_kw={"placeholder": "Create a strong password",
                   "autocomplete": "new-password"},
    )

    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(message="Please confirm your new password"),
            EqualTo("new_password", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm your new password",
                   "autocomplete": "new-password"},
    )


class ForgotPasswordForm(FlaskForm):  # type: ignore[misc]
    """Forgot password form."""

    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
        ],
        render_kw={"placeholder": "Enter your email address",
                   "autocomplete": "email"},
    )


class ResetPasswordForm(FlaskForm):  # type: ignore[misc]
    """Reset password form."""

    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters"),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)",
                message="Password must contain at least one lowercase letter, one uppercase letter, and one number",
            ),
        ],
        render_kw={"placeholder": "Create a strong password",
                   "autocomplete": "new-password"},
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Confirm your password",
                   "autocomplete": "new-password"},
    )
