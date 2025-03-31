"""ドメイン値オブジェクトの定義モジュール"""
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional


class VLMType(Enum):
    """VLMの種類を表す列挙型"""
    LLAMA = auto()
    GPT = auto()
    MISTRAL = auto()
    CUSTOM = auto()


@dataclass(frozen=True)
class ModelParameters:
    """モデルパラメータを表す値オブジェクト"""
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    
    def to_dict(self) -> Dict[str, any]:
        """パラメータを辞書形式に変換"""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty
        }


@dataclass(frozen=True)
class VLMRequest:
    """VLMリクエストを表す値オブジェクト"""
    prompt_text: str
    model_id: str
    parameters: Optional[ModelParameters] = None