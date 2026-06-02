from backend.app.parsers.type_parser import parse_type_info


def test_parse_type_info():

    raw_data = {
        "name": "fire",
        "damage_relations": {
            "double_damage_from": [{"name": "water"}],
            "half_damage_from": [{"name": "grass"}],
            "no_damage_from": [],
        },
    }

    result = parse_type_info(raw_data)

    assert result.name == "fire"
    assert result.double_damage_from == ["water"]
    assert result.half_damage_from == ["grass"]
