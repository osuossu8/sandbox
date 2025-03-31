"""GPT VLMクライアントの実装モジュール"""
import asyncio
import logging
from typing import Dict, Optional

from ....domain.exceptions import VLMConnectionError, VLMProcessingError
from ....domain.value_objects import VLMRequest
from ..base import BaseVLMClient


logger = logging.getLogger(__name__)


class GPTVLMClient(BaseVLMClient):
    """GPT VLMクライアント"""
    
    def __init__(self, model_id: str, config: Optional[Dict[str, any]] = None):
        """
        初期化
        
        Args:
            model_id: VLMモデルのID
            config: クライアント設定（オプション）
                - api_base: APIのベースURL
                - api_key: APIキー
        """
        super().__init__(model_id, config)
        self.api_base = self.config.get("api_base", "http://localhost:8000")
        self.api_key = self.config.get("api_key")
        
        # 実際の実装では、ここでHTTPクライアントを初期化する
        # self.client = httpx.AsyncClient(...)
        self.client = None
        logger.info(f"Initialized GPTVLMClient for model {model_id}")
    
    async def _execute_request(self, request: VLMRequest) -> Dict[str, any]:
        """
        GPTモデルにリクエストを実行する
        
        Args:
            request: VLMリクエスト
            
        Returns:
            レスポンスデータの辞書
            
        Raises:
            VLMConnectionError: VLMとの接続に問題がある場合
            VLMProcessingError: VLMの処理中にエラーが発生した場合
        """
        try:
            # 実際の実装では、ここでAPIにリクエストを送信する
            # response = await self.client.post(...)
            
            # モックの実装（実際のAPI呼び出しの代わり）
            logger.debug(f"Executing request to GPT model {self.model_id}")
            
            # 非同期処理をシミュレート
            await asyncio.sleep(0.3)
            
            # モックレスポンスの生成
            parameters = request.parameters
            max_tokens = parameters.max_tokens if parameters else 1024
            temperature = parameters.temperature if parameters else 0.7
            
            # プロンプトに基づいた簡単なレスポンス生成
            prompt_lower = request.prompt_text.lower()
            if "hello" in prompt_lower or "こんにちは" in prompt_lower:
                response_text = "こんにちは！GPTモデルです。どのようにお手伝いできますか？"
            elif "help" in prompt_lower or "助けて" in prompt_lower:
                response_text = "どのようなことでお困りですか？具体的に教えていただければ、お手伝いします。"
            else:
                response_text = f"あなたのプロンプト「{request.prompt_text[:30]}...」を受け取りました。GPTモデルからの応答です。"
            
            # トークン数の計算（実際には文字数÷4程度）
            tokens_used = len(response_text) // 4
            
            return {
                "text": response_text,
                "tokens_used": tokens_used,
                "metadata": {
                    "model": self.model_id,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "finish_reason": "stop"
                }
            }
            
        except Exception as e:
            logger.exception(f"Error executing request to GPT model {self.model_id}")
            if "Connection" in str(e):
                raise VLMConnectionError(self.model_id, str(e))
            else:
                raise VLMProcessingError(self.model_id, str(e))