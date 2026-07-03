from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from backend.app.dependencies.dependencias import get_filter_service
from backend.app.services.filter_service import FilterService
from backend.main import app


# Configuramos un fixture con un mock service para comprobar errores en el filtrado
@pytest.fixture
def mock_filter_service():

    mock = MagicMock()

    app.dependency_overrides[get_filter_service] = lambda: mock

    yield mock

    del app.dependency_overrides[get_filter_service]


client = TestClient(app)


def test_integration_filter_service_lazy_loaging():
    """Este test comprueba el lazy loading en el servicio de busqueda por filtros"""
    service = FilterService()

    # Iniciamos con el service vacío
    assert service._pokemon_data is None

    # Al utilizar el servicio, se inicia la lectura del JSON
    data = service.pokemon_data

    assert isinstance(data, list)

    # Si el dataset existe y tiene datos, comprobamos que no este vacío
    if len(data) > 0:
        assert "id" in data[0]
        assert "name" in data[0]


def test_integration_filter_service_reload():
    """Este test comprueba que si se busca un nuevo filtro, se recargue y se fuerce una
    relectura limpia del dataset, para asegurar la entrega de datos correctos en cada
    busqueda"""
    service = FilterService()

    # Forzamos la primera carga
    first_charge = service.pokemon_data

    service.reload()

    assert isinstance(service.pokemon_data, list)
    assert len(first_charge) == len(service.pokemon_data)


def test_integration_filter_endpoint_with_local_json():
    """Este test comprueba que la petición HTTP devuelve el JSON unicamente de los
    parametros solicitados"""
    response = client.get("/api/v2/filter?pokemon_type=water&min_attack=40")

    data = response.json()

    if len(data) > 0:
        for pokemon in data:
            assert "water" in pokemon.get("types", [])
            assert pokemon.get("attack", 0) >= 40

    assert response.status_code == 200
    assert isinstance(data, list)


def test_integration_filter_endpoint_empty_results():
    """Este test comprueba la captura de un error frente a filtros que no coinciden con
    ningún Pokemon"""
    response = client.get("/api/v2/filter?min_attack=999&min_speed=999")

    data = response.json()

    assert response.status_code == 200
    assert data == []


def test_integration_filter_not_found(mock_filter_service):
    """Este test comprueba que se captura el Value Error y se lanza un 404 not Found"""
    mock_filter_service.filter_pokemons.side_effect = ValueError(
        "El tipo especificado no existe en el dataset"
    )

    response = client.get("/api/v2/filter?pokemon_type=missing")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in data
    assert "El tipo especificado no existe en el dataset" in data["detail"]


def test_integration_filter_generic_exception(mock_filter_service):
    """Este test comprueba que se captura el Exception y se lanza un 500 Fallo del
    servidor"""
    mock_filter_service.filter_pokemons.side_effect = Exception(
        "Fallo crítico del servidor"
    )

    response = client.get("/api/v2/filter?pokemon_type=missing")
    data = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        "Error interno al procesar el motor analítico: Fallo crítico del servidor"
        in data["detail"]
    )
