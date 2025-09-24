"""Main application routes blueprint."""

from flask import Blueprint, render_template

# Create main Blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index() -> str:
    """Main application index page."""
    return render_template("main/index.html")
