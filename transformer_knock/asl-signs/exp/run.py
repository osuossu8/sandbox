import sys

sys.path.append("/workspace/sandbox/transformer_knock/asl-signs/")
import json
from pathlib import Path
from typing import cast

import click
import hydra
import pandas as pd
from lightning import Trainer, seed_everything
from lightning.pytorch.callbacks import LearningRateMonitor, ModelCheckpoint
from lightning.pytorch.loggers import CSVLogger
from omegaconf import DictConfig, OmegaConf

from src.create_kfold import DataSplitter
from src.datamodules.dataset import GISLDataModule
from src.models.modelmodule import GISLModelModule


@click.command()
@click.argument("exp-id", type=str)
@click.option("--epoch", type=int, default=-1, help="Epoch")
@click.option("--debug", type=bool, default=False, help="Debug mode")
def main(exp_id: str, epoch: int, debug: bool) -> None:
    datasplitter = DataSplitter(
        target_col="label",
        group_col="participant_id",
    )

    root_dir = Path("/workspace/sandbox/transformer_knock/asl-signs/")
    data_dir = root_dir / "data"
    label_map_path = Path(data_dir / "sign_to_prediction_index_map.json")

    with label_map_path.open(mode="r") as f:
        label_map = json.load(f)

    df = pd.read_csv(data_dir / "train.csv")
    df["path"] = df["path"].map(lambda x: data_dir / x)
    df["label"] = df["sign"].map(label_map)

    df = datasplitter.split(df)
    train_df = df[df["kfold"] != 0].reset_index(drop=True)
    val_df = df[df["kfold"] == 0].reset_index(drop=True)

    if debug:
        train_df = train_df.head(1000)
        val_df = val_df.head(1000)

    config_path = root_dir / "config" / f"{exp_id}.yaml"
    config = cast(DictConfig, OmegaConf.load(config_path))
    seed_everything(config.seed)

    if epoch > 0:
        config.epoch = epoch
        config.scheduler.params.T_0 = epoch
        config.trainer.max_epochs = epoch

    datamodule = GISLDataModule(train_df, val_df, config)
    model_defintion = hydra.utils.get_class(config.model.definition)
    model = GISLModelModule(model_defintion, config)

    lr_monitor = LearningRateMonitor()
    metric_checkpoint = ModelCheckpoint(**config.checkpoint)

    logging_path = root_dir / "logs" / f"{exp_id}"
    logging_path.mkdir(parents=True, exist_ok=True)
    csv_logger = CSVLogger(logging_path)
    trainer = Trainer(logger=csv_logger, callbacks=[lr_monitor, metric_checkpoint], **config.trainer)
    trainer.fit(model, datamodule=datamodule)


if __name__ == "__main__":
    main()
