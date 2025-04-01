from typing import Any

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None) -> dict[str, Any]:
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1234)
