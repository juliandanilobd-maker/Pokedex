from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


# Creamos un test para probar el endpoint health
def test_health():

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
