from backend.app.parsers.type_parser import parse_type_info


def test_parse_type_info():

    raw_data = {
        "name": "fire",
        "damage_relations": {
            "double_damage_from": [{"name": "water"}],
            "half_damage_from": [{"name": "grass"}],
            "no_damage_from": [{"name": "normal"}],
        },
    }

    result = parse_type_info(raw_data)

    assert result.name == "fire"
    assert result.double_damage_from == ["water"]
    assert result.half_damage_from == ["grass"]
    assert result.no_damage_from == ["normal"]


# Comprobamos el comportamiento frente a diccionarios sin relaciones o vacíos
def test_parse_type_info_missing_relations():

    raw_data = {"name": "ghost"}

    result = parse_type_info(raw_data)

    assert result.name == "ghost"
    assert result.double_damage_from == []
    assert result.half_damage_from == []
    assert result.no_damage_from == []


# Comprobamos el comportamiento con elementos corruptos dentro de las listas de daño
def test_parse_type_info_handles_corrupted_elements():

    raw_data = {
        "name": "dragon",
        "damage_relations": {
            "double_damage_from": [{"url": "http://api-rota.com"}],
            "half_damage_from": [],
            "no_damage_from": [],
        },
    }

    result = parse_type_info(raw_data)

    assert result.name == "dragon"
    assert result.double_damage_from == [""]
