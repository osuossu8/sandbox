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
poetry run python exp/run.py 004 --debug True
```

```bash
for exp_id in "001" "002" "003" "004" "005";
do
    echo " "
    echo "start exp ${exp_id}"
    echo " "
    poetry run python exp/run.py ${exp_id} --debug True
done
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
