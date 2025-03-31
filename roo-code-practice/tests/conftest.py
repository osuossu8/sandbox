"""pytest設定ファイル"""
import asyncio
from typing import Dict, List, Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.local_vlm_server.application.interfaces import VLMClientInterface, VLMRepositoryInterface
from src.local_vlm_server.application.services import VLMService
from src.local_vlm_server.domain.entities import Prompt, VLMModel, VLMResponse
from src.local_vlm_server.domain.exceptions import VLMModelNotFoundError
from src.local_vlm_server.domain.value_objects import VLMRequest
from src.local_vlm_server.interface.main import app as main_app


# モックVLMクライアント
class MockVLMClient(VLMClientInterface):
    """テスト用のモックVLMクライアント"""
    
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.requests: List[VLMRequest] = []
    
    async def generate_response(self, request: VLMRequest) -> VLMResponse:
        """モックレスポンスを生成する"""
        self.requests.append(request)
        
        # モックレスポンスの生成
        prompt = Prompt(text=request.prompt_text)
        return VLMResponse(
            model_id=self.model_id,
            prompt=prompt,
            text=f"Mock response from {self.model_id} for prompt: {request.prompt_text[:20]}...",
            tokens_used=len(request.prompt_text) // 4,
            metadata={"mock": True}
        )


# モックVLMリポジトリ
class MockVLMRepository(VLMRepositoryInterface):
    """テスト用のモックVLMリポジトリ"""
    
    def __init__(self):
        self.models: Dict[str, VLMModel] = {
            "test-model-1": VLMModel(
                id="test-model-1",
                name="Test Model 1",
                description="A test model"
            ),
            "test-model-2": VLMModel(
                id="test-model-2",
                name="Test Model 2",
                description="Another test model"
            )
        }
        self.clients: Dict[str, VLMClientInterface] = {
            model_id: MockVLMClient(model_id)
            for model_id in self.models
        }
    
    async def get_all_models(self) -> List[VLMModel]:
        """すべてのモデルを取得する"""
        return list(self.models.values())
    
    async def get_model_by_id(self, model_id: str) -> Optional[VLMModel]:
        """指定されたIDのモデルを取得する"""
        return self.models.get(model_id)
    
    async def get_client_for_model(self, model_id: str) -> VLMClientInterface:
        """指定されたモデルIDに対応するクライアントを取得する"""
        if model_id not in self.models:
            raise VLMModelNotFoundError(model_id)
        return self.clients[model_id]


@pytest.fixture
def mock_vlm_repository():
    """モックVLMリポジトリのフィクスチャ"""
    return MockVLMRepository()


@pytest.fixture
def mock_vlm_service(mock_vlm_repository):
    """モックVLMサービスのフィクスチャ"""
    return VLMService(mock_vlm_repository)


@pytest.fixture
def test_app(mock_vlm_repository, monkeypatch):
    """テスト用アプリケーションのフィクスチャ"""
    # 依存関係の注入をモックに置き換え
    from src.local_vlm_server.interface.api.dependencies import get_vlm_repository
    
    async def mock_get_vlm_repository():
        return mock_vlm_repository
    
    monkeypatch.setattr(
        "src.local_vlm_server.interface.api.dependencies.get_vlm_repository",
        mock_get_vlm_repository
    )
    
    return main_app


@pytest.fixture
def test_client(test_app):
    """テストクライアントのフィクスチャ"""
    return TestClient(test_app)


# asyncioのイベントループフィクスチャ
@pytest.fixture
def event_loop():
    """asyncioイベントループのフィクスチャ"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()