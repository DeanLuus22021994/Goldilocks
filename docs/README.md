---
uid: goldilocks.overview
title: Goldilocks Documentation
description: Comprehensive documentation for the Goldilocks Flask application
author: Goldilocks Development Team
ms.date: 2024-09-24
---

High-performance Flask application with optimized architecture and modern development practices.

> [!NOTE]
> This documentation is auto-generated and kept in sync with the current codebase structure using DocFX.

## 🚀 Quick Start

Get up and running with Goldilocks:

- **VS Code Dev Container**: Open folder and reopen in container; post-create installs deps and pre-commit hooks.
- **Run Options**:
  - VS Code task: Run Flask (port 9000)
  - Command line: `flask --app src.goldilocks.app run --host 0.0.0.0 --port 9000`
  - Docker: `docker compose up --build` (uses gunicorn on 9000)
- **Access**: Navigate to `http://localhost:9000`

## 📚 Documentation

Build and view comprehensive documentation with DocFX:

```bash
# Build documentation (first run downloads DocFX automatically)
./docs/bin/build.sh

# View generated site
cd docs/_site && python -m http.server 8080
# Access at http://localhost:8080
```

The documentation system:

- **Auto-build**: Downloads DocFX binaries on first use
- **Version Control**: Only configuration files tracked, binaries ignored
- **Comprehensive**: API docs, technical specs, Docker guides
- **Modern**: Static site generation with navigation and search

## 🎨 User Interface

Modern, accessible web interface:

- **Layout**: Sticky header, collapsible sidebar menu, main content, and footer
- **Theming**: Light/dark theme toggle with system preference detection
- **Responsive**: Mobile-friendly responsive layout
- **Accessibility**: Focus-visible indicators, reduced-motion support
- **Authentication**: Profile dropdown (demo via localStorage)

```javascript
// Enable demo auth
localStorage.setItem(
  "goldilocks-auth",
  JSON.stringify({ loggedIn: true, name: "Ada" })
);
// Disable demo auth
localStorage.removeItem("goldilocks-auth");
```

## 📡 API Endpoints

RESTful API with structured responses:

| Endpoint   | Method   | Response                   | Headers                          |
| ---------- | -------- | -------------------------- | -------------------------------- |
| `/`        | GET      | Serves `static/index.html` | -                                |
| `/health`  | GET/HEAD | `{"status":"ok"}`          | X-Request-ID, X-Response-Time-ms |
| `/version` | GET      | App/Python/Flask versions  | X-Request-ID, X-Response-Time-ms |
| `*`        | Any      | `{"message":"Not Found"}`  | 404 status                       |

## 🔍 Observability

Production-ready logging and monitoring:

- **Structured Logging**: JSON format with correlation IDs
- **Request Tracing**: X-Request-ID header (auto-generated if missing)
- **Performance**: X-Response-Time-ms timing header on all responses
- **Health Checks**: `/health` endpoint for load balancer monitoring

## 🧪 Testing & Quality

Comprehensive testing and code quality tools:

```bash
# Testing
pytest -q                                    # Run test suite
pytest -q --cov=goldilocks --cov-report=term-missing --cov-report=xml

# Static Analysis
mypy .                                       # Type checking
pre-commit run --all-files                   # All quality checks (black, isort, flake8, mypy)
```

## 🛠️ VS Code Integration

Pre-configured development tasks:

- **Run Flask (port 9000)** - Start development server
- **Test: pytest** - Run full test suite
- **Test: watch (looponfail)** - Continuous testing
- **Coverage** - Generate coverage reports
- **Type check (mypy)** - Static type analysis
- **Pre-commit (all files)** - Code quality validation

## 🚀 CI/CD Pipeline

Automated workflows with GitHub Actions:

- **Testing**: pytest with coverage reporting
- **Caching**: pip dependencies and pre-commit hooks
- **Quality**: mypy type checking and linting
- **Performance**: Build time and test execution monitoring

## 🐳 Development Container

Optimized Docker-based development:

- **Base**: Python 3.14.0 with pip cache persistence
- **Tools**: Git, make, and all development dependencies pre-installed
- **Setup**: Automated pip upgrade, requirements installation, pre-commit hooks
- **Networking**: Port 9000 auto-forwarding and browser opening

## 🔧 Troubleshooting

Common development issues and solutions:

### Pylance Import Errors

If you see "Import ... could not be resolved" in VS Code:

1. Ensure you're opened in the Dev Container (has Flask/pytest installed)
2. Select correct Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose the container environment interpreter

### Container Issues

- **Slow rebuilds**: Check devcontainer-lock.json for cache invalidation
- **Port conflicts**: Ensure port 9000 is available
- **Permission errors**: Verify Docker has proper file system access

## 📚 Related Documentation

- [Technical Specifications](xref:goldilocks.technical) - Architecture and performance details
- [Project Structure](xref:goldilocks.structure) - File organization and modules
- [API Reference](xref:goldilocks.api) - Generated API documentation
