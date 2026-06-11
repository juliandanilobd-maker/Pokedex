from __future__ import annotations

from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

import backend.app.api.routes as pokemon_routes
from backend.app.services.filter_service import FilterService
from backend.main import app

client = TestClient(app)


# Comprobamos el lazy loading
def test_integration_filter_service_lazy_loaging():

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


# Comprobamos que el reload fuerce una relectura limpia del dataset
def test_integration_filter_service_reload():

    service = FilterService()

    # Forzamos la primera carga
    first_charge = service.pokemon_data

    service.reload()

    assert isinstance(service.pokemon_data, list)
    assert len(first_charge) == len(service.pokemon_data)


# Comprobamos que la petición HTTP filtra correctamente el JSON real
def test_integration_filter_endpoint_with_local_json():

    response = client.get("/api/v1/filter?pokemon_type=water&min_attack=40")

    data = response.json()

    if len(data) > 0:
        for pokemon in data:
            assert "water" in pokemon.get("types", [])
            assert pokemon.get("attack", 0) >= 40

    assert response.status_code == 200
    assert isinstance(data, list)


# Comprobamos el comportamiento frente a criterios que no coincide con ningún Pokemon
def test_integration_filter_endpoint_empty_results():

    response = client.get("/api/v1/filter?min_attack=999&min_speed=999")

    data = response.json()

    assert response.status_code == 200
    assert data == []


# Comprobamos que se captura un ValueError del servicio por el catch de la ruta
# y lanza un 404
def test_integration_filter_not_found():

    with patch.object(pokemon_routes, "FilterService") as mock_filter:
        mock_instance = mock_filter.return_value

        mock_instance.filter_pokemons.side_effect = ValueError(
            "El tipo especificado no existe en el dataset"
        )

        response = client.get("/api/v1/filter?pokemon_type=missing")
        data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in data
    assert "El tipo especificado no existe en el dataset" in data["detail"]


# Comprobamos la captura de un fallo interno del servidor
def test_integration_filter_generic_exception():

    with patch.object(pokemon_routes, "FilterService") as mock_filter:
        mock_instance = mock_filter.return_value

        mock_instance.filter_pokemons.side_effect = Exception(
            "Fallo crítico del servidor"
        )

        response = client.get("/api/v1/filter?pokemon_type=missing")
        data = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert (
        "Error interno al procesar el motor analítico: Fallo crítico del servidor"
        in data["detail"]
    )
