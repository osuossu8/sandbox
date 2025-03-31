"""アプリケーションサービスの定義モジュール"""
from typing import List, Optional

from ..domain.entities import Prompt, VLMModel, VLMResponse
from ..domain.exceptions import InvalidPromptError, VLMModelNotFoundError
from ..domain.value_objects import ModelParameters, VLMRequest
from .interfaces import VLMRepositoryInterface


class VLMService:
    """VLMサービスクラス"""
    
    def __init__(self, repository: VLMRepositoryInterface):
        """
        初期化
        
        Args:
            repository: VLMリポジトリ
        """
        self._repository = repository
    
    async def get_available_models(self) -> List[VLMModel]:
        """
        利用可能なすべてのVLMモデルを取得する
        
        Returns:
            VLMモデルのリスト
        """
        return await self._repository.get_all_models()
    
    async def get_model_by_id(self, model_id: str) -> Optional[VLMModel]:
        """
        指定されたIDのVLMモデルを取得する
        
        Args:
            model_id: VLMモデルのID
            
        Returns:
            VLMモデル（存在しない場合はNone）
        """
        return await self._repository.get_model_by_id(model_id)
    
    async def process_prompt(
        self, 
        model_id: str, 
        prompt_text: str, 
        parameters: Optional[ModelParameters] = None
    ) -> VLMResponse:
        """
        プロンプトを処理し、VLMからのレスポンスを取得する
        
        Args:
            model_id: 使用するVLMモデルのID
            prompt_text: プロンプトテキスト
            parameters: モデルパラメータ（オプション）
            
        Returns:
            VLMレスポンス
            
        Raises:
            InvalidPromptError: 無効なプロンプトが指定された場合
            VLMModelNotFoundError: 指定されたモデルが見つからない場合
            VLMConnectionError: VLMとの接続に問題がある場合
            VLMProcessingError: VLMの処理中にエラーが発生した場合
        """
        if not prompt_text or not prompt_text.strip():
            raise InvalidPromptError("Prompt text cannot be empty")
        
        # モデルの存在確認
        model = await self._repository.get_model_by_id(model_id)
        if not model:
            raise VLMModelNotFoundError(model_id)
        
        # クライアントの取得
        client = await self._repository.get_client_for_model(model_id)
        
        # リクエストの作成と送信
        request = VLMRequest(
            prompt_text=prompt_text,
            model_id=model_id,
            parameters=parameters
        )
        
        return await client.generate_response(request)