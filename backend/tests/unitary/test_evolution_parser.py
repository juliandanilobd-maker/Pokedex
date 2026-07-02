from backend.app.parsers.evolution_parser import parse_evolution_tree


def test_parse_simple_evolution_tree():
    """Este test comprueba el parseo correcto de un árbol evolutivo con línea directa,
    sin ramificaciones"""
    raw_data = {
        "species": {"name": "bulbasaur"},
        "evolution_details": [],
        "evolves_to": [
            {
                "species": {"name": "ivysaur"},
                "evolution_details": [],
                "evolves_to": [
                    {
                        "species": {"name": "venusaur"},
                        "evolution_details": [
                            {
                                "min_level": 32,
                            }
                        ],
                    },
                ],
            }
        ],
    }

    evolution = parse_evolution_tree(raw_data)
    ivysaur_node = evolution.children[0]
    venusaur_node = ivysaur_node.children[0]

    # Probamos la extracción correcta de datos,
    # pero tambien que maneja la ausencia de detalles de evolución
    assert evolution.name == "bulbasaur"
    assert evolution.evolution_details is None
    assert len(evolution.children) == 1

    # Probamos la extracción de datos de la primera evolución,
    # pero tambien el manejo de ausencia de ciertos detalles
    assert ivysaur_node.name == "ivysaur"
    assert ivysaur_node.evolution_details is None

    # Probamos la segunda evolución
    assert venusaur_node.name == "venusaur"
    assert venusaur_node.evolution_details is not None
    assert venusaur_node.evolution_details[0]["min_level"] == 32
    assert venusaur_node.evolution_details[0]["item"] is None


# Probamos la cobertura del parser evolution en un árbol con distintas ramificaciones
def test_parse_branched_evolution():
    """Este test comprueba el parseo correcto de un árbol evolutivo con varias
    ramificaciones"""
    raw_data = {
        "species": {"name": "eevee"},
        "evolves_to": [
            {"species": {"name": "vaporeon"}},
            {"species": {"name": "jolteon"}},
            {"species": {"name": "flareon"}},
            {"species": {"name": "espeon"}},
            {"species": {"name": "umbreon"}},
            {"species": {"name": "leafeon"}},
            {"species": {"name": "glaceon"}},
            {"species": {"name": "sylveon"}},
        ],
    }

    evolution = parse_evolution_tree(raw_data)

    # Comprobamos que el parser extrae correctamente las estructuras no lineales
    assert len(evolution.children) == 8
    assert evolution.children[0].name == "vaporeon"
    assert evolution.children[1].name == "jolteon"
    assert evolution.children[2].name == "flareon"
    assert evolution.children[3].name == "espeon"
    assert evolution.children[4].name == "umbreon"
    assert evolution.children[5].name == "leafeon"
    assert evolution.children[6].name == "glaceon"
    assert evolution.children[7].name == "sylveon"


def test_parse_evolution_all_details():
    """Este test comprueba que se parsean correctamente los detalles de una evolución
    (los requisitos)"""
    raw_data = {
        "species": {"name": "eevee"},
        "evolves_to": [
            {
                "species": {"name": "vaporeon"},
                "evolution_details": {
                    "trigger": {"name": "use-item"},
                    "item": {"name": "water-stone"},
                },
            },
            {
                "species": {"name": "jolteon"},
                "evolution_details": {
                    "trigger": {"name": "use-item"},
                    "item": {"name": "thunder-stone"},
                },
            },
            {
                "species": {"name": "flareon"},
                "evolution_details": {
                    "trigger": {"name": "use-item"},
                    "item": {"name": "fire-stone"},
                },
            },
            {
                "species": {"name": "espeon"},
                "evolution_details": {
                    "trigger": {"name": "level-up"},
                    "min_happiness": 220,
                    "time_of_day": "day",
                },
            },
            {
                "species": {"name": "umbreon"},
                "evolution_details": {
                    "trigger": {"name": "level-up"},
                    "min_happiness": 220,
                    "time_of_day": "night",
                },
            },
            {
                "species": {"name": "leafeon"},
                "evolution_details": [
                    {
                        "trigger": {"name": "level-up"},
                        "location": {"name": "moss-rock"},
                    },
                    {"trigger": {"name": "use-item"}, "item": {"name": "leaf-stone"}},
                ],
            },
            {
                "species": {"name": "glaceon"},
                "evolution_details": [],
            },
            {
                "species": {"name": "sylveon"},
                "evolution_details": {
                    "trigger": {"name": "level-up"},
                    "min_affection": 2,
                },
            },
        ],
    }

    evolution = parse_evolution_tree(raw_data)
    vaporeon_details = evolution.children[0].evolution_details

    assert vaporeon_details is not None
    assert len(vaporeon_details) == 1
    assert vaporeon_details[0]["item"] == "water-stone"

    jolteon_details = evolution.children[1].evolution_details

    assert jolteon_details is not None
    assert len(jolteon_details) == 1
    assert jolteon_details[0]["item"] == "thunder-stone"

    flareon_details = evolution.children[2].evolution_details

    assert flareon_details is not None
    assert len(flareon_details) == 1
    assert flareon_details[0]["item"] == "fire-stone"

    espeon_details = evolution.children[3].evolution_details

    assert espeon_details is not None
    assert len(espeon_details) == 1
    assert espeon_details[0]["trigger"] == "level-up"
    assert espeon_details[0]["min_happiness"] == 220
    assert espeon_details[0]["time_of_day"] == "day"

    umbreon_details = evolution.children[4].evolution_details

    assert umbreon_details is not None
    assert len(umbreon_details) == 1
    assert umbreon_details[0]["trigger"] == "level-up"
    assert umbreon_details[0]["min_happiness"] == 220
    assert umbreon_details[0]["time_of_day"] == "night"

    leafeon_details = evolution.children[5].evolution_details

    assert leafeon_details is not None
    assert len(leafeon_details) == 2
    assert leafeon_details[0]["trigger"] == "level-up"
    assert leafeon_details[0]["location"] == "moss-rock"
    assert leafeon_details[1]["trigger"] == "use-item"
    assert leafeon_details[1]["item"] == "leaf-stone"

    # Comprobamos el comportamiento frente a listas evolution_details vacías
    glaceon_details = evolution.children[6].evolution_details

    assert glaceon_details is None

    sylveon_details = evolution.children[7].evolution_details

    assert sylveon_details is not None
    assert len(sylveon_details) == 1
    assert sylveon_details[0]["trigger"] == "level-up"
    assert sylveon_details[0]["min_affection"] == 2


def test_parse_evolution_empty_node():
    """Este test comprueba el comportamiento del parser frente a diccionarios vacíos o
    corruptos, se captura correctamente el
    error y no colapsa la app"""
    raw_data = {}

    evolution = parse_evolution_tree(raw_data)

    assert evolution.name == "desconocido"
    assert evolution.children == []
    assert evolution.evolution_details is None
