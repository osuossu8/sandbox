import numpy as np
import torch
from omegaconf import DictConfig
from torch import Tensor, nn


def positional_encoding(length, embed_dim):
    dim = embed_dim // 2

    position = np.arange(length)[:, np.newaxis]  # (seq, 1)
    dim = np.arange(dim)[np.newaxis, :] / dim  # (1, dim)

    angle = 1 / (10000**dim)  # (1, dim)
    angle = position * angle  # (pos, dim)

    pos_embed = np.concatenate([np.sin(angle), np.cos(angle)], axis=-1)
    pos_embed = torch.from_numpy(pos_embed).float()
    return pos_embed


class SimpleMultiHeadAttentionNetWithPositionalEncoding(nn.Module):
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

        self.pos_encoding = positional_encoding(cfg.max_length, cfg.feature_dim)
        self.pos_encoding = self.pos_encoding.cuda()

        self.query_linear = nn.Linear(cfg.feature_dim, self.depth)  # 246 -> 128
        self.key_linear = nn.Linear(cfg.feature_dim, self.depth)
        self.value_linear = nn.Linear(cfg.feature_dim, self.depth)

        self.last_linear = nn.Linear(self.depth, cfg.num_classes)
        self.criterion = nn.CrossEntropyLoss()

    def _split_head(self, x: Tensor) -> Tensor:
        x = x.unsqueeze(1)  # (batch_size, time, emb) -> (batch_size, 1, time, emb)
        # contiguous あってもなくても精度変わらなかったけど念の為
        x = x.contiguous().view(
            x.size(0),
            self.head_num,
            x.size(2),
            self.depth // self.head_num,
        )  # (batch_size, 1, time, emb) -> (batch_size, head_num, time, depth//head_num)
        return x

    def _combine_head(self, x: Tensor) -> Tensor:
        batch_size, _, length, _ = x.size()
        return x.contiguous().view(batch_size, length, self.depth)

    def forward(
        self,
        x: Tensor,  # (batch_size, time, emb)
        attention_mask: Tensor | None,  # (batch_size, time)
    ) -> Tensor:
        # input = memory -> self-attention

        x = x + self.pos_encoding
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


class SimpleMultiHeadAttentionNetWithPositionalEmbedding(nn.Module):
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

        pos_embed = positional_encoding(cfg.max_length, cfg.feature_dim)
        # self.register_buffer('pos_embed', pos_embed)
        self.pos_embed = nn.Parameter(pos_embed)

        self.query_linear = nn.Linear(cfg.feature_dim, self.depth)  # 246 -> 128
        self.key_linear = nn.Linear(cfg.feature_dim, self.depth)
        self.value_linear = nn.Linear(cfg.feature_dim, self.depth)

        self.last_linear = nn.Linear(self.depth, cfg.num_classes)
        self.criterion = nn.CrossEntropyLoss()

    def _split_head(self, x: Tensor) -> Tensor:
        x = x.unsqueeze(1)  # (batch_size, time, emb) -> (batch_size, 1, time, emb)
        # contiguous あってもなくても精度変わらなかったけど念の為
        x = x.contiguous().view(
            x.size(0),
            self.head_num,
            x.size(2),
            self.depth // self.head_num,
        )  # (batch_size, 1, time, emb) -> (batch_size, head_num, time, depth//head_num)
        return x

    def _combine_head(self, x: Tensor) -> Tensor:
        batch_size, _, length, _ = x.size()
        return x.contiguous().view(batch_size, length, self.depth)

    def forward(
        self,
        x: Tensor,  # (batch_size, time, emb)
        attention_mask: Tensor | None,  # (batch_size, time)
    ) -> Tensor:
        # input = memory -> self-attention

        x = x + self.pos_embed
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
        # contiguous あってもなくても精度変わらなかったけど念の為
        x = x.contiguous().view(
            x.size(0),
            self.head_num,
            x.size(2),
            self.depth // self.head_num,
        )  # (batch_size, 1, time, emb) -> (batch_size, head_num, time, depth//head_num)
        return x

    def _combine_head(self, x: Tensor) -> Tensor:
        batch_size, _, length, _ = x.size()
        return x.contiguous().view(batch_size, length, self.depth)

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


