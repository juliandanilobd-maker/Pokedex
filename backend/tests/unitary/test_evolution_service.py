from unittest.mock import AsyncMock

import pytest

from backend.app.services.evolution_service import EvolutionService


# Generamos una mock class Client para insertar respuestas controladas y evitar llamadas
# innecesarias a la API
class MockClient:
    async def get_species(self, identifier):

        return {"evolution_chain": {"url": "http://pokeapi.co/v2/evolution-chain/1/"}}

    async def get(self, url):

        return {
            "chain": {
                "species": {"name": "bulbasaur"},
                "evolves_to": [],
            }
        }


async def test_get_evolution_tree():
    """Este test comprueba que se obtienen correctamente los datos de un árbol
    evolutivo"""
    service = EvolutionService(MockClient())

    tree = await service.get_evolution_tree("1")

    assert tree is not None
    assert tree.name == "bulbasaur"
    assert tree.children == []


async def test_get_evolution_tree_missing_url():
    """Este test comprueba que se devuelve un None si no existe el árbol evolutivo"""
    client_mock = AsyncMock()
    client_mock.get_species.return_value = {"evolution_chain": {}}

    service = EvolutionService(client_mock)

    tree = await service.get_evolution_tree("pikachu")

    assert tree is None


async def test_get_evolution_tree_corrupted_chain_data():
    """Este test comprueba el comportamiento del servicio frente a datos corruptos
    o inválidos"""
    client_mock = AsyncMock()
    client_mock.get_species.return_value = {"evolution_chain": {"url": "valid_url"}}

    # Simulamos un error en la API
    client_mock.get.return_value = {"corrupted_data": {}}

    service = EvolutionService(client_mock)

    with pytest.raises(KeyError):
        await service.get_evolution_tree("uknown")
