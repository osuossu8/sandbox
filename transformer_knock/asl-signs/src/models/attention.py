import torch
from omegaconf import DictConfig
from torch import Tensor, nn


class SimpleAttentionNet(nn.Module):
    """
    https://qiita.com/halhorn/items/c91497522be27bde17ce
    """

    def __init__(
        self,
        cfg: DictConfig,
    ):
        super().__init__()

        self.cfg = cfg
        self.depth = 128

        self.query_linear = nn.Linear(cfg.feature_dim, self.depth)  # 246 -> 128
        self.key_linear = nn.Linear(cfg.feature_dim, self.depth)
        self.value_linear = nn.Linear(cfg.feature_dim, self.depth)

        self.last_linear = nn.Linear(self.depth, cfg.num_classes)
        self.criterion = nn.CrossEntropyLoss()

    def forward(
        self,
        x: Tensor,  # (batch_size, time, emb)
    ) -> Tensor:
        # input = memory -> self-attention
        input_x = x
        memory_x = x

        q = self.query_linear(input_x)  # (batch_size, time, depth)
        k = self.key_linear(memory_x)  # (batch_size, time, depth)
        v = self.value_linear(memory_x)  # (batch_size, time, depth)

        # dot product
        # https://qiita.com/tand826/items/9e1b6a4de785097fe6a5
        logit = torch.bmm(q, k.transpose(1, 2))

        # normalization
        attention_weight = torch.nn.functional.softmax(logit, dim=2)

        attention_output = torch.bmm(attention_weight, v)  # (batch_size, time, depth)

        output = self.last_linear(attention_output)  # (batch_size, time, num_classes)

        # avg with time channel
        output = output.mean(dim=1)  # (batch_size, num_classes)
        return output
