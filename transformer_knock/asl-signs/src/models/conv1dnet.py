from typing import TypedDict

import numpy as np
from lightning import LightningModule
from omegaconf import DictConfig
from torch import Tensor, nn
from torch.optim import AdamW, Optimizer
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, LRScheduler


class Batch(TypedDict):
    image: Tensor
    label: Tensor


class Conv1dNet(LightningModule):
    def __init__(
        self,
        cfg: DictConfig,
    ):
        super().__init__()

        self.cfg = cfg
        self.conv0 = nn.Sequential(
            nn.Conv1d(cfg.feature_dim, 128, kernel_size=3, stride=1, padding="same"),
            nn.BatchNorm1d(128),
            nn.ReLU(),
        )
        self.conv1 = nn.Conv1d(128, cfg.num_classes, 1)
        self.linear = nn.Linear(cfg.max_length, 1)
        self.criterion = nn.CrossEntropyLoss()
        self.preds: list[int] = []
        self.gts: list[int] = []

    def forward(
        self,
        x: Tensor,
    ) -> Tensor:
        x = x.transpose(1, 2)  # (batch_size, n_timesteps, n_channels)
        x = self.conv0(x)
        x = self.conv1(x)  # (batch_size, n_timesteps, n_classes)
        x = self.linear(x)
        output = x[:, :, 0]
        return output

    def _share_step(self, batch: Batch) -> tuple[Tensor, Tensor, Tensor]:
        images, labels = batch["image"], batch["label"]
        images = images.float()
        logits = self.forward(images)
        loss = self.criterion(logits, labels)
        return loss, logits, labels

    def training_step(self, batch: Batch, batch_idx: int) -> Tensor:
        loss, *_ = self._share_step(batch)
        self.log("train_loss", loss, on_epoch=True, prog_bar=True, on_step=False)
        return loss

    def validation_step(self, batch: Batch, batch_idx: int) -> Tensor:
        loss, logits, labels = self._share_step(batch)
        self.log("val_loss", loss, on_epoch=True, prog_bar=True, on_step=False)
        outputs = logits.argmax(dim=1).cpu().numpy().tolist()
        labels = labels.cpu().numpy().tolist()
        self.preds.extend(outputs)
        self.gts.extend(labels)
        return loss

    def on_validation_epoch_end(self) -> None:
        preds = np.array(self.preds)
        labels = np.array(self.gts)
        acc = np.mean(preds == labels)
        self.log("val_acc", acc, on_epoch=True, prog_bar=True)
        self.preds.clear()
        self.gts.clear()

    def configure_optimizers(self) -> tuple[list[Optimizer], list[LRScheduler]]:
        optimizer = AdamW(self.parameters(), **self.cfg.optimizer.params)
        scheduler = CosineAnnealingWarmRestarts(optimizer, **self.cfg.scheduler.params)
        return [optimizer], [scheduler]
