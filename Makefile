default:help

help:
	@echo "db api"

clean:
	@echo "Cleaning up..."
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.pyo" -exec rm -f {} +
	@echo "Cleanup complete."

# Project setup

install:
	poetry install

# Development

isort:
	isort src

black:
	black src

flake8:
	flake8 src

mypy:
	mypy src

test:
	pytest

format: isort black flake8 mypy

# Start project

start:
	uvicorn src.db_api.main:app --reload

