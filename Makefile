.PHONY: check test emit fmt lint

check: fmt lint test

test:
	uv run pytest

emit:
	uv run python scripts/emit.py

fmt:
	uv run ruff format .

lint:
	uv run ruff check .
	uv run mypy scripts/ tests/
