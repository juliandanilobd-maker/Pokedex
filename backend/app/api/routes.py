from fastapi import APIRouter, HTTPException
from dataclasses import asdict

from backend.app.core.config import settings
from backend.app.dependencies.dependencias import (
    pokemon_service,
    evolution_service,
)

router = APIRouter(prefix=settings.API_PREFIX)


# Endpoint dummy para validar routing correcto
@router.get("/status")
async def status() -> dict[str, str]:
    return {"status": "active", "layer": "fastapi-core"}


# Endpoint health
@router.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
    }


# Raiz de la API
@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Pokedex API -FastAPI core running"}


# Endpoint Pokemon
@router.get("/pokemon/{identifier}")
async def get_pokemon(identifier: str):

    try:
        return pokemon_service.get_pokemon_detail(identifier)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Endpoint Evolution
@router.get("/pokemon/{identifier}/evolution")
async def get_evolution_chain(identifier: str):

    try:
        node = evolution_service.get_evolution_tree(identifier)
        # Convierte un dataclass en un dict,
        # para poder extraer todos los datos de un diccionario
        return asdict(node) if node is not None else None

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
