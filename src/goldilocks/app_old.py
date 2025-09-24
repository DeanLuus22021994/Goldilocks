"""Goldilocks Flask application entry point.

This module provides the main Flask application instance using the
application factory pattern for proper structure and testability.
"""

import os

from goldilocks.core.app_factory import create_app

# Create Flask application using factory pattern
config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

# For compatibility with existing deployment scripts
__all__ = ["app"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

from __future__ import annotations

import importlib
import logging
import os
import sys
import time
import uuid
import warnings
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as pkg_version
from logging import StreamHandler, getLogger

import flask as flask_module
from flask import Flask, Response, flash, g, jsonify, redirect, render_template_string, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

# Import at module level to satisfy linters and provide a safe fallback
try:
    from goldilocks import __version__ as _FALLBACK_APP_VERSION
except ImportError:  # pragma: no cover
    _FALLBACK_APP_VERSION = "0.1.0"  # pragma: no cover

# Import database models
from goldilocks.models.database import User, db
from goldilocks.models.forms import LoginForm, ProfileForm, RegisterForm
from goldilocks.services.auth import AuthenticationService

# Get the path to the frontend static directory
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
STATIC_FOLDER = os.path.join(BASE_DIR, "frontend", "static")

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path="/static")

# Configuration
app.config.update(
    SECRET_KEY=os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"),
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "DATABASE_URL", "mysql+pymysql://goldilocks_user:goldilocks_pass_2024@localhost:3306/goldilocks"
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ENGINE_OPTIONS={
        "pool_size": 10,
        "pool_timeout": 30,
        "pool_recycle": 3600,
        "max_overflow": 20,
        "pool_pre_ping": True,
    },
    WTF_CSRF_ENABLED=True,
    WTF_CSRF_TIME_LIMIT=3600,
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=86400,  # 24 hours
)

# Initialize extensions
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page"
login_manager.login_message_category = "info"

# Initialize database after app configuration
db.init_app(app)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """Load user for Flask-Login."""
    try:
        return db.session.query(User).filter_by(id=int(user_id)).first()
    except (ValueError, TypeError):
        return None


class CorrelationIdFilter(logging.Filter):
    """Ensure every log record contains a correlation_id field."""

    def filter(self, record: logging.LogRecord) -> bool:
        # pragma: no cover - thin shim
        try:
            record.correlation_id = getattr(g, "correlation_id", "-")
        except RuntimeError:  # outside request context
            record.correlation_id = "-"
        return True


# Logging: prefer JSON logs if python-json-logger is available
logger = getLogger("goldilocks")
handler = StreamHandler()
handler.addFilter(CorrelationIdFilter())

# Use a single constant for the log format and keep lines under 79 chars
LOG_FORMAT = " ".join(
    (
        "%(asctime)s",
        "%(levelname)s",
        "%(name)s",
        "%(correlation_id)s",
        "%(message)s",
    )
)
formatter: logging.Formatter = logging.Formatter(LOG_FORMAT)
try:
    jsonlogger_mod = importlib.import_module("pythonjsonlogger.jsonlogger")
    JsonFormatter = jsonlogger_mod.JsonFormatter
    formatter = JsonFormatter(LOG_FORMAT)
except (ImportError, AttributeError):  # pragma: no cover
    pass

handler.setFormatter(formatter)
# Avoid duplicate handlers on reload
if not any(isinstance(h, StreamHandler) for h in logger.handlers):
    logger.addHandler(handler)
logger.setLevel(logging.INFO)
# Do not propagate to root to avoid double-logging when root has handlers
logger.propagate = False

# Propagate Flask's logs to the root logger and ensure it has our handler
app.logger.handlers = []
app.logger.propagate = True
root_logger = logging.getLogger()
if not any(isinstance(h, StreamHandler) for h in root_logger.handlers):
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


@app.before_request
def add_correlation_id_and_timing() -> None:
    """Attach a correlation ID and start time to the request context."""
    cid = request.headers.get("X-Request-ID") or uuid.uuid4().hex
    g.correlation_id = cid
    g.start_time = time.perf_counter()


