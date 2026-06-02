from fastapi import APIRouter

from backend.app.core.config import settings

router = APIRouter(prefix=settings.API_PREFIX)


# Raiz de la API
@router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Pokedex API -FastAPI core running"}


# Endpoint dummy para validar routing correcto
@router.get("/status")
async def status() -> dict[str, str]:
    return {"status": "active", "layer": "fastapi-core"}
