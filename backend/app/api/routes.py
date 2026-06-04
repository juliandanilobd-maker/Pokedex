from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    get_evolution_service,
    get_pokemon_service,
)
from backend.app.services.evolution_service import EvolutionService
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
