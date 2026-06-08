from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    get_evolution_service,
    get_pokemon_service,
)
from backend.app.services.evolution_service import EvolutionService
from backend.app.services.filter_service import FilterService
from backend.app.services.pokemon_service import PokemonService

router = APIRouter(prefix=settings.API_PREFIX)

# ENDPOINTS CON DEPENDENCY INJECTION


@router.get("/pokemon/{identifier}", tags=["Pokemon"])
async def get_pokemon(
    identifier: str, pokemon_service: PokemonService = Depends(get_pokemon_service)
):

    try:
        return pokemon_service.get_pokemon_detail(identifier)

    except ValueError as e:
        # Se captura el error con un Value Error si la API devuelve un 404
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/pokemon/{identifier}/evolution", tags=["Evolution"])
async def get_evolution_chain(
    identifier: str,
    evolution_service: EvolutionService = Depends(get_evolution_service),
):

    try:
        node = evolution_service.get_evolution_tree(identifier)
        # Presentamos un nodo tipado con un Dataclass, y lo serializamos a diccionario
        # para poder procesar la respuesta JSON.
        return asdict(node) if node is not None else None

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/filter", tags=["Filter"])
async def get_filtered_pokemons(
    pokemon_type: str | None = Query(None, description="Tipo elemental del Pokemon"),
    generation: int | None = Query(None, description="Generación (1, 2, etc.)"),
    min_id: int = Query(0, description="ID mínimo del rango"),
    max_id: int = Query(0, description="ID máximo del rango"),
    min_attack: int = Query(0, description="Ataque base mínimo"),
    min_defense: int = Query(0, description="Defensa base mínimo"),
    min_hp: int = Query(0, description="Puntos de salud mínimos"),
    min_base_exp: int = Query(0, description="Experiencia base mínima"),
    min_speed: int = Query(0, description="Velocidad base mínima"),
) -> list[dict]:
    """Endpoint para filtrar el dataset de Pokemon de forma acumulativa"""

    filter_service = FilterService()
    try:
        return filter_service.filter_pokemons(
            pokemon_type=pokemon_type,
            generation=generation,
            min_id=min_id,
            max_id=max_id,
            min_attack=min_attack,
            min_defense=min_defense,
            min_hp=min_hp,
            min_base_exp=min_base_exp,
            min_speed=min_speed,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al procesar el filtrado analítico: {e!s}",
        ) from e
