from backend.app.parsers.pokemon_parser import parse_pokemon, parse_pokemon_basic


def test_parse_pokemon_basic_fields():

    raw_data = {
        "id": 25,
        "name": "pikachu",
        "types": [{"type": {"name": "electric"}}],
        "stats": [
            {
                "stat": {"name": "speed"},
                "base_stat": 90,
            }
        ],
        "abilities": [{"ability": {"name": "static"}}],
        "height": 4,
        "weight": 60,
        "base_experience": 112,
        "sprites": {"front_default": "sprite.png"},
    }

    pokemon = parse_pokemon(raw_data)

    assert pokemon.id == 25
    assert pokemon.name == "pikachu"
    assert pokemon.types == ["electric"]
    assert pokemon.stats["speed"] == 90


def test_parse_pokemon_basic():

    raw_data = {
        "id": 1,
        "name": "bulbasaur",
        "types": [{"type": {"name": "grass"}}],
        "sprites": {"front_default": "sprite.png"},
    }

    pokemon = parse_pokemon_basic(raw_data)

    assert pokemon.id == 1
    assert pokemon.name == "bulbasaur"
    assert pokemon.types == ["grass"]
