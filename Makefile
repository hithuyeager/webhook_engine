.PHONY: up down migrate test lint typecheck

up:
	docker compose up -d --build

down:
	docker compose down

migrate:
	uv run alembic upgrade head

test:
	uv run pytest -v

lint:
	uv run ruff check app tests alembic

typecheck:
	uv run mypy app tests