from fastapi.testclient import TestClient

from backend.app.core.config import Settings, settings
from backend.main import app

client = TestClient(app)


# Comprobamos el microservicio responda correctamente en su ruta de infraestructura
def test_health_e2e():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["app"] == settings.APP_NAME


# Comprobamos la raíz de la api
def test_root():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Pokedex API -FastAPI core running"


# Comprobamos los metodos permitidos por CORS
def test_cors_allows_explicit_whitelisted_methods():
    headers = {
        "Origin": "http://localhost:8501",
        "Access-Control-Request-Method": "POST",
    }
    response = client.options("/health", headers=headers)

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

    allowed_methods = response.headers.get("access-control-allow-methods", "")
    assert "GET" in allowed_methods
    assert "POST" in allowed_methods
    assert "PUT" in allowed_methods
    assert "DELETE" in allowed_methods
    assert "PATCH" in allowed_methods
    assert "OPTIONS" in allowed_methods


# Comprobamos que no se aceptan metodos que no están en la lista autorizada
def test_cors_rejects_non_whitelisted_methods():
    # Comprobamos con TRACE un metodo peligroso para ataques Cross-Site Tracking
    headers = {
        "Origin": "http://localhost:8501",
        "Access-Control-Request-Method": "TRACE",
    }

    response = client.options("/health", headers=headers)

    # El middleware de FastAPI rechaza la petición con un 400 Bad Request
    assert response.status_code == 400


def test_assemble_cors_origins_from_string():
    # Simulamos que llega un string como en GitHub Actions
    settings = Settings(ALLOWED_ORIGINS="http://localhost:8501, http://localhost:3000")

    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:8501",
        "http://localhost:3000",
    ]


def test_assemble_cors_origins_empty_string():
    # Simulamos un string vacío
    settings = Settings(ALLOWED_ORIGINS="")
    assert settings.ALLOWED_ORIGINS == []


def test_assemble_cors_origins_fallback():
    # Simulamos que llega algo muy diferente como un entero para probar el fallback
    settings = Settings(ALLOWED_ORIGINS=12345)
    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:8501",
        "http://localhost:3000",
    ]
