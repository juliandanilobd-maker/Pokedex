"""En este módulo se encuentra el cliente del frontend que se comunica con el
cliente y consume los diferentes endpoints para traer la info al frontend"""

from __future__ import annotations

from typing import Any

import requests

# CREAMOS EXCEPCIONES PERSONALIZADAS DE DOMINIO


# Excepción para todos los errores de cliente HTTP
class BackendClientError(Exception):
    pass


# Excepción para cuando el servidor FastAPI está apagado o inaccesible
class BackendConnectionError(BackendClientError):
    pass


# Excepción para cuando el backend excede el tiempo máximo de respuesta
class BackendTimeoutError(BackendClientError):
    pass


# Excepción para códigos de estado HTTP
class BackendHTTPError(BackendClientError):
    def __init__(self, status_code: int, detail: str) -> None:

        super().__init__(f"Error HTTP {status_code}: {detail}")
        self.status_code = status_code


# Cliente encargado de la comunicación con el backend
class BackendClient:
    BASE_URL = "http://localhost:8000/api/v2"
    TIMEOUT = 10

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:

        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout as e:
            raise BackendTimeoutError("El servidor tardó demasiado en responder") from e

        except requests.exceptions.ConnectionError as e:
            raise BackendConnectionError(
                "No se pudo establecer conexión con el backend"
            ) from e

        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                status_code = e.response.status_code

                try:
                    detail = e.response.json().get("detail", e.strerror)

                except Exception:
                    detail = e.response.text or str(e)

            else:
                status_code = 500
                detail = "El servidor no envó ninguna respuesta"

            raise BackendHTTPError(status_code, detail) from e

        except Exception as e:
            raise BackendClientError(f"Error inesperado en el cliente: {e}") from e

    # Implementamos la verificación del estado del backend
    def check_health(self) -> bool:
        """Esta función retorna un valor booleano:
        True si el backend nos devuelve un 200 Ok, y
        False en caso contrario.
        """
        url = self.BASE_URL.replace("/api/v2", "/health")
        try:
            response = requests.get(url, timeout=3)

        except Exception:
            return False

        else:
            return response.status_code == 200

    def get_pokemon(self, identifier: str | str) -> dict[str, Any]:
        result = self._get(f"/pokemon/{str(identifier).lower().strip()}")

        return result if isinstance(result, dict) else {}

    def get_evolution(self, identifier: str | str) -> dict[str, Any]:
        result = self._get(f"/pokemon/{str(identifier).lower().strip()}/evolution")

        return result if isinstance(result, dict) else {}

    def filter_pokemons(self, cleaned_params: dict[str, Any]) -> list[dict[str, Any]]:

        cleaned_params = {
            k: v
            for k, v in cleaned_params.items()
            if v is not None and v != 0 and v != ""
        }

        result = self._get("/filter", params=cleaned_params)

        return result if isinstance(result, list) else []

    def get_effectiveness(self, identifier: str | int) -> dict[str, Any]:
        result = self._get(f"/pokemon/{str(identifier).lower().strip()}/effectiveness")

        return result if isinstance(result, dict) else {}

    def get_pokemon_full_detail(self, identifier: str | int) -> dict[str, Any]:
        result = self._get(f"/pokemon/{str(identifier).lower().strip()}/full-detail")
        return result if isinstance(result, dict) else {}
