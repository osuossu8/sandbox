"""API依存関係の定義モジュール"""
import logging
from typing import Annotated

from fastapi import Depends

from ...application.services import VLMService
from ...domain.value_objects import ModelParameters
from ...infrastructure.vlm_repository import VLMRepository
from .schemas import ModelParametersSchema


logger = logging.getLogger(__name__)


# シングルトンインスタンス
_vlm_repository = None
_vlm_service = None


def get_vlm_repository() -> VLMRepository:
    """
    VLMリポジトリのシングルトンインスタンスを取得する
    
    Returns:
        VLMリポジトリ
    """
    global _vlm_repository
    if _vlm_repository is None:
        logger.info("Creating VLMRepository instance")
        _vlm_repository = VLMRepository()
    return _vlm_repository


def get_vlm_service(
    repository: Annotated[VLMRepository, Depends(get_vlm_repository)]
) -> VLMService:
    """
    VLMサービスのシングルトンインスタンスを取得する
    
    Args:
        repository: VLMリポジトリ
        
    Returns:
        VLMサービス
    """
    global _vlm_service
    if _vlm_service is None:
        logger.info("Creating VLMService instance")
        _vlm_service = VLMService(repository)
    return _vlm_service


def convert_parameters(
    parameters: ModelParametersSchema = None
) -> ModelParameters:
    """
    APIスキーマのパラメータをドメインモデルのパラメータに変換する
    
    Args:
        parameters: APIスキーマのパラメータ
        
    Returns:
        ドメインモデルのパラメータ
    """
    if parameters is None:
        return ModelParameters()
    
    return ModelParameters(
        temperature=parameters.temperature,
        max_tokens=parameters.max_tokens,
        top_p=parameters.top_p,
        frequency_penalty=parameters.frequency_penalty,
        presence_penalty=parameters.presence_penalty
    )