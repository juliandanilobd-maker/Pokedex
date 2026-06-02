from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settigs(BaseSettings):
    model_config = ConfigDict(
        case_sensitive=False,
        env_file=".env",
    )

    APP_NAME: str = "Pokedex"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    ALLOWED_ORIGINS: list[str] = ["*"]


settings = Settigs()
