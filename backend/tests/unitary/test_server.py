from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.main import app

client = TestClient(app)


def test_server_initialization_and_lifespan():
    """Este test comprueba la inicialización correcta del servidor"""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_response():
    """Este test comprueba la respuesta del endpoint health"""
    response = client.get("/health")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["app"] == settings.APP_NAME


def test_api_router_is_included_correctly():
    """Este test comprueba si se incluye correctamente el router a la API"""
    endpoint_url = f"{settings.API_PREFIX}/pokemon/pikachu"
    response = client.get(endpoint_url)

    assert response.status_code != 404, "El router de la API no está bien configurado"


def test_cors_middleware_allows_valid_origins():
    """Este test comprueba la infraestructura CORS"""
    headers = {
        "Origin": "http://localhost:8501",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "content-type",
        "User-Agent": "Mozilla/5.0",
    }

    response = client.options("/health", headers=headers)

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
