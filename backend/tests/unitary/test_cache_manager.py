import sqlite3
import time

import pytest

from backend.app.cache.cache_manager import CacheManager
from backend.app.core.config import settings


# Utilizamos fixture para que cada test use una base de datos limpia en cada prueba
@pytest.fixture
def cache_test(monkeypatch, tmp_path):
    # Creamos un archivo temporal para la base de datos local
    test_db = tmp_path / "test_cache.db"
    monkeypatch.setattr(settings, "CACHE_DB_PATH", str(test_db))
    return CacheManager()


# PRUEBAS PARA DETERMINAR EL FUNCIONAMIENTO EN LOS ACIERTOS DE CACHE
# Creamos un test que inserta estos datos en el cache,
# y que los obtiene de forma correcta
def test_set_and_get(cache_test):

    cache_test.set(
        "pikachu",
        {"id": 25},
        ttl=60,
    )

    result = cache_test.get("pikachu")

    assert result is not None
    assert result["id"] == 25

    # Probamos la actualización de una clave existente
    cache_test.set(
        "pikachu",
        {
            "id": 25,
            "level": 100,
        },
        ttl=60,
    )

    updated_result = cache_test.get("pikachu")

    assert updated_result["id"] == 25
    assert updated_result["level"] == 100


# Testeamos el tiempo de expiración de la info en el cache
def test_expired_cache():

    cache = CacheManager()

    cache.set(
        "test",
        {"value": 1},
        ttl=1,
    )

    # Dejamos que expire la info (ttl = 1 segundo, consulta en = 1.1 segundos)
    time.sleep(1.1)

    assert cache.get("test") is None


# Test usando el ttl por defecto establecido en settings
def test_default_ttl_framework(monkeypatch, cache_test):
    # Establecemos un ttl por defecto en las configuraciones para probar
    # que el cache usa el ttl por defecto
    monkeypatch.setattr(settings, "CACHE_TTL", 1)

    # No le pasamos el ttl para comprobar que usa el por defecto
    cache_test.set("default_key", {"data": "ok"})

    time.sleep(1.1)
    assert cache_test.get("default_key") is None


# PRUEBAS PARA DETERMINAR FUNCIONAMIENTO EN FALLOS DEL CACHE
# Test con clave inexistente
def test_get_non_existent_key(cache_test):

    # Intentamos pedir algo que no se ha guardado en el cache
    result = cache_test.get("missing_pokemon")
    assert result is None


# Test con JSON corrupto
def test_corrupted_json_handling(cache_test):

    # Se guarda un dato no JSON válido en la DB para forzar error
    with sqlite3.connect(cache_test.db_path) as conn:
        conn.execute(
            "INSERT INTO cache VALUES (?, ?, ?)",
            ("corrupt", "{this string is not a valid json}", time.time() + 60),
        )
        conn.commit()

    # Probamos si se detecta el JSONDecodeError, y se borra la fila de la DB.
    result = cache_test.get("corrupt")
    assert result is None

    # Probamos si se ejecutó el borrado de esa fila
    with sqlite3.connect(cache_test.db_path) as conn:
        row = conn.execute("SELECT * FROM cache WHERE key='corrupt'").fetchone()
        assert row is None
