import sys

sys.path.append("/root/sandbox/transformer_knock/asl-signs/")
import json
from pathlib import Path

import pandas as pd

from src.create_kfold import DataSplitter

datasplitter = DataSplitter(
    target_col="label",
    group_col="participant_id",
)


root_dir = Path("/root/sandbox/transformer_knock/asl-signs/")
label_map_path = Path(root_dir / "data" / "sign_to_prediction_index_map.json")

with label_map_path.open(mode="r") as f:
    label_map = json.load(f)

df = pd.read_csv(root_dir / "data/train.csv")
df["path"] = df["path"].map(lambda x: root_dir / x)
df["label"] = df["sign"].map(label_map)

df = datasplitter.split(df)

print(df["kfold"].value_counts())
print(df)
