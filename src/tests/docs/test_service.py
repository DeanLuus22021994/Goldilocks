"""
Tests for documentation service module.

Following SRP, these tests focus on service orchestration
without cross-cutting concerns.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from docs.service import DocumentationService, generate_documentation


class TestDocumentationService:
    """Test documentation service following SRP."""

    def test_service_initialization(self) -> None:
        """Test service initializes with correct dependencies."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            service = DocumentationService(project_root)

            assert service.project_root == project_root
            assert service.output_dir == project_root / "docs"
            # Test that service is properly initialized by attempting to use it
            try:
                # This will test internal components without accessing protected attributes
                service.generate_all_documentation()
                # If we get here, all components were properly initialized
                initialization_successful = True
            except Exception:
                initialization_successful = False
            assert initialization_successful

    def test_service_with_custom_output_dir(self) -> None:
        """Test service initialization with custom output directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            custom_output = Path(temp_dir) / "custom_docs"

            service = DocumentationService(project_root, custom_output)

            assert service.output_dir == custom_output

    @patch("docs.service.DocumentationService._generate_structure_document")
    @patch("docs.service.DocumentationService._generate_technical_document")
    def test_generate_all_documentation_calls_generators(
        self,
        mock_technical: MagicMock,
        mock_structure: MagicMock,
    ) -> None:
        """Test that generate_all_documentation calls both generators."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            service = DocumentationService(project_root)

            service.generate_all_documentation()

            mock_structure.assert_called_once()
            mock_technical.assert_called_once()

    def test_generate_all_documentation_creates_output_dir(self) -> None:
        """Test that documentation generation creates output directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            output_dir = Path(temp_dir) / "new_docs"

            service = DocumentationService(project_root, output_dir)

            # Mock the generators to avoid actual file operations
            with (
                patch.object(service, "_generate_structure_document"),
                patch.object(service, "_generate_technical_document"),
            ):
                service.generate_all_documentation()

            assert output_dir.exists()
            assert output_dir.is_dir()


class TestGenerateDocumentationFunction:
    """Test standalone generate_documentation function."""

    def test_generate_documentation_success(self) -> None:
        """Test successful documentation generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # Create a minimal project structure
            (project_root / "src").mkdir()
            (project_root / "src" / "main.py").write_text('print("hello")')

            result = generate_documentation(project_root)

            assert result == 0
            assert (project_root / "docs" / "STRUCTURE.md").exists()
            assert (project_root / "docs" / "TECHNICAL.md").exists()

    def test_generate_documentation_nonexistent_project(self) -> None:
        """Test documentation generation with nonexistent project root."""
        nonexistent_path = Path("/this/path/does/not/exist")

        result = generate_documentation(nonexistent_path)

        assert result == 1

    @patch.dict("os.environ", {"PROJECT_ROOT": "/custom/project/root"})
    @patch("docs.service.Path")
    def test_generate_documentation_uses_env_var(self, mock_path: MagicMock) -> None:
        """Test that function uses PROJECT_ROOT environment variable."""
        mock_project_root = MagicMock()
        mock_project_root.exists.return_value = False
        mock_path.return_value = mock_project_root

        result = generate_documentation()

        mock_path.assert_called_with("/custom/project/root")
        assert result == 1
