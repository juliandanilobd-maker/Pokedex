from backend.app.services.pokemon_service import PokemonService


class MockClient:
    def get_pokemon(self, identifier):

        return {
            "id": 25,
            "name": "pikachu",
            "types": [],
            "stats": [],
            "abilities": [],
            "sprites": {},
        }


def test_get_pokemon_detail():
    service = PokemonService(MockClient())

    pokemon = service.get_pokemon_detail("pikachu")

    assert pokemon.id == 25
    assert pokemon.name == "pikachu"
