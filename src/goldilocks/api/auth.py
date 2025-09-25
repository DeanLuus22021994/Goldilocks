"""Authentication API blueprint for user registration, login, and profile
management."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required  # type: ignore[misc]
from flask_login import login_user  # type: ignore[misc]
from flask_login import (  # type: ignore[import-untyped]
    current_user,
    logout_user,
)
from werkzeug.wrappers import Response

from goldilocks.models.forms import LoginForm, ProfileForm, RegisterForm
from goldilocks.services.auth import AuthenticationService

# Create authentication Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """User login page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():  # type: ignore[misc]
        email = form.email.data
        password = form.password.data

        if not email or not password:
            flash("Email and password are required", "error")
            return render_template("auth/login.html", form=form)

        user, error = AuthenticationService.authenticate_user(email, password)

        if user:
            login_user(user, remember=form.remember_me.data)
            AuthenticationService.log_activity("login", user.id)
            flash("Successfully logged in!", "success")

            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("auth.dashboard"))
        else:
            flash(error or "Invalid email or password", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    """User registration page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():  # type: ignore[misc]
        email = form.email.data
        username = form.username.data
        password = form.password.data
        full_name = form.full_name.data

        if not all([email, username, password, full_name]):
            flash("All fields are required", "error")
            return render_template("auth/register.html", form=form)

        user, error = AuthenticationService.create_user(
            email=email,  # type: ignore[arg-type]
            username=username,  # type: ignore[arg-type]
            password=password,  # type: ignore[arg-type]
            full_name=full_name,
        )

        if user:
            login_user(user)
            AuthenticationService.log_activity("register", user.id)
            flash(
                "Account created successfully! Welcome to Goldilocks!",
                "success",
            )
            return redirect(url_for("auth.dashboard"))
        else:
            flash(error or "Registration failed", "error")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
@login_required  # type: ignore[misc]
def logout() -> Response:
    """User logout handler."""
    user_id = current_user.id
    logout_user()
    AuthenticationService.log_activity("logout", user_id)
    flash("You have been logged out successfully", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/dashboard")
@login_required  # type: ignore[misc]
def dashboard() -> str:
    """User dashboard page."""
    return render_template("auth/dashboard.html")


@auth_bp.route("/profile")
@login_required  # type: ignore[misc]
def profile() -> str | Response:
    """User profile page and update handler."""
    form = ProfileForm()

    if form.validate_on_submit():  # type: ignore[misc]
        success, error = AuthenticationService.update_user_profile(
            user_id=current_user.id,
            full_name=form.full_name.data,
            bio=form.bio.data,
        )

        if success:
            flash("Profile updated successfully!", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash(error or "Profile update failed", "error")

    # Pre-populate form with current user data
    if not form.is_submitted():
        form.full_name.data = current_user.full_name
        if hasattr(current_user, "profile") and current_user.profile:
            form.bio.data = current_user.profile.bio

    return render_template("auth/profile.html", form=form)
