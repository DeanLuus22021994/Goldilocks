"""
Content processors for documentation.

Following SRP, this module handles only content processing
without cross-cutting concerns.
"""


class MarkdownProcessor:
    """Processes markdown using markitdown package when available."""

    def __init__(self) -> None:
        """Initialize processor with optional markitdown support."""
        self._markitdown: object | None = None
        self._initialize_markitdown()

    def _initialize_markitdown(self) -> None:
        """Lazy initialization of markitdown to handle import issues."""
        try:
            import markitdown  # type: ignore

            self._markitdown = markitdown.MarkItDown()
        except ImportError:
            self._markitdown = None

    def enhance_content(self, content: str) -> str:
        """Enhance content using markitdown if available."""
        if self._markitdown is None:
            return content

        # For now, return content as-is since we're generating markdown
        # In the future, could process various file types to markdown
        return content

    @property
    def is_available(self) -> bool:
        """Check if markitdown processor is available."""
        return self._markitdown is not None
