# Goldilocks Dev Container (Python + Flask)

Minimal, fast, reproducible Flask starter in a Dev Container.

Quickstart

- VS Code Dev Container: open folder and reopen in container; post-create installs deps and pre-commit hooks.
- Run:
  - VS Code task: Run Flask (port 9000)
  - Or: flask --app app run --host 0.0.0.0 --port 9000 --no-debugger --no-reload
  - Or: docker compose up --build (uses gunicorn on 9000)
- Open in browser: `$BROWSER http://localhost:9000`

Shell UI

- Top header bar (sticky), Azure-portal-like collapsible sidebar menu, main content, and footer.
- Theme toggle (light/dark), health badge, and responsive layout.
- Profile dropdown (top-right) appears when logged in. For demo, toggle via localStorage:
  - localStorage.setItem("goldilocks-auth", JSON.stringify({ loggedIn: true, name: "Ada" }))
  - localStorage.removeItem("goldilocks-auth") to hide again.

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

- Modular CSS/JS, accessible theme toggle, focus-visible, reduced-motion friendly.
- Density utilities (compact/comfortable), favicon.

Testing

- pytest -q
- Coverage: pytest -q --cov=app --cov-report=term-missing --cov-report=xml

Static analysis

- mypy .
- pre-commit run --all-files (black, isort, flake8, mypy, pyupgrade)

Environment cleanup

- python clean.py (removes Python cache, pytest cache, mypy cache, temp files)
- Use this to clear IDE errors caused by stale cache files

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

- Python 3.14.0 base, pip cache persisted.
- Git and make installed permanently in the Docker image.
- postCreateCommand upgrades pip, installs requirements, installs pre-commit hooks.
- Port 9000 auto-forwards and opens.

Troubleshooting: Pylance missing imports

- If you see "Import ... could not be resolved" in VS Code, ensure you're opened in the Dev Container so the interpreter has Flask/pytest installed.
- Or select the correct Python interpreter (Command Palette → Python: Select Interpreter) corresponding to the container environment.
