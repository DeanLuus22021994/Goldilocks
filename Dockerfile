FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_INPUT=1 \
  PIP_ROOT_USER_ACTION=ignore \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Install Git for VS Code and general use
RUN apt-get update \
  && apt-get install -y --no-install-recommends git ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY static ./static

ENV FLASK_APP=app.py
EXPOSE 9000

# Use gunicorn for high performance; default workers auto = 2*CPU+1
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "0", "--threads", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]