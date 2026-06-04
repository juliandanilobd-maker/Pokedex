import contextlib
import os
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.main import app

functional_client = TestClient(app)


# Establecemos el uso de una base de datos aislada para cache
@pytest.fixture(scope="module", autouse=True)
def setup_functional_enviroment(monkeypatch_module):

    os.makedirs("data", exist_ok=True)
    # Creamos un archivo unicamente para pruebas E2E
    test_db_path = "data/functional_test_cache.db"

    # Aseguramos el uso de un archivo de base de datos de cache
    monkeypatch_module.setenv("CACHE_DB_PATH", test_db_path)

    yield

    # Establecemos que se limpie el archivo al terminar los tests
    if os.path.exists(test_db_path):
        os.remove(settings.CACHE_DB_PATH)
    contextlib.suppress(PermissionError)


# Establecemos el flujo real E2E, una petición real a PokeAPI y almacenamiento en cache
def test_e2e_pokemon_flow_with_real_cache():

    # Realizamos la primera petición directa a la PokeAPI
    start_time_api = time.time()
    response_1 = functional_client.get("/api/v1/pokemon/ditto")
    duration_api = time.time() - start_time_api

    assert response_1.status_code == 200

    data_1 = response_1.json()

    assert data_1["name"] == "ditto"
    assert "normal" in data_1["types"]

    # Verificamos que se guardo correctamente en la DB
    with sqlite3.connect(settings.CACHE_DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
        assert count > 0, "¡La base de datos de caché sigue vacía!"

        rows = conn.execute("SELECT key FROM cache").fetchall()
        print(f"\nClaves reales en cache: {rows}")

    # Realizamos la segunda petición al cache, a los datos guardados de la primera
    start_time_cache = time.time()
    response_2 = functional_client.get("/api/v1/pokemon/ditto")
    duration_cache = time.time() - start_time_cache

    assert response_2.status_code == 200
    assert response_2.json()["id"] == data_1["id"]

    # Comprobamos el rendimiento,
    # la respuesta de cache debe ser mucho mayor a la PokeAPI
    assert duration_cache < duration_api
    print(
        f"\n[E2E] Tiempo API: {duration_api:.4f}s |Tiempo Cache: {duration_cache:.4f}s"
    )


# Comprobamos de manera funcional real el árbol evolutivo de Charmander
def test_e2e_evolution_real_api():
    response = functional_client.get("/api/v1/pokemon/charmander/evolution")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "charmander"

    # Validamos que la API real devuelve la cadena con sus hijos
    assert len(data["children"]) > 0
    assert data["children"][0]["name"] == "charmeleon"


# Comprobamos el comportamiento con cadenas no encontradas
def test_get_evolution_chain_e2e_not_found():

    response = functional_client.get("/api/v1/pokemon/missing_pokemon/evolution")
    data = response.json()

    error_msg = data["detail"]

    assert response.status_code == 404
    assert "No se encontro el recurso" in error_msg
    assert "Verifica que el nombre o ID sea correcto." in error_msg
