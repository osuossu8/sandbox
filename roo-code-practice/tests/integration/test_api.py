"""APIの統合テスト"""
import json

import pytest
from fastapi.testclient import TestClient


class TestAPIEndpoints:
    """APIエンドポイントの統合テスト"""
    
    def test_root_endpoint(self, test_client):
        """ルートエンドポイントのテスト"""
        response = test_client.get("/")
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs_url" in data
    
    def test_list_models(self, test_client):
        """モデル一覧取得エンドポイントのテスト"""
        response = test_client.get("/api/v1/models")
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) == 2  # モックリポジトリには2つのモデルがある
        
        # モデルデータの検証
        models = data["models"]
        model_ids = [model["id"] for model in models]
        assert "test-model-1" in model_ids
        assert "test-model-2" in model_ids
    
    def test_get_model_by_id_existing(self, test_client):
        """存在するモデルID取得エンドポイントのテスト"""
        response = test_client.get("/api/v1/models/test-model-1")
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "test-model-1"
        assert data["name"] == "Test Model 1"
    
    def test_get_model_by_id_nonexistent(self, test_client):
        """存在しないモデルID取得エンドポイントのテスト"""
        response = test_client.get("/api/v1/models/nonexistent-model")
        
        # レスポンスの検証
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "ModelNotFound" in data["error"]
    
    def test_generate_text_success(self, test_client):
        """テキスト生成エンドポイント成功のテスト"""
        # リクエストデータ
        request_data = {
            "model_id": "test-model-1",
            "prompt": "Hello, world!",
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        }
        
        # リクエスト送信
        response = test_client.post(
            "/api/v1/generate",
            json=request_data
        )
        
        # レスポンスの検証
        assert response.status_code == 200
        data = response.json()
        assert data["model_id"] == "test-model-1"
        assert data["prompt"] == "Hello, world!"
        assert "text" in data
        assert data["tokens_used"] > 0
        assert "metadata" in data
    
    def test_generate_text_invalid_model(self, test_client):
        """存在しないモデルでのテキスト生成テスト"""
        # リクエストデータ
        request_data = {
            "model_id": "nonexistent-model",
            "prompt": "Hello, world!"
        }
        
        # リクエスト送信
        response = test_client.post(
            "/api/v1/generate",
            json=request_data
        )
        
        # レスポンスの検証
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "ModelNotFound" in data["error"]
    
    def test_generate_text_empty_prompt(self, test_client):
        """空プロンプトでのテキスト生成テスト"""
        # リクエストデータ
        request_data = {
            "model_id": "test-model-1",
            "prompt": ""
        }
        
        # リクエスト送信
        response = test_client.post(
            "/api/v1/generate",
            json=request_data
        )
        
        # レスポンスの検証
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "InvalidPrompt" in data["error"]
    
    def test_generate_text_invalid_parameters(self, test_client):
        """無効なパラメータでのテキスト生成テスト"""
        # リクエストデータ（温度が範囲外）
        request_data = {
            "model_id": "test-model-1",
            "prompt": "Hello, world!",
            "parameters": {
                "temperature": 3.0  # 0.0〜2.0の範囲外
            }
        }
        
        # リクエスト送信
        response = test_client.post(
            "/api/v1/generate",
            json=request_data
        )
        
        # レスポンスの検証
        assert response.status_code == 422  # バリデーションエラー
        data = response.json()
        assert "detail" in data