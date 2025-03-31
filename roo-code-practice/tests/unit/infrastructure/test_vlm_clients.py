"""VLMクライアントのテスト"""
import pytest

from src.local_vlm_server.domain.exceptions import VLMProcessingError
from src.local_vlm_server.domain.value_objects import ModelParameters, VLMRequest
from src.local_vlm_server.infrastructure.vlm_clients.implementations.gpt import GPTVLMClient
from src.local_vlm_server.infrastructure.vlm_clients.implementations.llama import LlamaVLMClient


class TestLlamaVLMClient:
    """LlamaVLMClientのテスト"""
    
    @pytest.fixture
    def llama_client(self):
        """LlamaVLMClientのフィクスチャ"""
        return LlamaVLMClient(
            model_id="test-llama",
            config={
                "model_path": "/path/to/model.bin",
                "context_size": 2048,
                "gpu_layers": 32
            }
        )
    
    @pytest.mark.asyncio
    async def test_initialization(self, llama_client):
        """初期化のテスト"""
        assert llama_client.model_id == "test-llama"
        assert llama_client.model_path == "/path/to/model.bin"
        assert llama_client.context_size == 2048
        assert llama_client.gpu_layers == 32
    
    @pytest.mark.asyncio
    async def test_generate_response(self, llama_client):
        """レスポンス生成のテスト"""
        # テストリクエスト
        request = VLMRequest(
            prompt_text="Hello, world!",
            model_id="test-llama",
            parameters=ModelParameters(temperature=0.7, max_tokens=100)
        )
        
        # レスポンス生成
        response = await llama_client.generate_response(request)
        
        # 結果の検証
        assert response is not None
        assert response.model_id == "test-llama"
        assert response.prompt.text == "Hello, world!"
        assert len(response.text) > 0
        assert response.tokens_used > 0
        assert response.metadata is not None
    
    @pytest.mark.asyncio
    async def test_generate_response_with_greeting(self, llama_client):
        """挨拶プロンプトでのレスポンス生成テスト"""
        # 挨拶プロンプト
        request = VLMRequest(
            prompt_text="こんにちは",
            model_id="test-llama"
        )
        
        # レスポンス生成
        response = await llama_client.generate_response(request)
        
        # 結果の検証
        assert "こんにちは" in response.text
        assert "LLaMA" in response.text


class TestGPTVLMClient:
    """GPTVLMClientのテスト"""
    
    @pytest.fixture
    def gpt_client(self):
        """GPTVLMClientのフィクスチャ"""
        return GPTVLMClient(
            model_id="test-gpt",
            config={
                "api_base": "http://localhost:8000",
                "api_key": "test-key"
            }
        )
    
    @pytest.mark.asyncio
    async def test_initialization(self, gpt_client):
        """初期化のテスト"""
        assert gpt_client.model_id == "test-gpt"
        assert gpt_client.api_base == "http://localhost:8000"
        assert gpt_client.api_key == "test-key"
    
    @pytest.mark.asyncio
    async def test_generate_response(self, gpt_client):
        """レスポンス生成のテスト"""
        # テストリクエスト
        request = VLMRequest(
            prompt_text="Hello, world!",
            model_id="test-gpt",
            parameters=ModelParameters(temperature=0.7, max_tokens=100)
        )
        
        # レスポンス生成
        response = await gpt_client.generate_response(request)
        
        # 結果の検証
        assert response is not None
        assert response.model_id == "test-gpt"
        assert response.prompt.text == "Hello, world!"
        assert len(response.text) > 0
        assert response.tokens_used > 0
        assert response.metadata is not None
        assert response.metadata.get("model") == "test-gpt"
        assert response.metadata.get("temperature") == 0.7
    
    @pytest.mark.asyncio
    async def test_generate_response_with_help(self, gpt_client):
        """ヘルププロンプトでのレスポンス生成テスト"""
        # ヘルププロンプト
        request = VLMRequest(
            prompt_text="助けて",
            model_id="test-gpt"
        )
        
        # レスポンス生成
        response = await gpt_client.generate_response(request)
        
        # 結果の検証
        assert "お困り" in response.text or "助け" in response.text