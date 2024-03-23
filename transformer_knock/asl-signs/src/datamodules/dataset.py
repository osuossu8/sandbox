import numpy as np
import numpy.typing as npt
import pandas as pd
import torch
from lightning import LightningModule
from omegaconf import DictConfig
from torch.utils.data import DataLoader, Dataset

ROWS_PER_FRAME = 543


def load_relevant_data_subset(pq_path: str) -> npt.NDArray[np.float32]:
    data_columns = ["x", "y", "z"]
    data = pd.read_parquet(pq_path, columns=data_columns)
    n_frames = int(len(data) / ROWS_PER_FRAME)
    data = data.to_numpy().reshape(n_frames, ROWS_PER_FRAME, len(data_columns))
    return data.astype(np.float32)


class GISLDataset(Dataset):  # type: ignore
    def __init__(self, df: pd.DataFrame, cfg: DictConfig) -> None:
        self.df = df
        self.paths = df["path"].to_numpy()
        self.labels = df["label"].to_numpy()
        self.max_length = cfg.max_length
        self.num_point = cfg.num_point

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        pq_path = self.paths[idx]
        xyz = load_relevant_data_subset(pq_path)
        xyz = torch.from_numpy(xyz)

        # normalize
        xyz = xyz - xyz[~torch.isnan(xyz)].mean(0, keepdim=True)
        xyz = xyz / xyz[~torch.isnan(xyz)].std(0, keepdim=True)

        LIP = [
            61,
            185,
            40,
            39,
            37,
            0,
            267,
            269,
            270,
            409,
            291,
            146,
            91,
            181,
            84,
            17,
            314,
            405,
            321,
            375,
            78,
            191,
            80,
            81,
            82,
            13,
            312,
            311,
            310,
            415,
            95,
            88,
            178,
            87,
            14,
            317,
            402,
            318,
            324,
            308,
        ]
        lip = xyz[:, LIP]
        lhand = xyz[:, 468:489]
        rhand = xyz[:, 522:543]
        xyz = torch.cat(
            [  # (len_seq, num_point, 3)
                lip,
                lhand,
                rhand,
            ],
            1,
        )

        # fill 0
        xyz[torch.isnan(xyz)] = 0

        len_seq = len(xyz)
        # (len_seq, num_point, 3) -> (len_seq, num_point * 3) # time, emb
        xyz = xyz.reshape(len_seq, self.num_point * 3)

        if len_seq <= self.max_length:
            padded = torch.zeros((self.max_length, self.num_point * 3))
            padded[:len_seq] = xyz
            xyz = padded
        else:
            xyz = xyz[: self.max_length]
        return {"image": xyz.to(torch.float32), "label": torch.tensor(self.labels[idx]).type(torch.LongTensor)}


class GISLDataModule(LightningModule):
    def __init__(
        self,
        train_df: pd.DataFrame,
        val_df: pd.DataFrame,
        cfg: DictConfig,
    ):
        super().__init__()
        self.train_df = train_df
        self.val_df = val_df
        self.cfg = cfg

    def _create_dataset(self, train: bool = True) -> GISLDataset:
        return GISLDataset(self.train_df, self.cfg) if train else GISLDataset(self.val_df, self.cfg)

    def train_dataloader(self) -> DataLoader:  # type: ignore
        dataset = self._create_dataset(True)
        return DataLoader(dataset, **self.cfg.train_loader)

    def val_dataloader(self) -> DataLoader:  # type: ignore
        dataset = self._create_dataset(False)
        return DataLoader(dataset, **self.cfg.val_loader)
