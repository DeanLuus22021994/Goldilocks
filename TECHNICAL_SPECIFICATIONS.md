Core app implementation
- /app/app.py
  - Logging and correlation ID
    - CorrelationIdFilter (ensures correlation_id on all log records)
    - before_request add_correlation_id_and_timing: sets g.correlation_id and start time
    - after_request add_response_headers: sets X-Request-ID and X-Response-Time-ms, logs request
  - Routes
    - GET / -> send_from_directory("static", "index.html")
    - GET /health -> returns {"status": "ok"}
    - GET /version
      - App version: APP_VERSION env var, else importlib.metadata.version("app"), else "0.1.0"
      - Flask version: pkg_version("Flask"), with fallback to flask.__version__ when PackageNotFoundError
      - Returns keys: app, python, flask, platform
  - Error handling
    - @app.errorhandler(404) -> {"message": "Not Found"}
  - Test/mypy compatibility
    - Explicit exports: __all__ = ["app", "pkg_version"] so tests can monkeypatch gold.pkg_version (fixes mypy attr-defined)

HTTP tests and fixtures
- /app/tests/conftest.py
  - Ensures repo root is importable for import app (adds ../ to sys.path)
  - Fixtures:
    - app -> Flask app instance
    - client -> FlaskClient
    - json_of -> turns response.data into dict
    - correlation_id_header -> {"X-Request-ID": "test-cid-123"}
  - Optional test output helpers (pytest_runtest_logreport/report_teststatus)
- /app/tests/index/test_index.py
  - GET / returns 200, Content-Type startswith "text/html"
  - Response has X-Request-ID echo and X-Response-Time-ms header (parsable as float)
- /app/tests/health/test_health.py
  - Status and body assertions for /health
  - Correlation header set when provided and auto-generated when missing
  - X-Response-Time-ms present and numeric
  - HEAD /health returns 200
- /app/tests/errors/test_404.py
  - Missing route returns 404 with {"message": "Not Found"}
- /app/tests/version/test_version.py
  - /version returns keys: {"app", "python", "flask", "platform"}
- /app/tests/version/test_version_fallback.py
  - Monkeypatches gold.pkg_version to raise PackageNotFoundError for "Flask"
  - Asserts fallback uses flask.__version__ (fix depends on app.py exporting pkg_version)

CI, test, and lint/type-check configuration
- /app/.github/workflows/ci.yml
  - Uses Python 3.13, caches pip
  - Installs deps, runs pytest with coverage (xml + term-missing)
  - Uploads coverage.xml as artifact
  - Runs mypy .
  - Runs pre-commit (installs hooks, then run --all-files)
- /app/pyproject.toml
  - pytest config (testpaths=tests, addopts include coverage)
  - mypy config (py3.13, warn_return_any, check_untyped_defs, etc.)
  - flake8 config mirrored here (note you also have a .flake8 file)
- /app/.pre-commit-config.yaml
  - Hooks: black, isort (profile black), flake8 + bugbear, mypy, pyupgrade, check-yaml, end-of-file-fixer, trailing-whitespace
- /app/requirements.txt
  - Runtime: Flask, gunicorn, python-json-logger
  - Dev: pytest, pytest-xdist, pytest-cov, coverage, mypy, pre-commit, flake8, black, isort
- /app/.flake8
  - max-line-length=100, extend-select=B,C4, ignore=W503 (duplicated with pyproject’s [tool.flake8])

Dev/run environment
- /app/Dockerfile
  - Python 3.13 slim, installs git and requirements
  - Copies app.py and static/
  - EXPOSE 9000
  - CMD runs gunicorn binding 0.0.0.0:9000, threads=2, workers set to "0" (this is unusual in gunicorn; typically workers >= 1)
- /app/docker-compose.yml
  - Builds Dockerfile, mounts project into /app, host networking + privileged, runs gunicorn command (see same workers=0 note)
- /app/.devcontainer/devcontainer.json
  - Uses docker-compose service web, forwards 9000
  - Installs Python + Copilot extensions
  - postCreateCommand installs requirements
- /app/.vscode/launch.json
  - Flask debug run: flask run --host 0.0.0.0 --port 9000 (no debugger, no reload)
- /app/.vscode/tasks.json
  - Tasks for Run Flask, pytest, watch, coverage, mypy, pre-commit
- /app/README.md
  - Documents run/test/type-check/pre-commit commands and endpoints

Static content
- /app/static/index.html
  - Minimal responsive styling, links to /health and /version, consistent with tests expecting text/html

Repo automation and guidance
- /app/.github/dependabot.yml
  - Tracks devcontainers weekly (consider adding pip and github-actions ecosystems if desired)
- /app/.github/copilot-instructions.md
  - The original task checklist (pytest, CI, Dockerfile, index.html styling, VS Code task, /version endpoint)

Likely attention points (non-blocking for tests, but worth noting)
- Gunicorn workers value "0" in Dockerfile and docker-compose (Gunicorn typically requires workers >= 1; if you hit runtime issues, set an explicit number or omit to use default via CMD args you control elsewhere).
- flake8 configuration appears in both pyproject.toml and .flake8; consider consolidating to one source of truth.
- /version app_version uses pkg_version("app"); since this repo isn’t an installed package, PackageNotFoundError will be common and fallback to "0.1.0" is expected. If you want dynamic versioning, consider reading from env, git, or packaging metadata.
