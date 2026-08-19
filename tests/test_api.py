from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def reset_db():
    main.items_db.clear()
    main.next_id = 1


def setup_function():
    reset_db()


def test_root_and_health():
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "healthy"


def test_create_and_get_item():
    response = client.post(
        "/items",
        json={"name": "Laptop", "description": "Test", "price": 999.99},
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["is_offer"] is False

    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_null_is_offer_is_rejected():
    response = client.post(
        "/items",
        json={"name": "Laptop", "price": 10, "is_offer": None},
    )
    assert response.status_code == 422


def test_invalid_price_is_rejected():
    response = client.post(
        "/items",
        json={"name": "Laptop", "price": -1},
    )
    assert response.status_code == 422


def test_missing_item_returns_404():
    assert client.get("/items/999").status_code == 404
    assert client.put("/items/999", json={"name": "x", "price": 1}).status_code == 404
    assert client.delete("/items/999").status_code == 404


def test_update_list_and_delete():
    created = client.post("/items", json={"name": "A", "price": 10})
    assert created.status_code == 201

    updated = client.put("/items/1", json={"name": "B", "price": 20, "is_offer": True})
    assert updated.status_code == 200
    assert updated.json()["name"] == "B"
    assert updated.json()["is_offer"] is True

    listed = client.get("/items")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["id"] == 1

    deleted = client.delete("/items/1")
    assert deleted.status_code == 200
    assert client.get("/items/1").status_code == 404
