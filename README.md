# Goldilocks Dev Container (Python + Flask)

Minimal, fast, reproducible Flask starter in a Dev Container.

Quickstart

- VS Code Dev Container: open folder and reopen in container; post-create installs deps and pre-commit hooks.
- Run:
  - VS Code task: Run Flask (port 9000)
  - Or: flask --app app run --host 0.0.0.0 --port 9000 --no-debugger --no-reload
  - Or: docker compose up --build (uses gunicorn on 9000)
- Open in browser: $BROWSER http://localhost:9000

Endpoints

- GET / -> serves static/index.html
- GET /health -> {"status":"ok"}; supports HEAD; sets X-Request-ID and X-Response-Time-ms
- GET /version -> app, python, flask, platform (app version via APP_VERSION env or fallback)
- 404 -> JSON {"message":"Not Found"}

Observability

- Structured logging (JSON if python-json-logger present), includes correlation_id.
- Request correlation via X-Request-ID header (auto-generated if absent).
- Timing header X-Response-Time-ms on all responses.

UI

- Minimal responsive layout, modular CSS/JS, accessible theme toggle (light/dark) with persistence and prefers-color-scheme.
- Favicon included; focus-visible outlines; reduced-motion friendly; density utilities (compact/comfortable).

Testing

- pytest -q
- Coverage: pytest -q --cov=app --cov-report=term-missing --cov-report=xml

Static analysis

- mypy .
- pre-commit run --all-files (black, isort, flake8, mypy, pyupgrade)

VS Code tasks

- Run Flask (port 9000)
- Test: pytest
- Test: watch (looponfail)
- Coverage
- Type check (mypy)
- Pre-commit (all files)

CI

- GitHub Actions: pytest with coverage, caches pip, mypy and pre-commit.

Dev Container

- Python 3.13 slim base, pip cache persisted.
- Git and make installed permanently in the Docker image.
- postCreateCommand upgrades pip, installs requirements, installs pre-commit hooks.
- Port 9000 auto-forwards and opens.
