from backend.app.parsers.pokemon_parser import (
    parse_pokemon,
    parse_pokemon_basic,
    parse_pokemon_description,
)


def test_parse_pokemon_basic_fields():
    """Este test comprueba el parseo de las caracteristicas y estadisticas base"""
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
    """Este test comprueba el parseo de los mínimos datos necesarios de un Pokemon"""
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
    """Este test comprueba el uso del sprite de official artwork"""
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


def test_parse_pokemon_missing_data():
    """Este test comprueba el manejo de diccionarios de datos vacíos"""
    pokemon = parse_pokemon({})

    assert pokemon.id == 0
    assert pokemon.name == ""
    assert pokemon.types == []
    assert pokemon.stats == {}
    assert pokemon.sprite_url == ""
    assert pokemon.sprite_shiny == ""


def test_parse_pokemon_description_success():
    """Este test comprueba el parseo correcto de la descripción de un Pokemon"""
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
                "flavor_text": "Texto en español,\nunico idioma que\fse obtiene. \r",
                "language": {"name": "es"},
                "version": {"name": "x"},
            },
        ]
    }

    description = parse_pokemon_description(raw_data)

    assert description.text == "Texto en español, unico idioma que se obtiene."
    assert description.language == "es"
    assert description.version == "x"


def test_parse_pokemon_description_no_valid_language():
    """Este test comprueba el manejo del error en caso de un lenguaje no válido de la
    descripción del Pokemon"""
    raw_species = {
        "flavor_text_entries": [
            {"flavor_text": "Bonjour", "language": {"name": "fr"}},
            {"flavor_text": "Hallo", "language": {"name": "de"}},
        ]
    }

    description = parse_pokemon_description(raw_species)

    assert (
        description.text == "Sin descripción registrada en los archivos de la Pokedex."
    )
