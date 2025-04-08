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

e2e:
	docker compose down sample_db
	docker compose up -d sample_db
	@sleep 1
	@echo "\n"
	uv --directory migration run alembic upgrade head
	@sleep 1
	@echo "\n"
	curl -X POST -H "Content-Type: application/json" -d @request_sample.json http://localhost:1111/tasks/
	@sleep 1
	@echo "\n"
	docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"
	@sleep 1
	@echo "\n"
	curl -X POST -H "Content-Type: application/json" -d '{"title": "sugoi_task", "done": true}' http://localhost:1111/tasks/1
	@sleep 1
	@echo "\n"
	docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"