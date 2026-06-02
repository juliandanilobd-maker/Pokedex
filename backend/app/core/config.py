from typing import ClassVar
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(
        case_sensitive=False,
        env_file=".env",
    )

    APP_NAME: str = "Pokedex"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    POKEPI_BASE_URL: ClassVar[str] = "https://pokeapi.co/api/v2"
    REQUEST_TIMEOUT: int = 10
    MIN_REQUEST_DELAY: float = 0.1

    ALLOWED_ORIGINS: list[str] = ["*"]


settings = Settings()
