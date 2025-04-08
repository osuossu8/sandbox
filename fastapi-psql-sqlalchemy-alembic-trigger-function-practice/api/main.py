import uvicorn
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI()


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1111)
