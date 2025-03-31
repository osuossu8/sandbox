"""ドメイン例外の定義モジュール"""


class DomainException(Exception):
    """ドメイン層の基底例外クラス"""
    pass


class VLMModelNotFoundError(DomainException):
    """指定されたVLMモデルが見つからない場合の例外"""
    def __init__(self, model_id: str):
        self.model_id = model_id
        super().__init__(f"VLM model with ID '{model_id}' not found")


class VLMConnectionError(DomainException):
    """VLMとの接続に問題がある場合の例外"""
    def __init__(self, model_id: str, details: str = None):
        self.model_id = model_id
        message = f"Failed to connect to VLM model '{model_id}'"
        if details:
            message += f": {details}"
        super().__init__(message)


class InvalidPromptError(DomainException):
    """無効なプロンプトが指定された場合の例外"""
    def __init__(self, reason: str = None):
        message = "Invalid prompt provided"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class VLMProcessingError(DomainException):
    """VLMの処理中にエラーが発生した場合の例外"""
    def __init__(self, model_id: str, details: str = None):
        self.model_id = model_id
        message = f"Error processing request with VLM model '{model_id}'"
        if details:
            message += f": {details}"
        super().__init__(message)