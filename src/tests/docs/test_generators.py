"""
Tests for content generators module.

Following SRP, these tests focus only on content generation
without cross-cutting concerns.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from docs.generators import (
    StructureContentGenerator,
    TechnicalContentGenerator,
)
from docs.models import GenerationContext, ProjectMetrics, SystemInfo


class TestStructureContentGenerator:
    """Test structure content generator following SRP."""

    def test_generate_content_includes_all_sections(self) -> None:
        """Test that structure content includes required sections."""
        generator = StructureContentGenerator()

        # Create mock context
        with tempfile.TemporaryDirectory() as temp_dir:
            context = GenerationContext(
                project_root=Path(temp_dir),
                output_dir=Path(temp_dir) / "docs",
                metrics=ProjectMetrics(
                    files_count=100,
                    lines_of_code=5000,
                    test_files=20,
                    docker_files=3,
                    github_workflows=2,
                ),
                system_info=SystemInfo(
                    python_version="Python 3.12.0",
                    flask_version="Flask==2.3.0",
                    docker_version="Docker 20.10.0",
                    timestamp="2023-01-01T12:00:00",
                ),
            )

            content = generator.generate_content(context)

            # Verify required sections are present
            assert "# Project Structure" in content
            assert "## Project Metrics" in content
            assert "## Directory Structure" in content
            assert "## Architecture Principles" in content
            assert "Total Files**: 100" in content
            assert "Lines of Code**: 5,000" in content

    @patch("subprocess.run")
    def test_generate_tree_uses_tree_command(self, mock_run: MagicMock) -> None:
        """Test that tree generation prefers external tree command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="project/\n├── file1.py\n└── file2.py\n")

        generator = StructureContentGenerator()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = generator.generate_tree_structure(Path(temp_dir))

            assert "project/" in result
            assert "├── file1.py" in result
            mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_generate_tree_fallback_to_python(self, mock_run: MagicMock) -> None:
        """Test fallback to Python tree implementation."""
        mock_run.side_effect = FileNotFoundError()

        generator = StructureContentGenerator()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "test.py").write_text("# test file")

            result = generator.generate_tree_structure(project_root)

            # Should include the root directory name
            assert project_root.name in result
            assert "test.py" in result

    def test_python_tree_ignores_common_dirs(self) -> None:
        """Test that Python tree implementation ignores common directories."""
        generator = StructureContentGenerator()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create directories that should be ignored
            (project_root / ".git").mkdir()
            (project_root / "__pycache__").mkdir()
            (project_root / "node_modules").mkdir()

            # Create files that should be included
            (project_root / "main.py").write_text("# main")
            (project_root / "src").mkdir()
            (project_root / "src" / "app.py").write_text("# app")

            result = generator.generate_python_tree_structure(project_root)

            assert "main.py" in result
            assert "src" in result
            assert "app.py" in result
            assert ".git" not in result
            assert "__pycache__" not in result
            assert "node_modules" not in result


class TestTechnicalContentGenerator:
    """Test technical content generator following SRP."""

    def test_generate_content_includes_system_info(self) -> None:
        """Test that technical content includes system information."""
        generator = TechnicalContentGenerator()

        with tempfile.TemporaryDirectory() as temp_dir:
            context = GenerationContext(
                project_root=Path(temp_dir),
                output_dir=Path(temp_dir) / "docs",
                metrics=ProjectMetrics(
                    files_count=100,
                    lines_of_code=5000,
                    test_files=20,
                    docker_files=3,
                    github_workflows=2,
                ),
                system_info=SystemInfo(
                    python_version="Python 3.12.0",
                    flask_version="Flask==2.3.0",
                    docker_version="Docker 20.10.0",
                    timestamp="2023-01-01T12:00:00.123456",
                ),
            )

            content = generator.generate_content(context)

            # Verify required sections are present
            assert "# Technical Documentation" in content
            assert "## System Information" in content
            assert "## Performance Metrics" in content
            assert "Python 3.12.0" in content
            assert "Flask==2.3.0" in content
            assert "Docker 20.10.0" in content
            assert "2023-01-01T12:00:00.123456" in content

    def test_generate_content_formats_metrics_correctly(self) -> None:
        """Test that metrics are formatted with proper separators."""
        generator = TechnicalContentGenerator()

        with tempfile.TemporaryDirectory() as temp_dir:
            context = GenerationContext(
                project_root=Path(temp_dir),
                output_dir=Path(temp_dir) / "docs",
                metrics=ProjectMetrics(
                    files_count=1000,
                    lines_of_code=50000,
                    test_files=200,
                    docker_files=5,
                    github_workflows=3,
                ),
                system_info=SystemInfo(
                    python_version="Python 3.12.0",
                    flask_version="Flask==2.3.0",
                    docker_version="Docker 20.10.0",
                    timestamp="2023-01-01T12:00:00",
                ),
            )

            content = generator.generate_content(context)

            # Verify number formatting with commas
            assert "Total Lines of Code**: 50,000" in content
