# fastapi-psql-sqlalchemy-alembic-trigger-function-practice

fastapi + postgresql + sqlalchemy + alembic の構成で trigger function を migration ファイルに設定するサンプルコード

## 背景

- fastapi + postgresql + sqlalchemy + alembic の構成自体は日本語でも多くの記事で紹介されている
- 紹介されている記事のサンプルコードは APP 側で時刻設定するものが多い (default, onupdate)
- 上記の構成で DB 側でレコードが追加された時の created_at と updated_at を設定したい
    - APP 側の時刻で設定すると利用する API が増えたりクラスタを構築する場合などに時刻の整合性がとれなくなる
- DB 側で設定する引数は紹介されているが Column に設定するだけでは正しく動作しない
    - 引数は server_default, server_onupdate
    - 期待通りに動作させるところまで踏み込んだ情報にアクセスするのが大変だった
        - postgresql では trigger なるものを設定しないといけないらしい
        - mysql だと DB 側で設定する updated_at は期待通りの挙動らしい


## 手順

初回のみ

```sh
uv sync --all-groups

# init command 
# this should be run only once
rm -rf migration
mkdir -p migration
uv --directory migration run alembic init alembic
uv --directory migration run alembic revision --autogenerate -m "init"
```

それ以降

```sh
# terminal 1
uv run uvicorn api.main:app --host 0.0.0.0 --port 1111 --reload

# terminal 2
# make refresh
# make migrate
make e2e
```

## Without trigger function for updated_at
```
$ make e2e
curl -X POST -H "Content-Type: application/json" -d @request_sample.json http://localhost:1111/tasks/
{"title":"sugoi_task","done":false}

docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"
 id |   title    | done |         created_at         |         updated_at         
----+------------+------+----------------------------+----------------------------
  1 | sugoi_task | f    | 2025-04-08 14:49:39.426614 | 2025-04-08 14:49:39.426614
(1 row)

curl -X POST -H "Content-Type: application/json" -d '{"title": "sugoi_task", "done": true}' http://localhost:1111/tasks/1
{"title":"sugoi_task","done":true}

docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"
 id |   title    | done |         created_at         |         updated_at         
----+------------+------+----------------------------+----------------------------
  1 | sugoi_task | t    | 2025-04-08 14:49:39.426614 | 2025-04-08 14:49:39.426614
(1 row)
```

## With trigger function for updated_at

```
curl -X POST -H "Content-Type: application/json" -d @request_sample.json http://localhost:1111/tasks/
{"title":"sugoi_task","done":false}

docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"
 id |   title    | done |         created_at         |         updated_at         
----+------------+------+----------------------------+----------------------------
  1 | sugoi_task | f    | 2025-04-08 15:00:51.288145 | 2025-04-08 15:00:51.288145
(1 row)



curl -X POST -H "Content-Type: application/json" -d '{"title": "sugoi_task", "done": true}' http://localhost:1111/tasks/1
{"title":"sugoi_task","done":true}

docker exec -it fastapi-psql-sqlalchemy-alembic-trigger-function-practice-sample_db-1 psql -U user -d sample_db -c "select * from tasks"
 id |   title    | done |         created_at         |         updated_at         
----+------------+------+----------------------------+----------------------------
  1 | sugoi_task | t    | 2025-04-08 15:00:51.288145 | 2025-04-08 15:00:53.540015
(1 row)
```

## References

- [postgresql docs - trigger functions](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [sqlalchemy issue](https://github.com/sqlalchemy/sqlalchemy/issues/3444#issuecomment-441929501)
- [stackoverflow](https://stackoverflow.com/questions/2362871/postgresql-current-timestamp-on-update)
- https://www.morling.dev/blog/last-updated-columns-with-postgres/