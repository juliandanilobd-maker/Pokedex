import time

from backend.app.cache.cache_manager import CacheManager


# Creamos un test que inserta estos datos en el cache, y que los obtiene de forma correcta
def test_set_and_get():

    cache = CacheManager()

    cache.set(
        "pikachu",
        {"id": 25},
        ttl=60,
    )

    result = cache.get("pikachu")

    assert result is not None
    assert result["id"] == 25


# Testeamos el tiempo de expiración de la info en el cache
def test_expired_cache():

    cache = CacheManager()

    cache.set(
        "test",
        {"value": 1},
        ttl=1,
    )

    # Dejamos que expire la info (ttl = 1 segundo, consulta en = 2 segundos)
    time.sleep(2)

    assert cache.get("test") is None
