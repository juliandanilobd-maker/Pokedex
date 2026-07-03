from unittest.mock import AsyncMock

from backend.app.models.pokemon_models import PokemonDetail
from backend.app.services.pokemon_service import PokemonService


async def test_get_pokemon_detail_success():
    """Este test comprueba la obtención de datos correctos con respecto a un Pokemon"""
    client_mock = AsyncMock()

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

    client_mock.get_species.return_value = {"flavor_text_entries": []}

    service = PokemonService(client_mock)

    pokemon = await service.get_pokemon_detail("pikachu")

    client_mock.get_pokemon.assert_called_once_with("pikachu")

    assert isinstance(pokemon, PokemonDetail)
    assert pokemon.id == 25
    assert pokemon.name == "pikachu"
    assert pokemon.types == ["electric"]
    assert pokemon.stats["speed"] == 90
    assert pokemon.abilities == ["static"]
    assert pokemon.sprite_url == "pikachu.png"


async def test_get_pokemon_edtail_handles_empty_payload():
    """Este test comprueba el manejo de errores en el Pokemon Service, usando datos
    inválidos o inexistentes"""
    client_mock = AsyncMock()

    client_mock.get_pokemon.return_value = {}

    service = PokemonService(client_mock)
    pokemon = await service.get_pokemon_detail("25")  # Probamos usando ID numerico

    assert pokemon.id == 0
    assert pokemon.name == ""
    assert pokemon.types == []
    assert pokemon.stats == {}
    assert pokemon.sprite_url == ""
