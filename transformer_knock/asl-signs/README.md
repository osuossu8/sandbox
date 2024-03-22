# asl-signs

https://www.kaggle.com/competitions/asl-signs

## setup env

```bash
poetry lock
poetry install
```

## prepare data

```bash
kaggle competitions download -c asl-signs
```

## lint and format

```bash
ruff format .
ruff check . --fix
```
