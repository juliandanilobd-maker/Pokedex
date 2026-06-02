"""
Este modulo proporciona una clase que encapsula las peticiones HTTP a la API,
maneja errores, implementa rate limiting basico y utiliza cache para evitar
peticiones repetidas.
"""

import requests
import time

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

        self.base_url = settings.POKEPI_BASE_URL
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

        # Incluimos: primero busqueda en cache
        cached = self.cache.get(url)
        if cached is not None:
            return cached

        # usamos rate limit
        self._rate_limit()

        # Se realiza la peticion
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

    # Creamos una funcion que nos permita construir la URL
    def _build_url(self, endpoint: str) -> str:

        if endpoint.startswith("http"):
            # Añadimos raise ValueError para evitar URLs externas
            if not endpoint.startswith(self.base_url):
                raise ValueError("URL externa no permitida")

            return endpoint

        # Construir URL completa
        url = f"{self.base_url.rstrip('/')}/{endpoint.strip('/')}"
        return url

    # Implementamos rate limiting básico
    def _rate_limit(self):

        # Calculamos el tiempo transcurrido entre el momento actual y la última request
        elapsed = time.time() - self._last_request_time

        # Si el tiempo calculado es menor al establecido en config, se frena el tiempo que resta de rate limit que establecimos en config
        if elapsed < settings.MIN_REQUEST_DELAY:
            time.sleep(settings.MIN_REQUEST_DELAY - elapsed)

    # A continuacion definimos funciones que nos entreguen los pokemones,
    # listas, especies, etc que ya solicitamos de manera limpia

    # Usamos identifier en lugar de name or id, con la finalidad de permitir cualquiera de estos para la busqueda
    # Volvemos a identifier a minusculas y elimina los espacios en blanco
    def normaliza_identifier(self, value: str) -> str:
        return str(value).lower().strip()

    # Toma el identifier corregido y lo añade al endpoint para buscar un
    # pokemon en especifico.
    def get_pokemon(self, identifier: str) -> dict:
        return self.get(f"pokemon/{identifier}")
