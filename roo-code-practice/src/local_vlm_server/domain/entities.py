"""ドメインエンティティの定義モジュール"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class VLMModel:
    """VLMモデルを表すエンティティ"""
    id: str
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, any]] = None
    
    def __eq__(self, other):
        if not isinstance(other, VLMModel):
            return False
        return self.id == other.id


@dataclass
class Prompt:
    """プロンプトを表すエンティティ"""
    text: str
    parameters: Optional[Dict[str, any]] = None


@dataclass
class VLMResponse:
    """VLMからのレスポンスを表すエンティティ"""
    model_id: str
    prompt: Prompt
    text: str
    tokens_used: int
    metadata: Optional[Dict[str, any]] = None