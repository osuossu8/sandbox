from omegaconf import DictConfig
from torch import Tensor, nn


class Conv1dNet(nn.Module):
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
