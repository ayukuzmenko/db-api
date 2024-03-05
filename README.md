# The Database API

## Overview

This Database Application is designed to simulate basic database operations.

## Features

- CRUD Operations: Perform create (insert), read (select), and delete operations.
- Transaction Support: Simulate the start, commit, and rollback of transactions.

## Getting Started

### Installation

Clone the repository and install the dependencies using Poetry:

```console
poetry install
```

### Running the Application

Start the application with Uvicorn:

```console
poetry run uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to view the Swagger UI and test the API endpoints.

## Development Commands

The project includes a Makefile to simplify common development tasks:

- make install: Install project dependencies.
- make isort: Sort import statements.
- make black: Format code according to Black's style.
- make flake8: Lint code to catch errors and enforce style.
- make mypy: Check types to catch type errors.
- make test: Run tests to ensure code changes don't break existing functionality.
- make format: Execute all linting and formatting commands.
- make start: Launch the FastAPI server.
- make clean: Clean up the project