@app.after_request
def add_response_headers(resp: Response) -> Response:
    """Add correlation ID and timing headers to response."""
    # Correlation ID and simple timing
    cid = getattr(g, "correlation_id", None)
    if cid:
        resp.headers["X-Request-ID"] = cid
    start = getattr(g, "start_time", None)
    if start is not None:
        dur_ms = (time.perf_counter() - start) * 1000.0
        resp.headers["X-Response-Time-ms"] = f"{dur_ms:.2f}"
        logger.info(
            "request",
            extra={
                "path": request.path,
                "method": request.method,
                "status": resp.status_code,
                "duration_ms": round(dur_ms, 2),
            },
        )
    return resp


@app.get("/")
def index() -> Response:
    """Serve the static index page."""
    return app.send_static_file("index.html")


@app.get("/health")
def health() -> tuple[Response, int]:
    """Return health status of the application."""
    return jsonify({"status": "ok"}), 200


@app.get("/version")
def version() -> tuple[Response, int]:
    """Return versions for the app, Python, Flask, and platform."""
    # app version can be provided via env APP_VERSION, else package metadata,
    # else fallback
    app_version = os.environ.get("APP_VERSION")
    if not app_version:
        try:
            # Prefer package metadata for our distribution name if installed
            app_version = pkg_version("goldilocks")
        except PackageNotFoundError:
            # Fallback to package variable defined in __init__
            app_version = _FALLBACK_APP_VERSION

    try:
        flask_version = pkg_version("Flask")
    except PackageNotFoundError:  # pragma: no cover
        # Fallback for unusual environments
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            flask_version = getattr(flask_module, "__version__", "unknown")

    data = {
        "app": app_version,
        "python": sys.version.split()[0],
        "flask": flask_version,
        "platform": sys.platform,
    }
    return jsonify(data), 200


@app.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    """User login page and handler."""
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user, error = AuthenticationService.authenticate_user(
            form.email.data, form.password.data
        )
        if user:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("dashboard"))
        else:
            flash(error or "Login failed", "error")

    return render_template_string(LOGIN_TEMPLATE, form=form)


