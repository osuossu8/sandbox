"""APIスキーマの定義モジュール"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ModelParametersSchema(BaseModel):
    """モデルパラメータのスキーマ"""
    temperature: float = Field(0.7, description="生成時の温度パラメータ", ge=0.0, le=2.0)
    max_tokens: int = Field(1024, description="生成する最大トークン数", gt=0)
    top_p: float = Field(1.0, description="トップPサンプリングの値", ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, description="頻度ペナルティ", ge=0.0, le=2.0)
    presence_penalty: float = Field(0.0, description="存在ペナルティ", ge=0.0, le=2.0)


class VLMModelSchema(BaseModel):
    """VLMモデルのスキーマ"""
    id: str = Field(..., description="モデルID")
    name: str = Field(..., description="モデル名")
    description: Optional[str] = Field(None, description="モデルの説明")
    parameters: Optional[Dict[str, any]] = Field(None, description="モデルのパラメータ")


class PromptRequestSchema(BaseModel):
    """プロンプトリクエストのスキーマ"""
    model_id: str = Field(..., description="使用するVLMモデルのID")
    prompt: str = Field(..., description="プロンプトテキスト")
    parameters: Optional[ModelParametersSchema] = Field(None, description="モデルパラメータ")


class VLMResponseSchema(BaseModel):
    """VLMレスポンスのスキーマ"""
    model_id: str = Field(..., description="使用したVLMモデルのID")
    prompt: str = Field(..., description="入力プロンプト")
    text: str = Field(..., description="生成されたテキスト")
    tokens_used: int = Field(..., description="使用されたトークン数")
    metadata: Optional[Dict[str, any]] = Field(None, description="レスポンスのメタデータ")


class ErrorResponseSchema(BaseModel):
    """エラーレスポンスのスキーマ"""
    error: str = Field(..., description="エラータイプ")
    message: str = Field(..., description="エラーメッセージ")
    details: Optional[Dict[str, any]] = Field(None, description="エラーの詳細情報")


class ModelsListResponseSchema(BaseModel):
    """モデル一覧レスポンスのスキーマ"""
    models: List[VLMModelSchema] = Field(..., description="利用可能なモデルのリスト")