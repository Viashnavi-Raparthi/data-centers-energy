.PHONY: install test lint run api clean

install:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

run:
	python -m gridportfolio.pipeline

api:
	uvicorn gridportfolio.api.app:app --reload

clean:
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf **/__pycache__
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info