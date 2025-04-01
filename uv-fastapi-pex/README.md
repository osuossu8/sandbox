# uv-fastapi-pex

fastapi サンプルアプリを pex に build して Docker コンテナ上で実行する
プロジェクト管理は uv で実施

## without docker container

```sh
uv sync --all-group
uv pip freeze > requirements.txt
uv run pex . -o sample-api-app.pex -e main -r requirements.txt -D src
```

## with docker container

```sh
docker compose up pex_container
```

```
REPOSITORY                      TAG                               IMAGE ID       CREATED         SIZE
uv-fastapi-pex-pex_container    latest                            5b36bbc802b8   3 seconds ago   161MB
```

## lint and format

```sh
uvx ruff check --fix
uvx ruff format
```