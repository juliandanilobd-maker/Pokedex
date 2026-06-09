from unittest.mock import MagicMock

import pytest

from backend.app.services.type_service import TypeService


# Creamos un cliente que simule el comportamiento de PokeAPIClient
@pytest.fixture
def mock_client():
    return MagicMock()

# Creamos un type service que inicialice el servicio con el cliente simulado
@pytest.fixture
def type_service(mock_client):
    return TypeService(client=mock_client)

# Comprobamos que el servicio extraiga y estructure las relaciones correctamente
def test_Get_damage_relations_success(type_service, mock_client):

    mock_client.get_type.return_value = {
        "name": "fire",
        "damage_relations": {
            "double_damage_from": [{"name": "water"}, {"name": "ground"}],
            "half_damage_from": [{"name": "fire"}, {"name": "grass"}],
            "no_damage_from": []
        }
    }

    result = type_service.get_damage_relations("fire")

    assert isinstance(result, dict)
    assert "water" in result["double_damage_from"]
    assert "ground" in result["double_damage_from"]
    assert "grass" in result["half_damage_from"]
    assert len(result["no_damage_from"]) == 0
    mock_client.get_type.assert_called_once_with("fire")

# Comprobamos los datos específicos de un tipo
def test_fire_type_relations(type_service, mock_client):

    mock_client.get_type.return_value = {
        "name": "fire",
        "damage_relations": {
            "double_damage_from": [{"name": "electric"}, {"name": "grass"}],
            "half_damage_from": [{"name": "fire"}, {"name": "water"}],
            "no_damage_from": []
        }
    }

    result = type_service.get_damage_relations("water")

    assert "electric" in result["double_damage_from"]
    assert "fire" in result["half_damage_from"]
