"""
Este modulo proporciona una clase que encapsula las peticiones HTTP a la API,
maneja errores, implementa rate limiting basico y utiliza cache para evitar
peticiones repetidas.
"""

import time

import requests

from backend.app.core.config import settings


class PokeAPIClient:
    """
    Cliente para interactuar con la PokeAPI.

    Caracteristicas:
    - Cache automático de respuestas (SQLite).
    - Rate Limiting.
    - HTTP Client.
    - Manejo de errores.
    - Constructor de URL.
    """

    def __init__(self, cache):

        self.base_url = settings.POKEAPI_BASE_URL
        self.cache = cache
        self._last_request_time = 0.0

    # A continuacion viene la base de las peticiones http
    def get(self, endpoint: str) -> dict:
        """
        Hace una peticion GET a la API.

        Args:
            endpoint: Ruta relativa al base_url (ej: "pokemon/pikachu").

        Returns:
            Diccionario con la respuesta JSON de la API.

        Raises:
            requests.exceptions.HTTPError: Si la API responde con error (
            404, 500, etc.
        )
            requests.exceptions.ConnectionError: Si no hay conexion a internet.
            requests.exceptions.Timeout: Si la peticion tarda demasiado.
        """

        url = self._build_url(endpoint)

        cached = self.cache.get(url)
        if cached is not None:
            return cached

        self._rate_limit()

        try:
            response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                raise ValueError(
                    f"No se encontro el recurso: {endpoint}."
                    "Verifica que el nombre o ID sea correcto."
                ) from e
            raise

        except requests.exceptions.ConnectionError as e:
            raise ConnectionError("No se pudo conectar a la PokeAPI.") from e

        except requests.exceptions.Timeout as e:
            raise TimeoutError(
                "La peticion a la PokeAPI tardo demasiado. "
                "Intenta de nuevo en unos momentos."
            ) from e

        # Establecemos un update state
        self._last_request_time = time.time()

        # Guardamos en la cache para futuras consultas
        self.cache.set(url, data, ttl=settings.CACHE_TTL)

        return data

    def _build_url(self, endpoint: str) -> str:

        if endpoint.startswith("http"):
            # Establecemos control SSRF (Server-Side Request Forgery), bloqueando
            # peticiones a dominios arbitrarios si un endpoint intenta desviar al client
            if not endpoint.startswith(self.base_url):
                raise ValueError("URL externa no permitida")

            return endpoint

        return f"{self.base_url.rstrip('/')}/{endpoint.strip('/')}"

    def _rate_limit(self):

        elapsed = time.time() - self._last_request_time

        # Forzamos un bloqueo (sleep), si el tiempo de la petición actual es menor a
        # al umbral de peticiones configurado en settings, esto protege nuestra IP
        # de bloqueos por ráfagas
        if elapsed < settings.MIN_REQUEST_DELAY:
            time.sleep(settings.MIN_REQUEST_DELAY - elapsed)

    # Usamos identifier en lugar de name or id, con la finalidad de permitir
    # cualquiera de estos para la busqueda
    def _normalize_identifier(self, value: str) -> str:
        return str(value).lower().strip()

    def get_pokemon(self, identifier: str) -> dict:
        clean_id = self._normalize_identifier(identifier)
        return self.get(f"pokemon/{clean_id}")

    def get_species(self, identifier: str | int) -> dict:
        clean_id = self._normalize_identifier(str(identifier))
        return self.get(f"pokemon-species/{clean_id}")
