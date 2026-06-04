from backend.app.parsers.pokemon_parser import (
    parse_pokemon,
    parse_pokemon_basic,
    parse_pokemon_description,
)


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
    assert pokemon.sprite_url == "sprite.png"
    assert pokemon.sprite_shiny == "sprite.png"


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


# Comprobamos que se utiliza como prioridad el artwork oficial
def test_parse_pokemon_official_artwork_priority():
    raw_data = {
        "sprites": {
            "front_default": "fallback.png",
            "front_shiny": "fallback_shiny.png",
            "other": {
                "official-artwork": {
                    "front_default": "official.png",
                    "front_shiny": "official_shiny.png",
                }
            },
        }
    }

    pokemon = parse_pokemon(raw_data)

    assert pokemon.sprite_url == "official.png"
    assert pokemon.sprite_shiny == "official_shiny.png"


# Comprobamos el manejo de diccionarios o datos vacíos
def test_parse_pokemon_missing_data():

    pokemon = parse_pokemon({})

    assert pokemon.id == 0
    assert pokemon.name == ""
    assert pokemon.types == []
    assert pokemon.stats == {}
    assert pokemon.sprite_url == ""
    assert pokemon.sprite_shiny == ""


# Comprobamos la cobertura en otros idiomas y el formateo de los datos
def test_parse_pokemon_description_success():

    raw_data = {
        "flavor_text_entries": [
            {
                "flavor_text": "Texto en japones que debe ignorar",
                "language": {"name": "ja"},
            },
            {
                "flavor_text": "This is a text\nwith newlines\fand formats.\r",
                "language": {"name": "en"},
            },
            {
                "flavor_text": "Texto en español, que deberá ser ignorado"
                "porque escogió el ingles primero",
                "language": {"name": "es"},
            },
        ]
    }

    description = parse_pokemon_description(raw_data)

    assert description == "This is a text with newlines and formats."


# Comprobamos descripciones en idiomas no admitidos
def test_parse_pokemon_description_no_valid_language():

    raw_species = {
        "flavor_text_entries": [
            {"flavor_text": "Bonjour", "language": {"name": "fr"}},
            {"flavor_text": "Hallo", "language": {"name": "de"}},
        ]
    }

    description = parse_pokemon_description(raw_species)

    assert description == ""
