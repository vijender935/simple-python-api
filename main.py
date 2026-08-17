from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(
    title="Simple Python API",
    description="A clean starter FastAPI project",
    version="1.0.0"
)

# ---------- Models ----------
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_offer: Optional[bool] = False

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    is_offer: bool

# In-memory storage (demo only)
items_db = {}
next_id = 1

# ---------- Endpoints ----------
@app.get("/")
def root():
    return {
        "message": "Welcome to Simple Python API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    global next_id
    item_id = next_id
    next_id += 1
    items_db[item_id] = item.model_dump()
    return {"id": item_id, **items_db[item_id]}

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id]}

@app.get("/items")
def list_items():
    return [{"id": k, **v} for k, v in items_db.items()]

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.model_dump()
    return {"id": item_id, **items_db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}

# ---------- Run ----------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
