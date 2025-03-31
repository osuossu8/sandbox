"""アプリケーション層のインターフェース定義モジュール"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..domain.entities import Prompt, VLMModel, VLMResponse
from ..domain.value_objects import ModelParameters, VLMRequest


class VLMClientInterface(ABC):
    """VLMクライアントのインターフェース"""
    
    @abstractmethod
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
        pass


class VLMRepositoryInterface(ABC):
    """VLMモデルリポジトリのインターフェース"""
    
    @abstractmethod
    async def get_all_models(self) -> List[VLMModel]:
        """
        利用可能なすべてのVLMモデルを取得する
        
        Returns:
            VLMモデルのリスト
        """
        pass
    
    @abstractmethod
    async def get_model_by_id(self, model_id: str) -> Optional[VLMModel]:
        """
        指定されたIDのVLMモデルを取得する
        
        Args:
            model_id: VLMモデルのID
            
        Returns:
            VLMモデル（存在しない場合はNone）
        """
        pass
    
    @abstractmethod
    async def get_client_for_model(self, model_id: str) -> VLMClientInterface:
        """
        指定されたモデルIDに対応するVLMクライアントを取得する
        
        Args:
            model_id: VLMモデルのID
            
        Returns:
            VLMクライアント
            
        Raises:
            VLMModelNotFoundError: 指定されたモデルが見つからない場合
        """
        pass