"""VLMクライアントの基底クラス定義モジュール"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Optional

from ...application.interfaces import VLMClientInterface
from ...domain.entities import Prompt, VLMResponse
from ...domain.exceptions import VLMConnectionError, VLMProcessingError
from ...domain.value_objects import ModelParameters, VLMRequest


logger = logging.getLogger(__name__)


class BaseVLMClient(VLMClientInterface, ABC):
    """VLMクライアントの基底クラス"""
    
    def __init__(self, model_id: str, config: Optional[Dict[str, any]] = None):
        """
        初期化
        
        Args:
            model_id: VLMモデルのID
            config: クライアント設定（オプション）
        """
        self.model_id = model_id
        self.config = config or {}
        logger.info(f"Initialized {self.__class__.__name__} for model {model_id}")
    
    @abstractmethod
    async def _execute_request(self, request: VLMRequest) -> Dict[str, any]:
        """
        実際のVLMリクエストを実行する
        
        Args:
            request: VLMリクエスト
            
        Returns:
            レスポンスデータの辞書
            
        Raises:
            VLMConnectionError: VLMとの接続に問題がある場合
            VLMProcessingError: VLMの処理中にエラーが発生した場合
        """
        pass
    
    async def generate_response(self, request: VLMRequest) -> VLMResponse:
        """
        VLMにリクエストを送信し、レスポンスを生成する
        
        Args:
            request: VLMリクエスト
            
        Returns:
            VLMレスポンス
            
        Raises:
            VLMConnectionError: VLMとの接続に問題がある場合
            VLMProcessingError: VLMの処理中にエラーが発生した場合
        """
        try:
            logger.debug(f"Sending request to {self.model_id}: {request.prompt_text[:50]}...")
            
            # パラメータの準備
            parameters = request.parameters or ModelParameters()
            
            # リクエストの実行
            response_data = await self._execute_request(request)
            
            # レスポンスの作成
            prompt = Prompt(text=request.prompt_text)
            response = VLMResponse(
                model_id=self.model_id,
                prompt=prompt,
                text=response_data.get("text", ""),
                tokens_used=response_data.get("tokens_used", 0),
                metadata=response_data.get("metadata")
            )
            
            logger.debug(f"Received response from {self.model_id}: {response.text[:50]}...")
            return response
            
        except VLMConnectionError as e:
            logger.error(f"Connection error with {self.model_id}: {str(e)}")
            raise
        except VLMProcessingError as e:
            logger.error(f"Processing error with {self.model_id}: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error with {self.model_id}")
            raise VLMProcessingError(self.model_id, str(e))