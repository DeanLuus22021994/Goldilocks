"""
Tests for data collectors module.

Following SRP, these tests focus only on data collection
without cross-cutting concerns.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from docs.collectors import ProjectDataCollector, SystemDataCollector
from docs.models import ProjectMetrics, SystemInfo


class TestProjectDataCollector:
    """Test project data collector following SRP."""

    def test_collect_metrics_with_sample_data(self) -> None:
        """Test metrics collection with sample project structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create sample project structure
            (project_root / "src").mkdir()
            (project_root / "src" / "main.py").write_text('print("hello")\n')
            (project_root / "test_example.py").write_text("def test(): pass\n")
            (project_root / "Dockerfile").touch()
            (project_root / ".github" / "workflows").mkdir(parents=True)
            (project_root / ".github" / "workflows" / "ci.yml").touch()

            collector = ProjectDataCollector(project_root)
            metrics = collector.collect_metrics()

            assert isinstance(metrics, ProjectMetrics)
            assert metrics.files_count >= 4  # At least the files we created
            assert metrics.lines_of_code >= 2  # Lines from Python files
            assert metrics.test_files >= 1  # test_example.py
            assert metrics.docker_files >= 1  # Dockerfile
            assert metrics.github_workflows >= 1  # ci.yml

    def test_collect_metrics_empty_directory(self) -> None:
        """Test metrics collection with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            collector = ProjectDataCollector(project_root)
            metrics = collector.collect_metrics()

            assert isinstance(metrics, ProjectMetrics)
            assert metrics.files_count == 0
            assert metrics.lines_of_code == 0
            assert metrics.test_files == 0
            assert metrics.docker_files == 0
            assert metrics.github_workflows == 0

    def test_collect_metrics_handles_unicode_errors(self) -> None:
        """Test that collector handles unicode decode errors gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create a binary file with .py extension
            binary_file = project_root / "binary.py"
            binary_file.write_bytes(b"\x80\x81\x82")

            collector = ProjectDataCollector(project_root)
            metrics = collector.collect_metrics()

            # Should not crash and should count the file but not its lines
            assert metrics.files_count >= 1
            assert metrics.lines_of_code == 0


class TestSystemDataCollector:
    """Test system data collector following SRP."""

    @patch("subprocess.run")
    def test_collect_system_info_success(self, mock_run: MagicMock) -> None:
        """Test successful system info collection."""
        # Mock subprocess calls
        mock_run.side_effect = [
            MagicMock(
                stdout="Python 3.12.0", returncode=0
            ),  # python --version
            MagicMock(
                stdout="Docker version 20.10.0", returncode=0
            ),  # docker --version
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create mock requirements.txt
            requirements_file = project_root / "requirements.txt"
            requirements_file.write_text("Flask==2.3.0\npytest==7.0.0\n")

            collector = SystemDataCollector(project_root)
            system_info = collector.collect_system_info()

            assert isinstance(system_info, SystemInfo)
            assert system_info.python_version == "Python 3.12.0"
            assert system_info.flask_version == "Flask==2.3.0"
            assert system_info.docker_version == "Docker version 20.10.0"
            assert system_info.timestamp is not None

    @patch("subprocess.run")
    def test_collect_system_info_command_failures(
        self, mock_run: MagicMock
    ) -> None:
        """Test system info collection with command failures."""
        # Mock failed subprocess calls
        mock_run.side_effect = FileNotFoundError()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            collector = SystemDataCollector(project_root)
            system_info = collector.collect_system_info()

            assert isinstance(system_info, SystemInfo)
            assert system_info.python_version == "Python (version unknown)"
            assert system_info.flask_version == "Flask (version unknown)"
            assert system_info.docker_version == "Docker not available"

    def test_collect_system_info_no_requirements(self) -> None:
        """Test system info collection without requirements.txt."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            collector = SystemDataCollector(project_root)

            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = [
                    MagicMock(stdout="Python 3.12.0", returncode=0),
                    MagicMock(stdout="Docker version 20.10.0", returncode=0),
                ]

                system_info = collector.collect_system_info()

                assert system_info.flask_version == "Flask (version unknown)"
