lint:
	uv sync --all-groups
	uv run ruff check --fix
	uv run ruff format

refresh:
	docker compose down sample_db
	docker compose up -d sample_db

migrate:
	uv --directory migration run alembic upgrade head
