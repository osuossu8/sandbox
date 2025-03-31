"""ドメインエンティティのテスト"""
import pytest

from src.local_vlm_server.domain.entities import Prompt, VLMModel, VLMResponse


class TestVLMModel:
    """VLMModelエンティティのテスト"""
    
    def test_create_vlm_model(self):
        """VLMModelの作成テスト"""
        # 基本的な作成
        model = VLMModel(id="test-model", name="Test Model")
        assert model.id == "test-model"
        assert model.name == "Test Model"
        assert model.description is None
        assert model.parameters is None
        
        # すべてのフィールドを指定
        model = VLMModel(
            id="test-model-2",
            name="Test Model 2",
            description="A test model",
            parameters={"temperature": 0.7}
        )
        assert model.id == "test-model-2"
        assert model.name == "Test Model 2"
        assert model.description == "A test model"
        assert model.parameters == {"temperature": 0.7}
    
    def test_vlm_model_equality(self):
        """VLMModelの等価性テスト"""
        model1 = VLMModel(id="test-model", name="Test Model")
        model2 = VLMModel(id="test-model", name="Different Name")
        model3 = VLMModel(id="different-id", name="Test Model")
        
        # 同じIDなら等価
        assert model1 == model2
        # 異なるIDなら非等価
        assert model1 != model3
        # 異なる型なら非等価
        assert model1 != "test-model"


class TestPrompt:
    """Promptエンティティのテスト"""
    
    def test_create_prompt(self):
        """Promptの作成テスト"""
        # 基本的な作成
        prompt = Prompt(text="Hello, world!")
        assert prompt.text == "Hello, world!"
        assert prompt.parameters is None
        
        # パラメータ付きの作成
        prompt = Prompt(
            text="Hello, world!",
            parameters={"temperature": 0.7}
        )
        assert prompt.text == "Hello, world!"
        assert prompt.parameters == {"temperature": 0.7}


class TestVLMResponse:
    """VLMResponseエンティティのテスト"""
    
    def test_create_vlm_response(self):
        """VLMResponseの作成テスト"""
        # 基本的な作成
        prompt = Prompt(text="Hello, world!")
        response = VLMResponse(
            model_id="test-model",
            prompt=prompt,
            text="Hello, human!",
            tokens_used=10
        )
        assert response.model_id == "test-model"
        assert response.prompt == prompt
        assert response.text == "Hello, human!"
        assert response.tokens_used == 10
        assert response.metadata is None
        
        # メタデータ付きの作成
        response = VLMResponse(
            model_id="test-model",
            prompt=prompt,
            text="Hello, human!",
            tokens_used=10,
            metadata={"finish_reason": "stop"}
        )
        assert response.model_id == "test-model"
        assert response.prompt == prompt
        assert response.text == "Hello, human!"
        assert response.tokens_used == 10
        assert response.metadata == {"finish_reason": "stop"}