"""
Command-line interface for documentation generation.

Following SRP, this module handles only CLI concerns without
business logic cross-cutting.
"""

import os
import sys
from pathlib import Path

from .service import generate_documentation


def main() -> int:
    """Main CLI entry point."""
    try:
        # Get project root from environment or use current working directory
        project_root = Path(os.environ.get("PROJECT_ROOT", os.getcwd()))
        return generate_documentation(project_root)
    except KeyboardInterrupt:
        print("\n❌ Documentation generation cancelled by user")
        return 130
    except Exception as e:
        print(f"❌ Error generating documentation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
