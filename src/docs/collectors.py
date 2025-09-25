"""
Data collectors for documentation generation.

Following SRP, this module handles only data collection without
cross-cutting concerns like formatting or file I/O.
"""

import subprocess
from datetime import datetime
from pathlib import Path

from .models import ProjectMetrics, SystemInfo


class ProjectDataCollector:
    """Collects project-specific data following SRP."""

    def __init__(self, project_root: Path) -> None:
        """Initialize with project root path."""
        self.project_root = project_root

    def collect_metrics(self) -> ProjectMetrics:
        """Collect project metrics without cross-cutting concerns."""
        files_count = sum(
            1 for _ in self.project_root.rglob("*") if _.is_file()
        )

        # Count lines of code in Python files
        loc = 0
        for file_path in self.project_root.rglob("*.py"):
            try:
                loc += len(file_path.read_text(encoding="utf-8").splitlines())
            except (UnicodeDecodeError, PermissionError):
                continue

        test_files = len(list(self.project_root.rglob("test*.py")))
        docker_files = len(
            list(self.project_root.rglob("*Dockerfile*"))
        ) + len(list(self.project_root.rglob("docker-compose*.yml")))
        github_workflows = len(
            list(self.project_root.rglob(".github/workflows/*.yml"))
        )

        return ProjectMetrics(
            files_count=files_count,
            lines_of_code=loc,
            test_files=test_files,
            docker_files=docker_files,
            github_workflows=github_workflows,
        )


class SystemDataCollector:
    """Collects system information following SRP."""

    def __init__(self, project_root: Path) -> None:
        """Initialize with project root path for requirements lookup."""
        self.project_root = project_root

    def collect_system_info(self) -> SystemInfo:
        """Collect system information without cross-cutting concerns."""
        python_version = self._get_python_version()
        flask_version = self._get_flask_version()
        docker_version = self._get_docker_version()
        timestamp = datetime.now().isoformat()

        return SystemInfo(
            python_version=python_version,
            flask_version=flask_version,
            docker_version=docker_version,
            timestamp=timestamp,
        )

    def _get_python_version(self) -> str:
        """Get Python version string."""
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.stdout.strip()
        except FileNotFoundError:
            return "Python (version unknown)"

    def _get_flask_version(self) -> str:
        """Get Flask version from requirements.txt."""
        try:
            requirements_path = self.project_root / "requirements.txt"
            if requirements_path.exists():
                content = requirements_path.read_text(encoding="utf-8")
                for line in content.splitlines():
                    if line.strip().lower().startswith("flask"):
                        return line.strip()
        except Exception:
            pass
        return "Flask (version unknown)"

    def _get_docker_version(self) -> str:
        """Get Docker version string."""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        return "Docker not available"
