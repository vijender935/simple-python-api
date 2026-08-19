import os
from threading import Lock

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="Simple Python API",
    description="A clean starter FastAPI project",
    version="1.0.0",
)


# ---------- Models ----------
class Item(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1)
    description: str | None = None
    price: float = Field(ge=0, allow_inf_nan=False)
    is_offer: bool = False


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    is_offer: bool


# In-memory storage (demo only)
items_db: dict[int, dict] = {}
next_id = 1
items_lock = Lock()


# ---------- Endpoints ----------
@app.get("/")
def root():
    return {
        "message": "Welcome to Simple Python API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    global next_id

    with items_lock:
        item_id = next_id
        next_id += 1
        items_db[item_id] = item.model_dump()
        return {"id": item_id, **items_db[item_id]}


@app.get("/items", response_model=list[ItemResponse])
def list_items():
    with items_lock:
        return [{"id": item_id, **item} for item_id, item in items_db.items()]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    with items_lock:
        item = items_db.get(item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"id": item_id, **item}


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    with items_lock:
        if item_id not in items_db:
            raise HTTPException(status_code=404, detail="Item not found")
        items_db[item_id] = item.model_dump()
        return {"id": item_id, **items_db[item_id]}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with items_lock:
        if item_id not in items_db:
            raise HTTPException(status_code=404, detail="Item not found")
        del items_db[item_id]

    return {"message": f"Item {item_id} deleted successfully"}


# ---------- Run ----------
if __name__ == "__main__":
    reload = os.getenv("RELOAD", "").lower() in {"1", "true", "yes"}
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=reload)
