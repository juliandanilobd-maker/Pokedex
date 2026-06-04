from unittest.mock import MagicMock

from backend.app.models.pokemon_models import PokemonDetail
from backend.app.services.pokemon_service import PokemonService


def test_get_pokemon_detail_success():

    client_mock = MagicMock()

    client_mock.get_pokemon.return_value = {
        "id": 25,
        "name": "pikachu",
        "types": [{"type": {"name": "electric"}}],
        "stats": [{"stat": {"name": "speed"}, "base_stat": 90}],
        "abilities": [{"ability": {"name": "static"}}],
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "sprites": {"front_default": "pikachu.png"},
    }

    service = PokemonService(client_mock)

    pokemon = service.get_pokemon_detail("pikachu")

    client_mock.get_pokemon.assert_called_once_with("pikachu")

    assert isinstance(pokemon, PokemonDetail)
    assert pokemon.id == 25
    assert pokemon.name == "pikachu"
    assert pokemon.types == ["electric"]
    assert pokemon.stats["speed"] == 90
    assert pokemon.abilities == ["static"]
    assert pokemon.sprite_url == "pikachu.png"


# Comprobamos el comportamiento con datos minimos o corruptos
def test_get_pokemon_edtail_handles_empty_payload():

    client_mock = MagicMock()

    client_mock.get_pokemon.return_value = {}

    service = PokemonService(client_mock)
    pokemon = service.get_pokemon_detail("25")  # Probamos usando ID numerico

    assert pokemon.id == 0
    assert pokemon.name == ""
    assert pokemon.types == []
    assert pokemon.stats == {}
    assert pokemon.sprite_url == ""
