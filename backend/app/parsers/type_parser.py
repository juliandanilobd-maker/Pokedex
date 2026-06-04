"""
Este módulo parsea las relaciones de daño de acuerdo a los tipos de Pokemon de la API
en el modelo TypeINFO.

Extrae las matrices de efectividad (debilidades, resistencias e inmunidades) necesarias
para calcular las ventajas o desventajas de los diferentes tipos en combate.
"""

from backend.app.models.pokemon_models import TypeInfo


def parse_type_info(data: dict) -> TypeInfo:

    # La PokeAPI agrupa las interacciones dentro del objeto damage_relations
    # Nos enfocamos en los vectores from para calcular las defensas
    relations = data.get("damage_relations", {})

    return TypeInfo(
        name=data.get("name", ""),
        double_damage_from=[
            t.get("name", "") for t in relations.get("double_damage_from", [])
        ],
        half_damage_from=[
            t.get("name", "") for t in relations.get("half_damage_from", [])
        ],
        no_damage_from=[t.get("name", "") for t in relations.get("no_damage_from", [])],
    )
