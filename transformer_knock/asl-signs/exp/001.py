import sys

sys.path.append("/root/sandbox/transformer_knock/asl-signs/")
import json
from pathlib import Path
from typing import cast

import pandas as pd
from lightning import Trainer, seed_everything
from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint
from lightning.pytorch.loggers import CSVLogger
from omegaconf import DictConfig, OmegaConf

from src.create_kfold import DataSplitter
from src.datamodules.dataset import GISLDataModule
from src.models.conv1dnet import Conv1dNet
from src.models.modelmodule import GISLModelModule

datasplitter = DataSplitter(
    target_col="label",
    group_col="participant_id",
)


root_dir = Path("/root/sandbox/transformer_knock/asl-signs/")
label_map_path = Path(root_dir / "data" / "sign_to_prediction_index_map.json")

with label_map_path.open(mode="r") as f:
    label_map = json.load(f)

df = pd.read_csv(root_dir / "data/train.csv")
df["path"] = df["path"].map(lambda x: root_dir / "data" / x)
df["label"] = df["sign"].map(label_map)

df = datasplitter.split(df)
train_df = df[df["kfold"] != 0].reset_index(drop=True)
val_df = df[df["kfold"] == 0].reset_index(drop=True)

config_path = root_dir / "config" / "001.yaml"
config = cast(DictConfig, OmegaConf.load(config_path))
seed_everything(config.seed)

datamodule = GISLDataModule(train_df, val_df, config)
model = GISLModelModule(Conv1dNet, config)

lr_monitor = LearningRateMonitor()
metric_checkpoint = ModelCheckpoint(**config.checkpoint)

logging_path = root_dir / "logs" / "001"
logging_path.mkdir(parents=True, exist_ok=True)
csv_logger = CSVLogger(logging_path)
trainer = Trainer(logger=csv_logger, callbacks=[lr_monitor, metric_checkpoint], **config.trainer)
trainer.fit(model, datamodule=datamodule)
