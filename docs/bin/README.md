# Documentation Build Tools

This directory contains build dependencies and tools required for generating documentation.

## Purpose

- **DocFX binaries**: For generating static documentation sites
- **Build tools**: Additional tools needed for documentation processing
- **Dependencies**: Runtime dependencies for documentation generation

## Usage

Build tools should be downloaded/installed into this directory during the documentation build process:

```bash
# Example: Download DocFX
cd docs/bin
wget https://github.com/dotnet/docfx/releases/latest/download/docfx-linux-x64.zip
unzip docfx-linux-x64.zip

# Build documentation
cd ..
./bin/docfx docfx.json
```

## Notes

- Files in this directory are ignored by Git (see `.gitignore`)
- Copilot ignores binary files but is aware of the directory structure
- This keeps the repository clean while maintaining build capability
