from backend.app.parsers.evolution_parser import parse_evolution_tree


def test_parse_simple_evolution_chain():

    raw_data = {
        "species": {"name": "bulbasaur"},
        "evolves_to": [
            {
                "species": {"name": "ivysaur"},
                "evolves_to": [
                    {
                        "species": {"name": "venusaur"},
                    }
                ],
                "evolution_details": [
                    {
                        "min_level": 32,
                    }
                ],
            }
        ],
    }

    evolution = parse_evolution_tree(raw_data)
    ivysaur_node = evolution.children[0]

    assert evolution.name == "bulbasaur"
    assert len(evolution.children) == 1
    assert evolution.children[0].name == "ivysaur"
    assert evolution.children[0].children[0].name == "venusaur"
    assert ivysaur_node.evolution_details is not None
    assert ivysaur_node.evolution_details["min_level"] == 32
