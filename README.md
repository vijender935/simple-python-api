# Simple Python API

Clean FastAPI starter project with basic CRUD endpoints.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docs
- Swagger UI → http://localhost:8000/docs
- ReDoc     → http://localhost:8000/redoc

## Endpoints

| Method | Endpoint          | Description          |
|--------|-------------------|----------------------|
| GET    | `/`               | Welcome message      |
| GET    | `/health`         | Health check         |
| POST   | `/items`          | Create item          |
| GET    | `/items`          | List all items       |
| GET    | `/items/{id}`     | Get single item      |
| PUT    | `/items/{id}`     | Update item          |
| DELETE | `/items/{id}`     | Delete item          |

## Example

```bash
# Create item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Gaming laptop", "price": 999.99, "is_offer": true}'

# List items
curl http://localhost:8000/items
```
