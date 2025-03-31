"""APIルートの定義モジュール"""
import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path

from ...application.services import VLMService
from ...domain.entities import VLMModel
from ...domain.exceptions import (
    DomainException,
    InvalidPromptError,
    VLMConnectionError,
    VLMModelNotFoundError,
    VLMProcessingError,
)
from .dependencies import convert_parameters, get_vlm_service
from .schemas import (
    ErrorResponseSchema,
    ModelsListResponseSchema,
    PromptRequestSchema,
    VLMModelSchema,
    VLMResponseSchema,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["vlm"])


@router.get(
    "/models",
    response_model=ModelsListResponseSchema,
    summary="利用可能なVLMモデルの一覧を取得",
    description="システムで利用可能なすべてのVLMモデルの一覧を返します。",
)
async def list_models(
    service: Annotated[VLMService, Depends(get_vlm_service)]
) -> ModelsListResponseSchema:
    """
    利用可能なVLMモデルの一覧を取得する
    
    Args:
        service: VLMサービス
        
    Returns:
        モデル一覧レスポンス
    """
    try:
        models = await service.get_available_models()
        return ModelsListResponseSchema(
            models=[
                VLMModelSchema(
                    id=model.id,
                    name=model.name,
                    description=model.description,
                    parameters=model.parameters
                )
                for model in models
            ]
        )
    except Exception as e:
        logger.exception("Error listing models")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponseSchema(
                error="InternalServerError",
                message="Failed to retrieve models",
                details={"error": str(e)}
            ).dict()
        )


@router.get(
    "/models/{model_id}",
    response_model=VLMModelSchema,
    summary="特定のVLMモデルの詳細を取得",
    description="指定されたIDのVLMモデルの詳細情報を返します。",
)
async def get_model(
    model_id: Annotated[str, Path(description="VLMモデルのID")],
    service: Annotated[VLMService, Depends(get_vlm_service)]
) -> VLMModelSchema:
    """
    特定のVLMモデルの詳細を取得する
    
    Args:
        model_id: VLMモデルのID
        service: VLMサービス
        
    Returns:
        モデルスキーマ
        
    Raises:
        HTTPException: モデルが見つからない場合
    """
    try:
        model = await service.get_model_by_id(model_id)
        if not model:
            raise HTTPException(
                status_code=404,
                detail=ErrorResponseSchema(
                    error="ModelNotFound",
                    message=f"Model with ID '{model_id}' not found",
                ).dict()
            )
        
        return VLMModelSchema(
            id=model.id,
            name=model.name,
            description=model.description,
            parameters=model.parameters
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error retrieving model {model_id}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponseSchema(
                error="InternalServerError",
                message=f"Failed to retrieve model {model_id}",
                details={"error": str(e)}
            ).dict()
        )


@router.post(
    "/generate",
    response_model=VLMResponseSchema,
    summary="VLMを使用してテキストを生成",
    description="指定されたモデルとプロンプトを使用してテキストを生成します。",
)
async def generate_text(
    request: PromptRequestSchema,
    service: Annotated[VLMService, Depends(get_vlm_service)]
) -> VLMResponseSchema:
    """
    VLMを使用してテキストを生成する
    
    Args:
        request: プロンプトリクエスト
        service: VLMサービス
        
    Returns:
        VLMレスポンス
        
    Raises:
        HTTPException: リクエスト処理中にエラーが発生した場合
    """
    try:
        # パラメータの変換
        parameters = convert_parameters(request.parameters)
        
        # プロンプト処理
        response = await service.process_prompt(
            model_id=request.model_id,
            prompt_text=request.prompt,
            parameters=parameters
        )
        
        return VLMResponseSchema(
            model_id=response.model_id,
            prompt=response.prompt.text,
            text=response.text,
            tokens_used=response.tokens_used,
            metadata=response.metadata
        )
        
    except VLMModelNotFoundError as e:
        logger.warning(f"Model not found: {e}")
        raise HTTPException(
            status_code=404,
            detail=ErrorResponseSchema(
                error="ModelNotFound",
                message=str(e)
            ).dict()
        )
    except InvalidPromptError as e:
        logger.warning(f"Invalid prompt: {e}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseSchema(
                error="InvalidPrompt",
                message=str(e)
            ).dict()
        )
    except VLMConnectionError as e:
        logger.error(f"VLM connection error: {e}")
        raise HTTPException(
            status_code=503,
            detail=ErrorResponseSchema(
                error="VLMConnectionError",
                message=str(e)
            ).dict()
        )
    except VLMProcessingError as e:
        logger.error(f"VLM processing error: {e}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponseSchema(
                error="VLMProcessingError",
                message=str(e)
            ).dict()
        )
    except DomainException as e:
        logger.error(f"Domain error: {e}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponseSchema(
                error="DomainError",
                message=str(e)
            ).dict()
        )
    except Exception as e:
        logger.exception("Unexpected error during text generation")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponseSchema(
                error="InternalServerError",
                message="An unexpected error occurred",
                details={"error": str(e)}
            ).dict()
        )