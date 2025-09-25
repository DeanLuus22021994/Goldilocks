"""
Data models for documentation generation.

Following the separation of concerns principle, this module contains
only data structures and type definitions without any business logic.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class ProjectMetrics:
    """Project metrics data structure."""

    files_count: int
    lines_of_code: int
    test_files: int
    docker_files: int
    github_workflows: int


@dataclass
class SystemInfo:
    """System information data structure."""

    python_version: str
    flask_version: str
    docker_version: str
    timestamp: str


@dataclass
class GenerationContext:
    """Context for documentation generation."""

    project_root: Path
    output_dir: Path
    metrics: ProjectMetrics
    system_info: SystemInfo


class DataCollectorProtocol(Protocol):
    """Protocol for data collectors following dependency inversion."""

    def collect_metrics(self) -> ProjectMetrics:
        """Collect project metrics."""
        ...

    def collect_system_info(self) -> SystemInfo:
        """Collect system information."""
        ...


class ContentGeneratorProtocol(Protocol):
    """Protocol for content generators following dependency inversion."""

    def generate_structure_content(self, context: GenerationContext) -> str:
        """Generate structure document content."""
        ...

    def generate_technical_content(self, context: GenerationContext) -> str:
        """Generate technical document content."""
        ...


class ProcessorProtocol(Protocol):
    """Protocol for content processors following dependency inversion."""

    def enhance_content(self, content: str) -> str:
        """Enhance content using processing capabilities."""
        ...
