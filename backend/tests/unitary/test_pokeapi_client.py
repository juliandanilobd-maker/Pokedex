import requests
import pytest


# Creamos una clase que de una mock response (respuesta simulada) para confirmar el funcionamiento
# de clients, utilizando la funcion monkeypatch de pytest
class MockResponse:
    # Codigo de estado 200 =  ok
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    # En client tenemos el atributo raise_for_status, por tanto en el Mock debe existir
    def raise_for_status(self):
        # Si el codigo es 400 o mas (es decir, error), lanza un Error
        if self.status_code >= 400:
            # response=self evita el error NoneType, la excepcion lleva respuesta dentro
            raise requests.exceptions.HTTPError(response=self)

    def json(self):
        return self.json_data


# Creamos funciones Mock para hacer llamadas en local, unicamente para probar
# que client recibe un json y lo devuelve.
# Usamos args y kwargs, para aceptar cualquier parametro.
def mock_get_success(*args, **kwargs):
    return MockResponse({"name": "pikachu"})


def mock_get_not_found(*args, **kwargs):
    return MockResponse({}, status_code=404)


def test_get_pokemon_success(monkeypatch, pokeapi_client):

    # usamos setattr para evitar llamados a internet, sino a nuestra función mock
    monkeypatch.setattr(requests, "get", mock_get_success)

    result = pokeapi_client.get("pokemon/pikachu")

    assert result["name"] == "pikachu"


# funcion para probar el error 404
def test_get_pokemon_404(monkeypatch, pokeapi_client):

    monkeypatch.setattr(requests, "get", mock_get_not_found)

    with pytest.raises(ValueError) as exc:
        pokeapi_client.get("{endpoint}")

    assert (
        "No se encontro el recurso: {endpoint}."
        "Verifica que el nombre o ID sea correcto." in str(exc.value)
    )
