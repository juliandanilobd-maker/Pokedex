"""
En este módulo establecemos el molde o prototipo
de como se devolverán los datos de los diferentes servicios
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PokemonBasic:
    """Representación simplificada de un Pokemon para vistas en listados o carta"""

    id: int
    name: str
    types: list[str]
    sprite_url: str


@dataclass
class PokemonDetail:
    """Información completa del Pokemon para su vista al detalle"""

    id: int
    name: str
    types: list[str]
    stats: dict[str, int]
    abilities: list[str]
    height: int
    weight: int
    base_experience: int
    sprite_url: str
    sprite_shiny: str | None = None

@dataclass
class EvolutionNode:
    """Nodo estructurado para representar los árboles de evoluciones.

    Implementando una estructura de datos recursivo donde cada Pokemon podría
    ramificarse en varias evoluciones simultaneas (ej. Eevee)
    """

    name: str
    children: list[EvolutionNode] = field(default_factory=list)
    evolution_details: list[dict[str, Any]] | None = None
    visibility: bool = True


@dataclass
class TypeInfo:
    """Mapeo de las relaciones de efectividad y debilidades de acuerdo a los tipos"""

    name: str
    double_damage_from: list[str]
    half_damage_from: list[str]
    no_damage_from: list[str]

@dataclass
class PokemonEffectiveness:
    weaknesses: list[str]
    resistance: list[str]
    inmunities: list[str]
