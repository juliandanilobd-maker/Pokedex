"""
En este módulo se parsea recursivamente el árbol de evolución anidado de la PokeAPI.

Tranformamos la estructura de diccionarios dinámicos en un árbol de tipado de objetos
EvolutionNode, estandarizando los requisitos de evolución.
"""

from backend.app.models.pokemon_models import EvolutionNode


def parse_evolution_tree(node: dict) -> EvolutionNode:

    # Mapeamos cada sub-nodo dentro de evolves_to
    # Si es una lista vacía el bucle no se ejecuta.
    children = [parse_evolution_tree(evo) for evo in node.get("evolves_to", []) or []]

    evolution_details = None
    raw_details = node.get("evolution_details")

    if raw_details:
        # Establecemos un sistema por si la API devuelve detalles como diccionario
        # único o una lista de elementos, normalizamos esta entrada
        # a una lista iterable para unificar el procesamiento
        details = raw_details if isinstance(raw_details, list) else [raw_details]

        evolution_details = []

        for d in details:
            if isinstance(d, dict):
                # Extraemos de forma segura los datos anidados, utilizando isinstance
                # para evitar KeyErrors o AttributeErrores en llaves complejas.
                details_parsed = {
                    "min_level": d.get("min_level"),
                    "item": (
                        d.get("item", {}).get("name")
                        if isinstance(d.get("item"), dict)
                        else None
                    ),
                    "trigger": (
                        d.get("trigger", {}).get("name")
                        if isinstance(d.get("trigger"), dict)
                        else None
                    ),
                    "min_happiness": (d.get("min_happiness")),
                    "time_of_day": (
                        d.get("time_of_day") if d.get("time_of_day") != "" else None
                    ),
                    "location": (
                        d.get("location", {}).get("name")
                        if isinstance(d.get("location"), dict)
                        else None
                    ),
                    "min_affection": (d.get("min_affection")),
                }

                evolution_details.append(details_parsed)

    # Si la lista quedó vacía por falta de detalles o por fallo en la estructura,
    # se establece explícitamente un None para evitar devolución de listas vacías
    if not evolution_details:
        evolution_details = None

    return EvolutionNode(
        name=node.get("species", {}).get("name", "")
        if isinstance(node.get("species"), dict)
        else "",
        children=children,
        visibility=True,
        evolution_details=evolution_details,
    )