class MultiHeadAttentionFromTorchNN(nn.Module):
    """
    not go well
    """

    def __init__(
        self,
        cfg: DictConfig,
    ):
        super().__init__()

        self.cfg = cfg
        self.depth = 128
        self.num_heads = 8
        self.emb = nn.Linear(self.cfg.feature_dim, self.depth)
        self.mha = nn.MultiheadAttention(
            embed_dim=self.depth,
            num_heads=self.num_heads,
            dropout=0.0,
            batch_first=True,
        )
        self.last_linear = nn.Linear(self.depth, self.cfg.num_classes)

    def forward(
        self,
        x: Tensor,  # (batch_size, time, emb)
        attention_mask: Tensor | None,  # (batch_size, time, emb)
    ) -> Tensor:
        if attention_mask is not None:
            attention_mask = attention_mask.repeat(self.num_heads, 1, 1)
        x = self.emb(x)
        attention_output = self.mha(x, x, x, attn_mask=attention_mask)[0]
        output = self.last_linear(attention_output)
        output = output.mean(dim=1)
        return output


class ScaledDotProductAttentionFromZenn(nn.Module):
    def __init__(self, d_k: int) -> None:
        super().__init__()
        self.d_k = d_k

    def forward(
        self,
        q: torch.Tensor,  # =Q
        k: torch.Tensor,  # =X
        v: torch.Tensor,  # =X
        mask: torch.Tensor = None,
    ) -> torch.Tensor:
        scalar = np.sqrt(self.d_k)
        attention_weight = torch.matmul(q, torch.transpose(k, 1, 2)) / scalar  # 「Q * X^T / (D^0.5)」" を計算

        if mask is not None:  # maskに対する処理
            if mask.dim() != attention_weight.dim():
                raise ValueError(
                    "mask.dim != attention_weight.dim, mask.dim={}, attention_weight.dim={}".format(
                        mask.dim(),
                        attention_weight.dim(),
                    ),
                )
            attention_weight = attention_weight.data.masked_fill_(mask, -torch.finfo(torch.float16).max)

        attention_weight = nn.functional.softmax(attention_weight, dim=2)  # Attention weightを計算
        return torch.matmul(attention_weight, v)  # (Attention weight) * X により重み付け.


class MultiHeadAttentionFromZenn(nn.Module):
    """
    from : https://zenn.dev/yukiyada/articles/59f3b820c52571
    not go well
    """

    def __init__(
        self,
        cfg: DictConfig,
    ) -> None:
        super().__init__()

        d_model = cfg.feature_dim
        h = 8

        self.d_model = d_model
        self.h = h
        self.d_k = d_model // h
        self.d_v = d_model // h

        #
        self.W_k = nn.Parameter(
            torch.Tensor(h, d_model, self.d_k),  # ヘッド数, 入力次元, 出力次元(=入力次元/ヘッド数)
        )

        self.W_q = nn.Parameter(
            torch.Tensor(h, d_model, self.d_k),  # ヘッド数, 入力次元, 出力次元(=入力次元/ヘッド数)
        )

        self.W_v = nn.Parameter(
            torch.Tensor(h, d_model, self.d_v),  # ヘッド数, 入力次元, 出力次元(=入力次元/ヘッド数)
        )

        self.scaled_dot_product_attention = ScaledDotProductAttentionFromZenn(self.d_k)

        self.linear = nn.Linear(h * self.d_v, d_model)
        self.last_linear = nn.Linear(d_model, cfg.num_classes)

    def forward(
        self,
        x: torch.Tensor,
        mask_3d: torch.Tensor = None,
    ) -> torch.Tensor:
        # x = self.emb(x)
        q = k = v = x
        batch_size, seq_len = q.size(0), q.size(1)

        """repeat Query,Key,Value by num of heads"""
        q = q.repeat(self.h, 1, 1, 1)  # head, batch_size, seq_len, d_model
        k = k.repeat(self.h, 1, 1, 1)  # head, batch_size, seq_len, d_model
        v = v.repeat(self.h, 1, 1, 1)  # head, batch_size, seq_len, d_model

        """Linear before scaled dot product attention"""
        q = torch.einsum("hijk,hkl->hijl", (q, self.W_q))  # head, batch_size, d_k, seq_len
        k = torch.einsum("hijk,hkl->hijl", (k, self.W_k))  # head, batch_size, d_k, seq_len
        v = torch.einsum("hijk,hkl->hijl", (v, self.W_v))  # head, batch_size, d_k, seq_len

        """Split heads"""
        q = q.view(self.h * batch_size, seq_len, self.d_k)
        k = k.view(self.h * batch_size, seq_len, self.d_k)
        v = v.view(self.h * batch_size, seq_len, self.d_v)

        if mask_3d is not None:
            mask_3d = mask_3d.repeat(self.h, 1, 1)

        """Scaled dot product attention"""
        attention_output = self.scaled_dot_product_attention(q, k, v, mask_3d)  # (head*batch_size, seq_len, d_model)

        attention_output = torch.chunk(attention_output, self.h, dim=0)
        attention_output = torch.cat(attention_output, dim=2)

        """Linear after scaled dot product attention"""
        output = self.linear(attention_output)

        output = self.last_linear(output)
        output = output.mean(dim=1)
        return output
