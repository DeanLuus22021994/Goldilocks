# Goldilocks Dev Container (Python + Flask)

Minimal, fast, reproducible Flask starter in a Dev Container.

Run

- Press F5, or:
  - flask --app app run --host 0.0.0.0 --port 9000 --no-debugger --no-reload
  - docker compose up --build (uses gunicorn on 9000)

Endpoints

- GET / -> serves static/index.html
- GET /health -> {"status":"ok"}
- GET /version -> app, Python, Flask, platform

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

- GitHub Actions runs pytest with coverage, caches pip, runs mypy and pre-commit.

Dev Container

- Python 3.13 image, pip cache persisted
- Git and make installed permanently in the Docker image (faster CI and consistent local dev)
- PIP_ROOT_USER_ACTION=ignore to suppress root warning
- Runs as root, privileged, host networking
- Port 9000 auto-opens on forward