@app.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    """User registration page and handler."""
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for("dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        user, error = AuthenticationService.create_user(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            full_name=form.full_name.data,
        )
        if user:
            login_user(user)
            flash("Registration successful! Welcome to Goldilocks!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash(error or "Registration failed", "error")

    return render_template_string(REGISTER_TEMPLATE, form=form)


@app.route("/logout")
@login_required
def logout() -> Response:
    """Log out current user."""
    AuthenticationService.log_activity(
        user_id=current_user.id,  # type: ignore
        action="logout",
    )
    logout_user()
    flash("You have been logged out successfully", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard() -> str:
    """User dashboard page."""
    stats = AuthenticationService.get_user_stats()
    return render_template_string(DASHBOARD_TEMPLATE, user=current_user, stats=stats)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile() -> Response | str:
    """User profile page and handler."""
    form = ProfileForm()

    if request.method == "GET":
        # Pre-populate form with current data
        form.full_name.data = current_user.full_name  # type: ignore
        if hasattr(current_user, "profile") and current_user.profile:  # type: ignore
            form.bio.data = current_user.profile.bio  # type: ignore
            form.location.data = current_user.profile.location  # type: ignore
            form.website.data = current_user.profile.website  # type: ignore
            form.company.data = current_user.profile.company  # type: ignore
            form.job_title.data = current_user.profile.job_title  # type: ignore

    if form.validate_on_submit():
        success, error = AuthenticationService.update_user_profile(
            user_id=current_user.id,  # type: ignore
            full_name=form.full_name.data,
            bio=form.bio.data,
            location=form.location.data,
            website=form.website.data,
            company=form.company.data,
            job_title=form.job_title.data,
        )
        if success:
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile"))
        else:
            flash(error or "Failed to update profile", "error")

    return render_template_string(PROFILE_TEMPLATE, form=form, user=current_user)


@app.errorhandler(404)
def not_found(_: Exception) -> tuple[Response, int]:
    """Handle 404 errors with JSON response."""
    return jsonify({"message": "Not Found"}), 404


# HTML Templates (in production, these would be separate files)
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Goldilocks</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/theme.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
    <style>
        .auth-container { max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .auth-form { background: var(--card); border-radius: 8px; padding: 2rem; box-shadow: var(--elev); }
        .form-group { margin-bottom: 1rem; }
        .form-label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 4px; }
        .form-input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1); }
        .form-error { color: var(--error); font-size: 0.875rem; margin-top: 0.25rem; }
        .flash-messages { margin-bottom: 1rem; }
        .flash-message { padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; }
        .flash-success { background: #d1fae5; color: #065f46; }
        .flash-error { background: #fee2e2; color: #991b1b; }
        .flash-info { background: #dbeafe; color: #1e40af; }
        .auth-links { text-align: center; margin-top: 1rem; }
        .auth-links a { color: var(--primary); text-decoration: none; }
        .auth-links a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-form">
            <h1 style="text-align: center; margin-bottom: 2rem;">Login to Goldilocks</h1>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="flash-messages">
                        {% for category, message in messages %}
                            <div class="flash-message flash-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}

            <form method="POST">
                {{ form.hidden_tag() }}

                <div class="form-group">
                    {{ form.email.label(class="form-label") }}
                    {{ form.email(class="form-input") }}
                    {% if form.email.errors %}
                        {% for error in form.email.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.password.label(class="form-label") }}
                    {{ form.password(class="form-input") }}
                    {% if form.password.errors %}
                        {% for error in form.password.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.remember_me() }} {{ form.remember_me.label() }}
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
            </form>

            <div class="auth-links">
                <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
                <p><a href="{{ url_for('index') }}">← Back to Home</a></p>
            </div>
        </div>
    </div>
    <script src="/static/js/main.js" defer></script>
</body>
</html>
"""

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Register - Goldilocks</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/theme.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
    <style>
        .auth-container { max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .auth-form { background: var(--card); border-radius: 8px; padding: 2rem; box-shadow: var(--elev); }
        .form-group { margin-bottom: 1rem; }
        .form-label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 4px; }
        .form-input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1); }
        .form-error { color: var(--error); font-size: 0.875rem; margin-top: 0.25rem; }
        .flash-messages { margin-bottom: 1rem; }
        .flash-message { padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; }
        .flash-success { background: #d1fae5; color: #065f46; }
        .flash-error { background: #fee2e2; color: #991b1b; }
        .flash-info { background: #dbeafe; color: #1e40af; }
        .auth-links { text-align: center; margin-top: 1rem; }
        .auth-links a { color: var(--primary); text-decoration: none; }
        .auth-links a:hover { text-decoration: underline; }
        .checkbox-group { display: flex; align-items: flex-start; gap: 0.5rem; }
        .checkbox-group input { margin-top: 0.25rem; }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="auth-form">
            <h1 style="text-align: center; margin-bottom: 2rem;">Create Account</h1>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="flash-messages">
                        {% for category, message in messages %}
                            <div class="flash-message flash-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}

            <form method="POST">
                {{ form.hidden_tag() }}

                <div class="form-group">
                    {{ form.full_name.label(class="form-label") }}
                    {{ form.full_name(class="form-input") }}
                    {% if form.full_name.errors %}
                        {% for error in form.full_name.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.username.label(class="form-label") }}
                    {{ form.username(class="form-input") }}
                    {% if form.username.errors %}
                        {% for error in form.username.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.email.label(class="form-label") }}
                    {{ form.email(class="form-input") }}
                    {% if form.email.errors %}
                        {% for error in form.email.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.password.label(class="form-label") }}
                    {{ form.password(class="form-input") }}
                    {% if form.password.errors %}
                        {% for error in form.password.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.confirm_password.label(class="form-label") }}
                    {{ form.confirm_password(class="form-input") }}
                    {% if form.confirm_password.errors %}
                        {% for error in form.confirm_password.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    <div class="checkbox-group">
                        {{ form.terms_accepted() }}
                        {{ form.terms_accepted.label() }}
                    </div>
                    {% if form.terms_accepted.errors %}
                        {% for error in form.terms_accepted.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%;">Create Account</button>
            </form>

            <div class="auth-links">
                <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
                <p><a href="{{ url_for('index') }}">← Back to Home</a></p>
            </div>
        </div>
    </div>
    <script src="/static/js/main.js" defer></script>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dashboard - Goldilocks</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/theme.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
    <link rel="stylesheet" href="/static/css/header.css">
    <style>
        .dashboard-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .dashboard-header { margin-bottom: 2rem; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .dashboard-card { background: var(--card); border-radius: 8px; padding: 2rem; box-shadow: var(--elev); }
        .stat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem; }
        .stat-item { text-align: center; padding: 1rem; background: var(--bg); border-radius: 4px; }
        .stat-value { font-size: 2rem; font-weight: bold; color: var(--primary); }
        .stat-label { font-size: 0.875rem; color: var(--muted); margin-top: 0.5rem; }
        .user-info { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
        .user-avatar { width: 64px; height: 64px; border-radius: 50%; background: var(--primary); display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem; font-weight: bold; }
        .user-details h2 { margin: 0; }
        .user-details p { margin: 0.25rem 0; color: var(--muted); }
        .nav-bar { background: var(--card); padding: 1rem 2rem; margin-bottom: 2rem; box-shadow: var(--elev); }
        .nav-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { color: var(--fg); text-decoration: none; font-weight: 500; }
        .nav-links a:hover { color: var(--primary); }
    </style>
</head>
<body>
    <nav class="nav-bar">
        <div class="nav-content">
            <div class="nav-brand">
                <strong>Goldilocks</strong>
            </div>
            <div class="nav-links">
                <a href="{{ url_for('dashboard') }}">Dashboard</a>
                <a href="{{ url_for('profile') }}">Profile</a>
                <a href="{{ url_for('logout') }}">Logout</a>
            </div>
        </div>
    </nav>

    <div class="dashboard-container">
        <div class="dashboard-header">
            <h1>Welcome back, {{ user.full_name or user.username }}!</h1>
            <p>Here's your dashboard overview</p>
        </div>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages" style="margin-bottom: 2rem;">
                    {% for category, message in messages %}
                        <div class="flash-message flash-{{ category }}" style="padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; {% if category == 'success' %}background: #d1fae5; color: #065f46;{% elif category == 'error' %}background: #fee2e2; color: #991b1b;{% else %}background: #dbeafe; color: #1e40af;{% endif %}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <div class="dashboard-grid">
            <div class="dashboard-card">
                <h3>Your Account</h3>
                <div class="user-info">
                    <div class="user-avatar">
                        {{ (user.full_name or user.username)[0].upper() }}
                    </div>
                    <div class="user-details">
                        <h2>{{ user.full_name or user.username }}</h2>
                        <p>{{ user.email }}</p>
                        <p>{{ user.role.title() }} • Joined {{ user.created_at.strftime('%B %Y') if user.created_at else 'Recently' }}</p>
                    </div>
                </div>
                <p><a href="{{ url_for('profile') }}" class="btn btn-secondary">Edit Profile</a></p>
            </div>

            <div class="dashboard-card">
                <h3>System Statistics</h3>
                <div class="stat-grid">
                    <div class="stat-item">
                        <div class="stat-value">{{ stats.total_users }}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ stats.active_users }}</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ stats.recent_logins }}</div>
                        <div class="stat-label">Recent Logins</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ stats.admin_users }}</div>
                        <div class="stat-label">Administrators</div>
                    </div>
                </div>
            </div>

            <div class="dashboard-card">
                <h3>Quick Actions</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <a href="{{ url_for('profile') }}" class="btn btn-primary">Update Profile</a>
                    <a href="{{ url_for('health') }}" class="btn btn-secondary">Check System Health</a>
                    <a href="{{ url_for('version') }}" class="btn btn-secondary">View System Info</a>
                    <a href="{{ url_for('index') }}" class="btn btn-secondary">Back to Home</a>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/js/main.js" defer></script>
</body>
</html>
"""

PROFILE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Profile - Goldilocks</title>
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/theme.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/layout.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <link rel="stylesheet" href="/static/css/buttons.css">
    <style>
        .profile-container { max-width: 600px; margin: 2rem auto; padding: 2rem; }
        .profile-form { background: var(--card); border-radius: 8px; padding: 2rem; box-shadow: var(--elev); }
        .form-group { margin-bottom: 1rem; }
        .form-label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 4px; }
        .form-textarea { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 4px; min-height: 100px; resize: vertical; }
        .form-input:focus, .form-textarea:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1); }
        .form-error { color: var(--error); font-size: 0.875rem; margin-top: 0.25rem; }
        .flash-messages { margin-bottom: 1rem; }
        .flash-message { padding: 0.75rem; border-radius: 4px; margin-bottom: 0.5rem; }
        .flash-success { background: #d1fae5; color: #065f46; }
        .flash-error { background: #fee2e2; color: #991b1b; }
        .flash-info { background: #dbeafe; color: #1e40af; }
        .nav-bar { background: var(--card); padding: 1rem 2rem; margin-bottom: 2rem; box-shadow: var(--elev); }
        .nav-content { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { color: var(--fg); text-decoration: none; font-weight: 500; }
        .nav-links a:hover { color: var(--primary); }
        .form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 2rem; }
    </style>
</head>
<body>
    <nav class="nav-bar">
        <div class="nav-content">
            <div class="nav-brand">
                <strong>Goldilocks</strong>
            </div>
            <div class="nav-links">
                <a href="{{ url_for('dashboard') }}">Dashboard</a>
                <a href="{{ url_for('profile') }}">Profile</a>
                <a href="{{ url_for('logout') }}">Logout</a>
            </div>
        </div>
    </nav>

    <div class="profile-container">
        <div class="profile-form">
            <h1 style="margin-bottom: 2rem;">Edit Profile</h1>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    <div class="flash-messages">
                        {% for category, message in messages %}
                            <div class="flash-message flash-{{ category }}">{{ message }}</div>
                        {% endfor %}
                    </div>
                {% endif %}
            {% endwith %}

            <form method="POST">
                {{ form.hidden_tag() }}

                <div class="form-group">
                    {{ form.full_name.label(class="form-label") }}
                    {{ form.full_name(class="form-input") }}
                    {% if form.full_name.errors %}
                        {% for error in form.full_name.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.bio.label(class="form-label") }}
                    {{ form.bio(class="form-textarea") }}
                    {% if form.bio.errors %}
                        {% for error in form.bio.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.location.label(class="form-label") }}
                    {{ form.location(class="form-input") }}
                    {% if form.location.errors %}
                        {% for error in form.location.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.website.label(class="form-label") }}
                    {{ form.website(class="form-input") }}
                    {% if form.website.errors %}
                        {% for error in form.website.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.company.label(class="form-label") }}
                    {{ form.company(class="form-input") }}
                    {% if form.company.errors %}
                        {% for error in form.company.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-group">
                    {{ form.job_title.label(class="form-label") }}
                    {{ form.job_title(class="form-input") }}
                    {% if form.job_title.errors %}
                        {% for error in form.job_title.errors %}
                            <div class="form-error">{{ error }}</div>
                        {% endfor %}
                    {% endif %}
                </div>

                <div class="form-actions">
                    <a href="{{ url_for('dashboard') }}" class="btn btn-secondary">Cancel</a>
                    <button type="submit" class="btn btn-primary">Update Profile</button>
                </div>
            </form>
        </div>
    </div>

    <script src="/static/js/main.js" defer></script>
</body>
</html>
"""


# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Error creating database tables: {e}")


# Explicit exports for typing and tests
__all__ = ["app", "pkg_version"]
