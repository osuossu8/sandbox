from typing import TypedDict

import numpy as np
from lightning import LightningModule
from omegaconf import DictConfig
from torch import Tensor, nn
from torch.optim import AdamW, Optimizer
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, LRScheduler


class Batch(TypedDict):
    image: Tensor
    mask: Tensor
    label: Tensor


class GISLModelModule(LightningModule):
    def __init__(
        self,
        model: nn.Module,
        cfg: DictConfig,
    ):
        super().__init__()

        self.cfg = cfg
        self.model = model(cfg)
        self.criterion = nn.CrossEntropyLoss()
        self.preds: list[int] = []
        self.gts: list[int] = []

    def forward(
        self,
        x: Tensor,
        attention_mask: Tensor | None,
    ) -> Tensor:
        return self.model(x, attention_mask)

    def _share_step(self, batch: Batch) -> tuple[Tensor, Tensor, Tensor]:
        images, masks, labels = batch["image"], batch["mask"], batch["label"]
        images = images.float()
        masks = masks.bool()
        logits = self.forward(images, masks)
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
