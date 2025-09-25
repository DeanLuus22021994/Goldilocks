"""
Documentation service orchestrating all components.

Following dependency inversion principle, this service coordinates
different components without cross-cutting concerns.
"""

from pathlib import Path

from .collectors import ProjectDataCollector, SystemDataCollector
from .generators import StructureContentGenerator, TechnicalContentGenerator
from .models import GenerationContext
from .processors import MarkdownProcessor


class DocumentationService:
    """Main service orchestrating documentation generation."""

    def __init__(
        self,
        project_root: Path,
        output_dir: Path | None = None,
    ) -> None:
        """Initialize service with dependencies."""
        self.project_root = project_root
        self.output_dir = output_dir or (project_root / "docs")

        # Initialize components following dependency injection
        self._project_collector = ProjectDataCollector(project_root)
        self._system_collector = SystemDataCollector(project_root)
        self._structure_generator = StructureContentGenerator()
        self._technical_generator = TechnicalContentGenerator()
        self._processor = MarkdownProcessor()

    def generate_all_documentation(self) -> None:
        """Generate all documentation following orchestration pattern."""
        print("🚀 Starting modern documentation generation...")

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

        # Collect data
        metrics = self._project_collector.collect_metrics()
        system_info = self._system_collector.collect_system_info()

        # Create generation context
        context = GenerationContext(
            project_root=self.project_root,
            output_dir=self.output_dir,
            metrics=metrics,
            system_info=system_info,
        )

        # Generate documents
        self._generate_structure_document(context)
        self._generate_technical_document(context)

        print("✅ Documentation generation complete!")

    def _generate_structure_document(self, context: GenerationContext) -> None:
        """Generate STRUCTURE.md document."""
        print("Generating STRUCTURE.md...")

        content = self._structure_generator.generate_content(context)
        enhanced_content = self._processor.enhance_content(content)

        output_path = context.output_dir / "STRUCTURE.md"
        output_path.write_text(enhanced_content, encoding="utf-8")
        print(f"✅ Generated {output_path}")

    def _generate_technical_document(self, context: GenerationContext) -> None:
        """Generate TECHNICAL.md document."""
        print("Generating TECHNICAL.md...")

        content = self._technical_generator.generate_content(context)
        enhanced_content = self._processor.enhance_content(content)

        output_path = context.output_dir / "TECHNICAL.md"
        output_path.write_text(enhanced_content, encoding="utf-8")
        print(f"✅ Generated {output_path}")


# For backwards compatibility, provide a simple function interface
def generate_documentation(
    project_root: Path | None = None,
    output_dir: Path | None = None,
) -> int:
    """Generate documentation with simple function interface."""
    import os

    if project_root is None:
        project_root = Path(os.environ.get("PROJECT_ROOT", os.getcwd()))

    if not project_root.exists():
        print(f"❌ Project root not found: {project_root}")
        return 1

    service = DocumentationService(project_root, output_dir)
    service.generate_all_documentation()
    return 0
