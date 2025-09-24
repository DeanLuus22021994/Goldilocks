"""Test template system migration and functionality."""

from flask import Flask


def test_template_system_works(app: Flask) -> None:
    """Test that the new template system renders correctly."""
    with app.test_client() as client:
        # Test main index template
        response = client.get("/")
        assert response.status_code == 200
        assert b"Goldilocks Flask App" in response.data

        # Test that template inheritance works (should contain base layout elements)
        assert b"<!DOCTYPE html>" in response.data
        assert b"<html" in response.data


def test_auth_login_template(app: Flask) -> None:
    """Test that auth login template renders correctly."""
    with app.test_client() as client:
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"Login to Goldilocks" in response.data
        assert b"form" in response.data.lower()


def test_template_folder_configured(app: Flask) -> None:
    """Test that template folder is correctly configured."""
    # Check that the template folder points to frontend/static/templates
    template_folder = app.template_folder
    assert template_folder is not None
    assert "frontend/static/templates" in template_folder


def test_static_files_accessible(app: Flask) -> None:
    """Test that CSS and JS files are accessible."""
    with app.test_client() as client:
        # Test CSS file access
        response = client.get("/static/css/variables.css")
        assert response.status_code == 200

        # Test JS file access
        response = client.get("/static/js/main.js")
        assert response.status_code == 200
