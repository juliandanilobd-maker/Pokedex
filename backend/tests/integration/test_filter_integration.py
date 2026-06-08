from __future__ import annotations

from unittest.mock import patch

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


# Comprobamos el comportamiento frente a HTTPException
def test_integration_filter_internal_server_error():

    with patch.object(pokemon_routes, "FilterService") as mock_filter:
        mock_instance = mock_filter.return_value

        mock_instance.filter_pokemons.side_effect = Exception(
            "Error interno al procesar el filtrado analítico"
        )

        response = client.get("/api/v1/filter?pokemon_type=grass")
    data = response.json()

    assert response.status_code == 500
    assert "detail" in data
    assert "Error interno al procesar el filtrado analítico" in data["detail"]
