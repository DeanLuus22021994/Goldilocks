"""Authentication API blueprint for user registration, login, and profile management."""

from flask import Blueprint, flash, redirect, render_template_string, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from goldilocks.models.forms import LoginForm, ProfileForm, RegisterForm
from goldilocks.services.auth import AuthenticationService

# Create authentication Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# HTML Templates as strings (to be moved to proper templates later)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Login - Goldilocks</title>
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
</head>
<body>
<div class="container">
    <h1>Login to Goldilocks</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.email.label }}
            {{ form.email() }}
            {% if form.email.errors %}
                <div class="form-error">{{ form.email.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.password.label }}
            {{ form.password() }}
            {% if form.password.errors %}
                <div class="form-error">{{ form.password.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.remember_me() }} {{ form.remember_me.label }}
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <p><a href="{{ url_for('auth.register') }}">Don't have an account? Register here</a></p>
</div>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Register - Goldilocks</title>
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
</head>
<body>
<div class="container">
    <h1>Create Account</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.full_name.label }}
            {{ form.full_name() }}
            {% if form.full_name.errors %}
                <div class="form-error">{{ form.full_name.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.username.label }}
            {{ form.username() }}
            {% if form.username.errors %}
                <div class="form-error">{{ form.username.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.email.label }}
            {{ form.email() }}
            {% if form.email.errors %}
                <div class="form-error">{{ form.email.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.password.label }}
            {{ form.password() }}
            {% if form.password.errors %}
                <div class="form-error">{{ form.password.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.confirm_password.label }}
            {{ form.confirm_password() }}
            {% if form.confirm_password.errors %}
                <div class="form-error">{{ form.confirm_password.errors[0] }}</div>
            {% endif %}
        </div>
        <div class="form-group">
            {{ form.terms_accepted() }} {{ form.terms_accepted.label }}
            {% if form.terms_accepted.errors %}
                <div class="form-error">{{ form.terms_accepted.errors[0] }}</div>
            {% endif %}
        </div>
        <button type="submit" class="btn btn-primary">Create Account</button>
    </form>
    <p><a href="{{ url_for('auth.login') }}">Already have an account? Login here</a></p>
</div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Dashboard - Goldilocks</title>
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
</head>
<body>
<div class="container">
    <h1>Welcome back, {{ current_user.full_name or current_user.username }}!</h1>
    <p>You are successfully logged in to Goldilocks.</p>
    <div class="actions">
        <a href="{{ url_for('auth.profile') }}" class="btn btn-secondary">View Profile</a>
        <a href="{{ url_for('auth.logout') }}" class="btn btn-secondary">Logout</a>
        <a href="/" class="btn btn-primary">Back to Home</a>
    </div>
</div>
</body>
</html>
"""


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if not email or not password:
            flash("Email and password are required", "error")
            return render_template_string(LOGIN_TEMPLATE, form=form)

        user, error = AuthenticationService.authenticate_user(email, password)

        if user:
            login_user(user, remember=form.remember_me.data)
            AuthenticationService.log_activity("login", user.id)
            flash("Successfully logged in!", "success")

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("auth.dashboard"))
        else:
            flash(error or "Invalid email or password", "error")

    return render_template_string(LOGIN_TEMPLATE, form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page and handler."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        full_name = form.full_name.data

        if not all([email, username, password, full_name]):
            flash("All fields are required", "error")
            return render_template_string(REGISTER_TEMPLATE, form=form)

        user, error = AuthenticationService.create_user(
            email=email,  # type: ignore[arg-type]
            username=username,  # type: ignore[arg-type]
            password=password,  # type: ignore[arg-type]
            full_name=full_name,  # type: ignore[arg-type]
        )

        if user:
            login_user(user)
            AuthenticationService.log_activity("register", user.id)
            flash("Account created successfully! Welcome to Goldilocks!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash(error or "Registration failed", "error")

    return render_template_string(REGISTER_TEMPLATE, form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout handler."""
    user_id = current_user.id
    logout_user()
    AuthenticationService.log_activity("logout", user_id)
    flash("You have been logged out successfully", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    """User dashboard page."""
    return render_template_string(DASHBOARD_TEMPLATE)


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile page and update handler."""
    form = ProfileForm()

    if form.validate_on_submit():
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
        if hasattr(current_user, 'profile') and current_user.profile:
            form.bio.data = current_user.profile.bio

    profile_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Profile - Goldilocks</title>
        <link rel="stylesheet" href="/static/css/variables.css">
        <link rel="stylesheet" href="/static/css/base.css">
        <link rel="stylesheet" href="/static/css/components.css">
        <link rel="stylesheet" href="/static/css/buttons.css">
    </head>
    <body>
    <div class="container">
        <h1>Your Profile</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.full_name.label }}
                {{ form.full_name() }}
                {% if form.full_name.errors %}
                    <div class="form-error">{{ form.full_name.errors[0] }}</div>
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.bio.label }}
                {{ form.bio() }}
                {% if form.bio.errors %}
                    <div class="form-error">{{ form.bio.errors[0] }}</div>
                {% endif %}
            </div>
            <button type="submit" class="btn btn-primary">Update Profile</button>
        </form>
        <div class="actions">
            <a href="{{ url_for('auth.dashboard') }}" class="btn btn-secondary">Back to Dashboard</a>
        </div>
    </div>
    </body>
    </html>
    """

    return render_template_string(profile_template, form=form)
