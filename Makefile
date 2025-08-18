.PHONY: install format lint test test-watch cov mypy precommit run dev docker-build docker-run

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

format:
	isort .
	black .

lint:
	flake8 .
	mypy .

test:
	pytest -q

test-watch:
	pytest -q -f

cov:
	pytest -q --cov=app --cov-report=term-missing --cov-report=xml

mypy:
	mypy .

precommit:
	pre-commit install-hooks
	pre-commit run --all-files

run:
	flask --app app run --host 0.0.0.0 --port 9000 --no-debugger --no-reload

dev: run

docker-build:
	docker build -t goldilocks-flask:latest .

docker-run:
	docker run --rm -it -p 9000:9000 goldilocks-flask:latest
