"""
En este set de tests comprobamos la infraestructura base del backend
"""

from fastapi.testclient import TestClient

from backend.app.core.config import Settings, settings
from backend.main import app

client = TestClient(app)


def test_health_e2e():
    """Este test comprueba que el endpoint health responda un 200 Ok
    si se levante correctamente el servidor"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["app"] == settings.APP_NAME


def test_root():
    """Este test comprueba que la raíz de la API lanza un 200 Ok"""
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Pokedex API -FastAPI core running"


def test_cors_allows_explicit_whitelisted_methods():
    """Este test comprueba que CORS admite unicamente los métodos permitidos"""
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


def test_cors_rejects_non_whitelisted_methods():
    """Es test comprueba que no se aceptan metodos que no están en la
    lista autorizada"""
    # Comprobamos con TRACE un metodo peligroso para ataques Cross-Site Tracking
    headers = {
        "Origin": "http://localhost:8501",
        "Access-Control-Request-Method": "TRACE",
    }

    response = client.options("/health", headers=headers)

    # El middleware de FastAPI rechaza la petición con un 400 Bad Request
    assert response.status_code == 400


def test_assemble_cors_origins_from_string():
    """Este test comprueba que Pydantic construye correctamente los origenes permitidos,
    ya que allowed origins en la configuración acepta unicamente listas"""
    # Simulamos que llegan las configuraciones como en GitHub Actions,
    # en donde las variables de entorno llegan en str (texto plano)
    settings = Settings(ALLOWED_ORIGINS="http://localhost:8501, http://localhost:3000")

    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:8501",
        "http://localhost:3000",
    ]


def test_assemble_cors_origins_empty_string():
    """Este test comprueba que Pydantic devuelve una lista con el fallback, en caso de
    que en un entorno de producción se eliminen los origenes permitidos, sin romper el
    levantamiento del servidor"""
    settings = Settings(ALLOWED_ORIGINS="")
    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:8501",
        "http://localhost:3000",
    ]


def test_assemble_cors_origins_fallback():
    """Este test comprueba que si se ingresa una URL erronea, se use el fallback seguro,
    asignando por defecto las URLs seguras del entorno local"""
    settings = Settings(ALLOWED_ORIGINS="12345")
    assert settings.ALLOWED_ORIGINS == [
        "http://localhost:8501",
        "http://localhost:3000",
    ]
