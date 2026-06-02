from __future__ import annotations

from fastapi import FastAPI
from contextlib import asynccontextmanager
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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(router)


# Verifica el estado del backend
@app.get("/health", tags=["Health"])
async def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
    }
