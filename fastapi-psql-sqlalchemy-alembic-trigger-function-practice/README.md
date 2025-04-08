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

```sh
uv sync --all-groups
```

## TODO

- os.getenv → pydantic-settings