import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


def create_app() -> FastAPI:
    return FastAPI()


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1111)