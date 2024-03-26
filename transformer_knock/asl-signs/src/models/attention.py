import torch
from omegaconf import DictConfig
from torch import Tensor, nn


class SimpleMultiHeadAttentionNet(nn.Module):
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
        self.head_num = 8

        self.query_linear = nn.Linear(cfg.feature_dim, self.depth)  # 246 -> 128
        self.key_linear = nn.Linear(cfg.feature_dim, self.depth)
        self.value_linear = nn.Linear(cfg.feature_dim, self.depth)

        self.last_linear = nn.Linear(self.depth, cfg.num_classes)
        self.criterion = nn.CrossEntropyLoss()

    def _split_head(self, x: Tensor) -> Tensor:
        x = x.unsqueeze(1)  # (batch_size, time, emb) -> (batch_size, 1, time, emb)
        x = x.view(
            x.size(0), self.head_num, x.size(2), self.depth // self.head_num,
        )  # (batch_size, 1, time, emb) -> (batch_size, head_num, time, depth//head_num)
        return x

    def _combine_head(self, x: Tensor) -> Tensor:
        batch_size, _, length, _ = x.size()
        return x.view(batch_size, length, self.depth)

    def forward(
        self,
        x: Tensor,  # (batch_size, time, emb)
        attention_mask: Tensor | None,  # (batch_size, time)
    ) -> Tensor:
        # input = memory -> self-attention
        input_x = x
        memory_x = x

        q = self.query_linear(input_x)  # (batch_size, time, depth)
        k = self.key_linear(memory_x)  # (batch_size, time, depth)
        v = self.value_linear(memory_x)  # (batch_size, time, depth)

        # multi head attention
        q = self._split_head(q)  # (batch_size, head_num, time, depth//head_num)
        k = self._split_head(k)
        v = self._split_head(v)

        # dot product
        # https://qiita.com/tand826/items/9e1b6a4de785097fe6a5
        if self.cfg.is_scaled_dot_product:
            q = q / (self.depth**0.5)
        logit = torch.matmul(q, k.transpose(2, 3))  # multi head

        if attention_mask is not None:
            # softmax する時に -inf が 0 になる
            attention_mask = attention_mask.data.masked_fill_(attention_mask, -torch.finfo(torch.float).max)
            attention_mask = attention_mask.unsqueeze(1)
            logit += attention_mask

        # normalization
        attention_weight = torch.nn.functional.softmax(logit, dim=3)

        attention_output = torch.matmul(attention_weight, v)  # (batch_size, head_num, time, depth//head_num)

        attention_output = self._combine_head(attention_output)

        output = self.last_linear(attention_output)  # (batch_size, time, num_classes)

        # avg with time channel
        output = output.mean(dim=1)  # (batch_size, num_classes)
        return output


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
        attention_mask: Tensor | None,  # (batch_size, time)
    ) -> Tensor:
        # input = memory -> self-attention
        input_x = x
        memory_x = x

        q = self.query_linear(input_x)  # (batch_size, time, depth)
        k = self.key_linear(memory_x)  # (batch_size, time, depth)
        v = self.value_linear(memory_x)  # (batch_size, time, depth)

        # dot product
        # https://qiita.com/tand826/items/9e1b6a4de785097fe6a5
        if self.cfg.is_scaled_dot_product:
            q = q / (self.depth**0.5)
        logit = torch.bmm(q, k.transpose(1, 2))  # single head

        if attention_mask is not None:
            # softmax する時に -inf が 0 になる
            attention_mask = attention_mask.data.masked_fill_(attention_mask, -torch.finfo(torch.float).max)
            logit += attention_mask

        # normalization
        attention_weight = torch.nn.functional.softmax(logit, dim=2)
        attention_output = torch.bmm(attention_weight, v)  # (batch_size, time, depth)
        output = self.last_linear(attention_output)  # (batch_size, time, num_classes)

        # avg with time channel
        output = output.mean(dim=1)  # (batch_size, num_classes)
        return output
