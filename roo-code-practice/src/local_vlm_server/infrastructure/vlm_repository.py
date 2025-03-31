"""VLMリポジトリの実装モジュール"""
import logging
from typing import Dict, List, Optional, Type

from ..application.interfaces import VLMClientInterface, VLMRepositoryInterface
from ..domain.entities import VLMModel
from ..domain.exceptions import VLMModelNotFoundError
from ..infrastructure.vlm_clients.base import BaseVLMClient
from ..infrastructure.vlm_clients.implementations.gpt import GPTVLMClient
from ..infrastructure.vlm_clients.implementations.llama import LlamaVLMClient


logger = logging.getLogger(__name__)


class VLMRepository(VLMRepositoryInterface):
    """VLMリポジトリの実装"""
    
    def __init__(self):
        """初期化"""
        self._models: Dict[str, VLMModel] = {}
        self._client_factories: Dict[str, Type[BaseVLMClient]] = {
            "llama": LlamaVLMClient,
            "gpt": GPTVLMClient,
        }
        self._client_configs: Dict[str, Dict[str, any]] = {}
        self._clients: Dict[str, VLMClientInterface] = {}
        
        # デフォルトモデルの登録
        self._register_default_models()
        
        logger.info(f"Initialized VLMRepository with {len(self._models)} models")
    
    def _register_default_models(self):
        """デフォルトモデルを登録する"""
        # LLaMAモデル
        self._models["llama-7b"] = VLMModel(
            id="llama-7b",
            name="LLaMA 7B",
            description="Meta AI's LLaMA 7B parameter model",
            parameters={
                "context_size": 2048,
                "gpu_layers": 32
            }
        )
        self._client_configs["llama-7b"] = {
            "model_path": "/path/to/llama-7b.bin",
            "context_size": 2048,
            "gpu_layers": 32
        }
        
        # GPTモデル
        self._models["gpt-local"] = VLMModel(
            id="gpt-local",
            name="GPT Local",
            description="Locally hosted GPT compatible model",
            parameters={
                "max_tokens": 4096
            }
        )
        self._client_configs["gpt-local"] = {
            "api_base": "http://localhost:8000",
            "api_key": "dummy-key"
        }
        
        logger.debug(f"Registered default models: {list(self._models.keys())}")
    
    def register_model(
        self, 
        model: VLMModel, 
        client_type: str, 
        config: Dict[str, any]
    ):
        """
        新しいモデルを登録する
        
        Args:
            model: VLMモデル
            client_type: クライアントタイプ（"llama"や"gpt"など）
            config: クライアント設定
        """
        self._models[model.id] = model
        self._client_configs[model.id] = config
        
        # すでにクライアントが作成されている場合は削除
        if model.id in self._clients:
            del self._clients[model.id]
            
        logger.info(f"Registered model {model.id} with client type {client_type}")
    
    async def get_all_models(self) -> List[VLMModel]:
        """
        利用可能なすべてのVLMモデルを取得する
        
        Returns:
            VLMモデルのリスト
        """
        return list(self._models.values())
    
    async def get_model_by_id(self, model_id: str) -> Optional[VLMModel]:
        """
        指定されたIDのVLMモデルを取得する
        
        Args:
            model_id: VLMモデルのID
            
        Returns:
            VLMモデル（存在しない場合はNone）
        """
        return self._models.get(model_id)
    
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
        # モデルの存在確認
        if model_id not in self._models:
            raise VLMModelNotFoundError(model_id)
        
        # クライアントがキャッシュされていればそれを返す
        if model_id in self._clients:
            return self._clients[model_id]
        
        # モデルタイプの判定
        model = self._models[model_id]
        client_type = None
        
        # モデルIDからクライアントタイプを推測
        if "llama" in model_id.lower():
            client_type = "llama"
        elif "gpt" in model_id.lower():
            client_type = "gpt"
        else:
            # デフォルトはLLaMA
            client_type = "llama"
        
        # クライアントファクトリの取得
        if client_type not in self._client_factories:
            logger.warning(f"Unknown client type {client_type}, falling back to llama")
            client_type = "llama"
            
        factory = self._client_factories[client_type]
        
        # クライアント設定の取得
        config = self._client_configs.get(model_id, {})
        
        # クライアントの作成
        client = factory(model_id, config)
        self._clients[model_id] = client
        
        logger.info(f"Created {client_type} client for model {model_id}")
        return client