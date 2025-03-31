"""アプリケーションサービスのテスト"""
import pytest

from src.local_vlm_server.domain.exceptions import InvalidPromptError, VLMModelNotFoundError
from src.local_vlm_server.domain.value_objects import ModelParameters


class TestVLMService:
    """VLMServiceのテスト"""
    
    @pytest.mark.asyncio
    async def test_get_available_models(self, mock_vlm_service, mock_vlm_repository):
        """利用可能なモデル一覧取得のテスト"""
        # モックリポジトリから期待されるモデル一覧
        expected_models = await mock_vlm_repository.get_all_models()
        
        # サービスからモデル一覧を取得
        models = await mock_vlm_service.get_available_models()
        
        # 結果の検証
        assert len(models) == len(expected_models)
        assert all(model in expected_models for model in models)
    
    @pytest.mark.asyncio
    async def test_get_model_by_id_existing(self, mock_vlm_service):
        """存在するモデルIDでのモデル取得テスト"""
        # 存在するモデルIDでモデルを取得
        model = await mock_vlm_service.get_model_by_id("test-model-1")
        
        # 結果の検証
        assert model is not None
        assert model.id == "test-model-1"
        assert model.name == "Test Model 1"
    
    @pytest.mark.asyncio
    async def test_get_model_by_id_nonexistent(self, mock_vlm_service):
        """存在しないモデルIDでのモデル取得テスト"""
        # 存在しないモデルIDでモデルを取得
        model = await mock_vlm_service.get_model_by_id("nonexistent-model")
        
        # 結果の検証
        assert model is None
    
    @pytest.mark.asyncio
    async def test_process_prompt_success(self, mock_vlm_service, mock_vlm_repository):
        """プロンプト処理成功のテスト"""
        # テストデータ
        model_id = "test-model-1"
        prompt_text = "Hello, world!"
        parameters = ModelParameters(temperature=0.5, max_tokens=100)
        
        # プロンプト処理
        response = await mock_vlm_service.process_prompt(
            model_id=model_id,
            prompt_text=prompt_text,
            parameters=parameters
        )
        
        # 結果の検証
        assert response is not None
        assert response.model_id == model_id
        assert response.prompt.text == prompt_text
        assert "Mock response" in response.text
        assert response.tokens_used > 0
        
        # モッククライアントへのリクエスト検証
        client = await mock_vlm_repository.get_client_for_model(model_id)
        assert len(client.requests) == 1
        assert client.requests[0].model_id == model_id
        assert client.requests[0].prompt_text == prompt_text
        assert client.requests[0].parameters == parameters
    
    @pytest.mark.asyncio
    async def test_process_prompt_empty_prompt(self, mock_vlm_service):
        """空プロンプトでの処理テスト"""
        # 空プロンプトでの処理
        with pytest.raises(InvalidPromptError) as excinfo:
            await mock_vlm_service.process_prompt(
                model_id="test-model-1",
                prompt_text=""
            )
        
        # 例外メッセージの検証
        assert "empty" in str(excinfo.value).lower()
    
    @pytest.mark.asyncio
    async def test_process_prompt_nonexistent_model(self, mock_vlm_service):
        """存在しないモデルIDでのプロンプト処理テスト"""
        # 存在しないモデルIDでの処理
        with pytest.raises(VLMModelNotFoundError) as excinfo:
            await mock_vlm_service.process_prompt(
                model_id="nonexistent-model",
                prompt_text="Hello, world!"
            )
        
        # 例外メッセージの検証
        assert "nonexistent-model" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_process_prompt_default_parameters(self, mock_vlm_service, mock_vlm_repository):
        """デフォルトパラメータでのプロンプト処理テスト"""
        # テストデータ
        model_id = "test-model-1"
        prompt_text = "Hello, world!"
        
        # パラメータなしでプロンプト処理
        response = await mock_vlm_service.process_prompt(
            model_id=model_id,
            prompt_text=prompt_text
        )
        
        # 結果の検証
        assert response is not None
        assert response.model_id == model_id
        
        # モッククライアントへのリクエスト検証
        client = await mock_vlm_repository.get_client_for_model(model_id)
        assert len(client.requests) == 1
        # デフォルトパラメータが使用されていることを確認
        assert client.requests[0].parameters is None