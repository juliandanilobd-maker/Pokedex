import time

import httpx
import pytest

from backend.app.core.config import settings


# Creamos una clase que de una mock response (respuesta simulada) para confirmar
# el funcionamiento de clients, utilizando la funcion monkeypatch de pytest
class MockResponse:
    # Codigo de estado 200 =  ok
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    # En client tenemos el atributo raise_for_status, por tanto en el Mock debe existir
    def raise_for_status(self):
        # Si el codigo es 400 o mas (es decir, error), lanza un Error
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://pokeapi.co/api/v2/test")
            response = httpx.Response(self.status_code, request=request)

            raise httpx.HTTPStatusError(
                f"{self.status_code} Error", request=request, response=response
            )

    def json(self):
        return self.json_data


# Creamos funciones Mock para hacer llamadas en local, unicamente para probar
# que client recibe un json y lo devuelve.
# Usamos args y kwargs, para aceptar cualquier parametro.
async def mock_get_success(*args, **kwargs):
    return MockResponse({"name": "pikachu"})


async def mock_get_not_found(*args, **kwargs):
    return MockResponse({}, status_code=404)


async def test_get_pokemon_success(monkeypatch, pokeapi_client):
    """Este test comprueba las llamadas tipo get que realiza nuestro client"""
    # usamos setattr para evitar llamados a internet, sino a nuestra función mock
    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_success)

    result = await pokeapi_client.get("pokemon/pikachu")

    assert result["name"] == "pikachu"


async def test_get_pokemon_404(monkeypatch, pokeapi_client):
    """Este test comprueba la captura de un error 404"""
    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_not_found)

    with pytest.raises(ValueError) as exc:
        await pokeapi_client.get("{endpoint}")

    assert (
        "No se encontro el recurso: {endpoint}."
        "Verifica que el nombre o ID sea correcto." in str(exc.value)
    )


async def test_pokeapi_client_raises_value_error_on_404(monkeypatch, pokeapi_client):
    """Este test comprueba la captura de un HTTP Error"""
    request_404 = httpx.Request(
        "GET", "https://pokeapi.co/api/v2/pokemon/invalid-pokemon"
    )
    response_404 = httpx.Response(404, request=request_404)

    def mock_get_404(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "Not Found", request=request_404, response=response_404
        )

    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_404)

    with pytest.raises(ValueError) as exc:
        await pokeapi_client.get("pokemon/invalid-pokemon")

    assert "No se encontro el recurso" in str(exc.value)


async def test_pokeapi_client_re_raises_other_http_errors(monkeypatch, pokeapi_client):
    """Este test captura el manejo del exception"""
    request = httpx.Request(
        "GET",
        "https://pokeapi.co/api/v2/pokemon/test",
    )

    response = httpx.Response(
        500,
        request=request,
    )

    async def mock_get_500(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "500 Internal Server Error", request=request, response=response
        )

    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_500)

    with pytest.raises(httpx.HTTPStatusError):
        await pokeapi_client.get("pokemon/pikachu")


async def test_get_pokemon_connection_error(monkeypatch, pokeapi_client):
    """Este test comprueba la captura de un error de conexión"""

    async def mock_get_connection_failure(*args, **kwargs):
        raise httpx.ConnectError("Simulated connection failure")

    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_connection_failure)

    with pytest.raises(ConnectionError) as exc:
        await pokeapi_client.get("pokemon/pikachu")

    assert "No se pudo conectar a la PokeAPI." in str(exc.value)


async def test_pokeapi_client_timeout_error(monkeypatch, pokeapi_client):
    """Este test comprueba la captura de un error de timeout de la respuesta"""

    async def mock_get_timeout(*args, **kwargs):
        raise httpx.TimeoutException("Request timed out")

    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_timeout)

    with pytest.raises(TimeoutError) as exc:
        await pokeapi_client.get("pokemon/pikachu")

    assert "La peticion a la PokeAPI tardo demasiado. " in str(exc.value)


async def test_get_pokemon_rejects_external_url(pokeapi_client):
    """Este test comprueba el manejo de errores en caso de un URL erronea"""
    # Definimos una URL externa no permitida
    external_url = "http://google.com/api/v2/pokemon/pikachu"

    with pytest.raises(ValueError) as exc:
        await pokeapi_client.get(external_url)

    assert "URL externa no permitida" in str(exc.value)


async def test_rate_limi_triggers_sleep(monkeypatch, pokeapi_client):
    """Este test comprueba el tiempo entre requests"""
    # Hacemos un mock get para que responda rápido
    monkeypatch.setattr(pokeapi_client.client, "get", mock_get_success)

    # Forzamos la última petición registrada como este momento
    pokeapi_client._last_request_time = time.time()

    # Guardamos el tiempo exacto antes de lanzar la nueva petición
    start_time = time.time()

    # Ejecutamos la segunda petición, con un tiempo elapsed casi 0
    await pokeapi_client.get("pokemon/pikachu")

    end_time = time.time()
    total_execution_time = end_time - start_time

    # Verificamos que se haya mandado a sleep
    assert total_execution_time >= (settings.MIN_REQUEST_DELAY - 0.1)


def test_normalize_identifier(monkeypatch, pokeapi_client):
    """Este test comprueba la normalización correcta del identifier = {nombre o ID}"""
    dirty_identifier = "     PiKaCHu\n   "

    result = pokeapi_client._normalize_identifier(dirty_identifier)

    assert result == "pikachu"
