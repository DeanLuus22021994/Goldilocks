# Goldilocks Dev Container (Python + Flask)

Minimal, fast, reproducible Flask starter in a Dev Container.

Run

- Press F5, or:
  - flask --app app run --host 0.0.0.0 --port 9000 --no-debugger --no-reload
  - docker compose up --build (uses gunicorn on 9000)

Endpoints

- GET / -> serves static/index.html
- GET /healthz -> {"status":"ok"}
- GET /version -> app, Python, Flask, platform

Testing

- pytest -q

CI

- GitHub Actions runs pytest on push/PR.

Dev Container

- Python 3.13 image, pip cache persisted
- Git installed for VS Code integration
- PIP_ROOT_USER_ACTION=ignore to suppress root warning
- Runs as root, privileged, host networking
- Port 9000 auto-opens on forward
