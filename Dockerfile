FROM python:3.13-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_INPUT=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Install minimal runtime deps (none needed for pure Python)
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY static ./static

ENV FLASK_APP=app.py
EXPOSE 9000

# Use gunicorn for high performance; default workers auto = 2*CPU+1
# Bind to all interfaces on port 9000, keep threads small for latency
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "0", "--threads", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
