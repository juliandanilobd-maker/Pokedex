"""
En este módulo se parsea recursivamente el árbol de evolución anidado de la PokeAPI.

Tranformamos la estructura de diccionarios dinámicos en un árbol de tipado de objetos
EvolutionNode, estandarizando los requisitos de evolución.
"""

import re

from backend.app.models.pokemon_models import EvolutionNode


def _extract_id_from_species_url(url: str) -> int:

    if not url:
        return 0

    match = re.search(r"/pokemon-species/(\d+)/", url)
    if match:
        return int(match.group(1))

    match_fallback = re.search(r"/pokemon/(\d+)/", url)

    return int(match_fallback.group(1)) if match_fallback else 0


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

    species_raw = node.get("species")

    species_name = (
        species_raw.get("name", "Desconocido")
        if isinstance(species_raw, dict)
        else "desconocido"
    )
    species_url = species_raw.get("url", "") if isinstance(species_raw, dict) else ""

    pokemon_id = _extract_id_from_species_url(species_url)

    constructed_sprite = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"

    return EvolutionNode(
        id=pokemon_id,
        name=species_name,
        sprite_url=constructed_sprite,
        children=children,
        visibility=True,
        evolution_details=evolution_details,
    )
