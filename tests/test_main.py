from fastapi.testclient import TestClient
from fastapi import Response
from main import app

client = TestClient(app=app)

def test_get_products():
    response: Response = client.get("/products")

    assert response.status_code == 200