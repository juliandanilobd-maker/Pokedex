"""Este módulo contiene tests funcionales E2E que recogen el comportamiento real del
backend"""

from __future__ import annotations

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
    """Este test comprueba que se realiza de forma correcta una petición a la API,
    con todos sus subprocesos guardado en caché, consulta inicial a caché y si no se
    encuentra, consulta a la API, y que el rendimiento de la cache
    sea más rápido que las llamadas a la API"""
    start_time_api = time.time()
    response_1 = functional_client.get("/api/v2/pokemon/ditto")
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
    response_2 = functional_client.get("/api/v2/pokemon/ditto")
    duration_cache = time.time() - start_time_cache

    assert response_2.status_code == 200
    assert response_2.json()["id"] == data_1["id"]

    # Comprobamos el rendimiento,
    # la respuesta de cache debe ser mucho mayor a la PokeAPI
    assert duration_cache < (duration_api + 0.05)
    print(
        f"\n[E2E] Tiempo API: {duration_api:.4f}s |Tiempo Cache: {duration_cache:.4f}s"
    )


def test_e2e_evolution_real_api():
    """Este test comprueba una llamada real para obtener el árbol evolutivo de un
    Pokemon (Ej. Charmander)"""
    response = functional_client.get("/api/v2/pokemon/charmander/evolution")
    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "charmander"

    # Validamos que la API real devuelve la cadena con sus hijos
    assert len(data["children"]) > 0
    assert data["children"][0]["name"] == "charmeleon"


def test_get_evolution_chain_e2e_not_found():
    """Este test comprueba la captura de errores en caso de cadenas evolutivas
    no encontradas"""
    response = functional_client.get("/api/v2/pokemon/missing_pokemon/evolution")
    data = response.json()

    assert response.status_code == 404
    assert "No se encontro el recurso" in data["detail"]


def test_endpoint_filter_by_type_functional():
    """Este test comprueba la recolección correcta de los parametros de busqueda en una
    busqueda por filtros"""
    response = functional_client.get("/api/v2/filter?pokemon_type=grass")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)

    for pokemon in data:
        assert "grass" in [t.lower() for t in pokemon.get("types", [])]


def test_endpoint_filter_validation_error():
    """Este test comprueba la captura de un error frente a un parametro de busqueda por
    filtros invalido"""
    response = functional_client.get("/api/v2/filter?generation=PRIMERA")

    assert response.status_code == 422
    assert "detail" in response.json()


def test_e2e_effectiveness_real_resolution():
    """Este test comprueba una llamada a la API para obtener la efectividad en combate
    de un Pokemon"""
    response = functional_client.get("/api/v2/pokemon/charizard/effectiveness")
    data = response.json()

    assert response.status_code == 200
    assert "ground" in data["immunities"]
    assert "bug" in data["resistances_x025"]
    assert "grass" in data["resistances_x025"]
    assert "fairy" in data["resistances"]
    assert "fighting" in data["resistances"]
    assert "fire" in data["resistances"]
    assert "steel" in data["resistances"]
    assert "electric" in data["weaknesses"]
    assert "water" in data["weaknesses"]
    assert "rock" in data["weaknesses_x4"]


def test_e2e_effectiveness_not_found():
    """Este test comprueba la captura de un error frente a una efectividad en combate
    no encontrada"""
    response = functional_client.get("/api/v2/pokemon/asdfgh/effectiveness")
    data = response.json()
    assert response.status_code == 404
    assert "No se encontro el recurso" in data["detail"]
