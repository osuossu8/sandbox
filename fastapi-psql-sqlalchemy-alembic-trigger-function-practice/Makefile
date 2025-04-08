lint:
	uv sync --all-groups
	uvx ruff check --fix
	uvx ruff format

refresh:
	docker compose down sample_db
	docker compose up -d sample_db

migrate:
	uv --directory migration run alembic upgrade head

list_tables:
	docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "\dt";