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

## run train

```bash
poetry run python exp/001.py
```

## lint and format

```bash
ruff format .
ruff check . --fix
mypy .
```

## watch performance

```bash
watch free -h
watch nvidia-smi
```
