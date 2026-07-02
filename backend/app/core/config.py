"""
En este módulo establecemos las constantes de configuración globales
"""

from typing import Any, ClassVar

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = {
        "case_sensitive": False,
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    APP_NAME: str = "Pokedex"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v2"

    # Infraestructura externa, instanciado con Field, para permitir su sustitución
    # por un mock o un espejo en entornos de testing.
    POKEAPI_BASE_URL: str = Field(default="https://pokeapi.co/api/v2")
    REQUEST_TIMEOUT: int = 10
    MIN_REQUEST_DELAY: float = 0.5
    CACHE_TTL: int = 604800  # Datos permanecen 1 semana en la caché

    # Ruta del archivo SQLite para la cache, para los tests funcionales usamos
    # un archivo aislado modificando esta variable
    CACHE_DB_PATH: str = "pokemon_cache.db"

    ALLOWED_ORIGINS: str | list[str] = [
        "http://localhost:8501",
        "http://localhost:3000",
    ]

    # Se añade validador para normalizar dato de ALLOWED_ORIGINS para permitir testing
    # automatizado en GitHub Actions
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        # Si ya es una lista, queda como lista
        if isinstance(v, list):
            return v
        # Si es un string eliminamos corchetes o comillas para que el url quede intacto
        if isinstance(v, str):
            clean_v = (
                v.strip()
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
                .replace('"', "")
            )
            # Si el string llega vacío, devolvemos una lista vacía
            if not clean_v:
                return ["http://localhost:8501", "http://localhost:3000"]

            items = [item.strip() for item in clean_v.split(",") if item.strip()]

            if not all(item.startswith(("http://", "https://")) for item in items):
                return ["http://localhost:8501", "http://localhost:3000"]

            # Separamos por comas para armar la lista limpia
            return [item.strip() for item in clean_v.split(",") if item.strip()]
        # Si llega cualquier cosa diferente a una URL válida, devolvemos este fallback
        return ["http://localhost:8501", "http://localhost:3000"]


settings = Settings()
