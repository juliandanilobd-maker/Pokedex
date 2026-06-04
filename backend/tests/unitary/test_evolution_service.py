from unittest.mock import MagicMock

import pytest

from backend.app.services.evolution_service import EvolutionService


class MockClient:
    def get_species(self, identifier):

        return {"evolution_chain": {"url": "http://pokeapi.co/v2/evolution-chain/1/"}}

    def get(self, url):

        return {
            "chain": {
                "species": {"name": "bulbasaur"},
                "evolves_to": [],
            }
        }


# Comprobamos que se obtiene de manera correcta la evolución
def test_get_evolution_tree():

    service = EvolutionService(MockClient())

    tree = service.get_evolution_tree("1")

    assert tree is not None
    assert tree.name == "bulbasaur"
    assert tree.children == []


# Comprobamos el comportamiento del servicio usando su funcionalidad "if not evo_url"
def test_get_evolution_tree_missing_url():

    client_mock = MagicMock()
    client_mock.get_species.return_value = {"evolution_chain": {}}

    service = EvolutionService(client_mock)

    tree = service.get_evolution_tree("pikachu")

    assert tree is None


# Comprobamos el comportamiento ante datos corruptos
def test_get_evolution_tree_corrupted_chain_data():

    client_mock = MagicMock()
    client_mock.get_species.return_value = {"evolution_chain": {"url": "valid_url"}}

    # Simulamos un error en la API
    client_mock.get.return_value = {"corrupted_data": {}}

    service = EvolutionService(client_mock)

    with pytest.raises(KeyError):
        service.get_evolution_tree("uknown")
