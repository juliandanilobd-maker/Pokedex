from unittest.mock import MagicMock
import pytest

from backend.app.clients.pokeapi_client import PokeAPIClient


# Se crea un mock cache que simula el CacheManager, para no romper los tests que incluyan PokeAPI Client
@pytest.fixture
def mock_cache():
    cache = MagicMock()

    cache.get.return_value = None
    return cache


# Creamos un pokeapi_client para usar en pruebas, que llama al PokeAPI Client real del backend, pero que usa como argumento un mock cache
@pytest.fixture
def pokeapi_client(mock_cache):
    return PokeAPIClient(cache=mock_cache)
