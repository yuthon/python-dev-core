format:
	uv run ruff format . --config=pyproject.toml

lint:
	uv run ruff check . --fix --config=pyproject.toml

typecheck:
	uv run mypy src/ --strict

test:
	uv run pytest

check: format lint typecheck test

check-all:
	uv run pre-commit run --all-files