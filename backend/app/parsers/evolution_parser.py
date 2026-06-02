from backend.app.models.pokemon_models import EvolutionNode


def parse_evolution_tree(node: dict) -> EvolutionNode:

    children = [parse_evolution_tree(evo) for evo in node.get("evolves_to", [])]

    evolution_details = None
    if node.get("evolution_details"):
        d = node["evolution_details"][0]

        evolution_details = {
            "min_level": d.get("min_level"),
            "item": (d.get("item", {}).get("name") if d.get("item") else None),
            "trigger": (d.get("trigger", {}).get("name") if d.get("trigger") else None),
            "min_happiness": (
                d.get("min_happiness", {}) if d.get("min_happiness") else None
            ),
            "time_of_day": (d.get("time_of_day", {}) if d.get("time_of_day") else None),
        }

    return EvolutionNode(
        name=node.get("species", {}).get("name", ""),
        children=children,
        evolution_details=evolution_details,
    )
