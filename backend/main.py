from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core.config import settings


# Se inicializa el servidor
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Evento que se ejecuta al iniciar la aplicación
    print(f"{settings.APP_NAME} iniciado correctamente")

    yield

    print(f"{settings.APP_NAME} cerrando")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(router)


# Los 3 endpoints al ser Core, no necesitan inyección porque son estáticos


# Raiz de la API
@app.get("/", tags=["Infraestructure"])
async def root() -> dict[str, str]:
    return {"message": "Pokedex API -FastAPI core running"}


# Endpoint health, verifica el estado del backend
@app.get("/health", tags=["Health"])
async def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
    }
