"""FastAPIメインアプリケーションモジュール"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..domain.exceptions import DomainException
from .api.routes import router as api_router


# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフスパン管理
    
    Args:
        app: FastAPIアプリケーション
    """
    # 起動時の処理
    logger.info("Starting Local VLM Server")
    
    yield
    
    # シャットダウン時の処理
    logger.info("Shutting down Local VLM Server")


# FastAPIアプリケーションの作成
app = FastAPI(
    title="Local VLM Server",
    description="複数のローカルVLMとプロンプトを引数にとり、引数に応じて別のVLMを呼び出すWebAPI",
    version="0.1.0",
    lifespan=lifespan,
)

# CORSミドルウェアの追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(api_router)


# ルートエンドポイント
@app.get("/", tags=["root"])
async def root():
    """
    ルートエンドポイント
    
    Returns:
        サーバー情報
    """
    return {
        "name": "Local VLM Server",
        "version": "0.1.0",
        "description": "複数のローカルVLMとプロンプトを引数にとり、引数に応じて別のVLMを呼び出すWebAPI",
        "docs_url": "/docs",
    }


# 例外ハンドラー
@app.exception_handler(DomainException)
async def domain_exception_handler(request, exc):
    """
    ドメイン例外ハンドラー
    
    Args:
        request: リクエスト
        exc: 例外
        
    Returns:
        JSONレスポンス
    """
    logger.warning(f"Domain exception: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc),
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    # 開発サーバーの起動
    uvicorn.run(
        "src.local_vlm_server.interface.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )