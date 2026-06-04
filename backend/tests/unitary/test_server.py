from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.main import app

client = TestClient(app)


# Comprobamos la inicialización y lifespan del servidor
def test_server_initialization_and_lifespan():

    response = client.get("/health")
    assert response.status_code == 200


# Comprobamos el endpoint health
def test_health_endpoint_response():

    response = client.get("/health")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["app"] == settings.APP_NAME


# Testeamos la integración del router a la API
def test_api_router_is_included_correctly():

    endpoint_url = f"{settings.API_PREFIX}/pokemon/pikachu"
    response = client.get(endpoint_url)

    assert response.status_code != 404, "El router de la API no está bien configurado"


# Comprobamos la infraestructura CORS
def test_cors_middleware_allows_valid_origins():

    headers = {
        "Origin": "http://localhost:8501",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "content-type",
        "User-Agent": "Mozilla/5.0",
    }

    response = client.options("/health", headers=headers)

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
