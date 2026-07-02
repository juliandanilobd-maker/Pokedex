"""
En este módulo establecemos el molde o prototipo
de como se devolverán los datos de los diferentes servicios
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PokemonBasic(BaseModel):
    """Representación simplificada de un Pokemon para vistas en listados o carta"""

    id: int
    name: str
    types: list[str]
    sprite_url: str


class FlavorText(BaseModel):
    text: str
    language: str = "es"
    version: str = "Desconocida"


class PokemonDetail(BaseModel):
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
    flavor_text_entry: FlavorText | None = None


class EvolutionNode(BaseModel):
    """Nodo estructurado para representar los árboles de evoluciones.

    Implementando una estructura de datos recursivo donde cada Pokemon podría
    ramificarse en varias evoluciones simultaneas (ej. Eevee)
    """

    id: int
    name: str
    sprite_url: str
    children: list[EvolutionNode] = Field(default_factory=list)
    evolution_details: list[dict[str, Any]] | None = None
    visibility: bool = True


class PokemonEffectiveness(BaseModel):
    """Mapeo de las relaciones de efectividad y debilidades de acuerdo a los tipos"""

    weaknesses_x4: list[str]
    weaknesses: list[str]
    resistances: list[str]
    resistances_x025: list[str]
    immunities: list[str]


class PokemonFilter(BaseModel):
    """Definimos el contenedor de filtros"""

    # Al usar Field None, o Field 0, establecemos que no son parámetros obligatorios
    pokemon_type: str | None = Field(None, description="Tipo elemental del Pokemon")
    generation: int | None = Field(None, description="Generación (1, 2, etc.)")
    min_id: int = Field(0, description="ID mínimo del rango")
    max_id: int = Field(0, description="ID máximo del rango")
    min_attack: int = Field(0, description="Ataque base mínimo")
    min_defense: int = Field(0, description="Defensa base mínimo")
    min_hp: int = Field(0, description="Puntos de salud mínimos")
    min_base_exp: int = Field(0, description="Experiencia base mínima")
    min_speed: int = Field(0, description="Velocidad base mínima")


class TeamMember(BaseModel):
    """Representación de un Pokemon dentro de un equipo"""

    id: int
    name: str
    types: list[str]
    hp: int
    attack: int
    defense: int
    speed: int
    sprite_url: str


class TeamCreate(BaseModel):
    """Payload de entrada para crear o actualizar un equipo"""

    name: str = Field(..., min_length=1, max_length=50)
    pokemon_ids: list[int] = Field(..., min_length=1, max_length=6)


class TeamStats(BaseModel):
    """Estadísticas agregadas de un equipo, calculadas"""

    total_hp: int
    total_attack: int
    total_defense: int
    total_speed: int
    avg_hp: float
    avg_attack: float
    avg_defense: float
    avg_speed: float
    type_coverage: list[str]


class Team(BaseModel):
    """Entidad principal que persiste en data/teams.json"""

    id: str
    name: str
    members: list[TeamMember]
    stats: TeamStats
    created_at: str


class TypeAverageStats(BaseModel):
    """Estadisticas descriptivas promedio para un tipo elemental"""

    type_name: str
    sample_size: int
    avg_hp: float
    avg_attack: float
    avg_defense: float
    avg_speed: float


class TopPokemonEntry(BaseModel):
    """Entrada individual en un ranking Top-N"""

    id: int
    name: str
    types: list[str]
    value: int
    metric: str


class AnomalyEntry(BaseModel):
    """Pokemon detectado como anómalo, o que se sale de las métricas
    con respecto a su tipo"""

    id: int
    name: str
    types: list[str]
    stat_total: int
    type_average: float
    deviation: float
    method: str
    reason: str


class PredictionResult(BaseModel):
    """El modelo de las estadisticas de predicción de un Pokemon"""

    primary_type: str
    secondary_type: str | None = None
    predicted_hp: float
    predicted_attack: float
    predicted_defense: float
    predicted_speed: float
    sample_size: int
    generations_used: list[int]
    window_size: int
    group_avg_hp: float
    group_avg_attack: float
    group_avg_defense: float
    group_avg_speed: float
    description: str


class SimulatorResult(BaseModel):
    """El modelo de los resultados de la generación de un Pokemon ficticio"""

    csv_path: str
    generated_count: int
    total_accumulated: int
    pokemon_type: str
    generation: int
    message: str
