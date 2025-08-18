FROM python:3.13-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_NO_INPUT=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY static ./static

ENV FLASK_APP=app.py
EXPOSE 9000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9000", "--no-debugger", "--no-reload"]
