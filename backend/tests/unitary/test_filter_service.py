from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pytest

from backend.app.services.filter_service import FilterService


# Usamos fixture para introducir un set datos controlado
@pytest.fixture
def mock_dataset() -> list[dict[str, Any]]:

    return [
        {
            "id": 1,
            "name": "bulbasaur",
            "types": ["grass", "poison"],
            "generation": 1,
            "attack": 49,
            "defense": 49,
            "hp": 45,
            "base_exp": 64,
            "speed": 45,
        },
        {
            "id": 4,
            "name": "charmander",
            "types": ["fire"],
            "generation": 1,
            "attack": 52,
            "defense": 43,
            "hp": 39,
            "base_exp": 62,
            "speed": 65,
        },
        {
            "id": "152",
            "name": "chikorita",
            "types": ["grass"],
            "generation": 2,
            "attack": 49,
            "defense": 65,
            "hp": 45,
            "base_exp": 64,
            "speed": 45,
        },
    ]


# Comprobamos el filtrado por tipo
def test_filter_by_type(mock_dataset: list[dict[str, Any]]):

    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(pokemon_type=" FIRE ")

    assert len(result) == 1
    assert result[0]["name"] == "charmander"


# Comprobamos el filtrado por generación
def test_filter_by_generation(mock_dataset: list[dict[str, Any]]):

    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(generation=2)

    assert len(result) == 1
    assert result[0]["name"] == "chikorita"


# Probamos la busqueda con filtros combinados
def test_filter_by_combined_stats(mock_dataset: list[dict[str, Any]]):

    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(min_id=2, max_id=165)

    assert len(result) == 2
    assert "bulbasaur" not in [p["name"] for p in result]

    result_defense = service.filter_pokemons(min_defense=49)

    assert len(result_defense) == 2
    assert "charmander" not in [p["name"] for p in result_defense]


def test_filter_by_hp(mock_dataset: list[dict[str, Any]]):

    service = FilterService()

    service._pokemon_data = mock_dataset

    result_hp = service.filter_pokemons(min_hp=45)

    assert len(result_hp) == 2
    assert "charmander" not in [p["name"] for p in result_hp]

    result_base_exp = service.filter_pokemons(min_base_exp=64)
    assert len(result_base_exp) == 2
    assert "charmander" not in [p["name"] for p in result_base_exp]


# Asegura el control de excepciones ante un archivo de datos corrupto
@patch("pathlib.Path.exists")
def test_load_data_corrupt_json(mock_exists: MagicMock):

    mock_exists.return_value = True
    service = FilterService()

    # Simulamos la apertura de un archivo que contiene un string JSON roto
    with patch("builtins.open", mock_open(read_data="{invalid_json:")):
        data = service._load_data()

    assert data == []


# Comprobamos el comportamiento cuando el archivo no existe
def test_load_data_file_not_found():

    service = FilterService()

    with (
        patch("pathlib.Path.exists", return_value=False),
        patch("builtins.print") as mock_print,
    ):
        result = service._load_data()

        assert result == []
        mock_print.assert_any_call(
            f"[FilterService] Archivo no encontrado:{service.data_path}"
        )


# Comprobamos el comportamiento en la excepción de lectura de disco (Permission Error)
def test_load_data_generic_exception():

    service = FilterService()

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", side_effect=OSError("Fallo de lectura físico")),
        patch("builtins.print") as mock_print,
    ):
        result = service._load_data()

        assert result == []
        mock_print.assert_any_call(
            "[FilterService] Error cargando el dataset: Fallo de lectura físico"
        )


# Comprobamos el comportamiento frente a JSON válido pero es un dicionario u objeto
def test_load_data_invalid_format_json():

    service = FilterService()
    mock_bad_json = json.dumps({"status": "ok", "data": []})

    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("builtins.open", mock_open(read_data=mock_bad_json)),
        patch("builtins.print") as mock_print,
    ):
        result = service._load_data()

        assert result == []
        mock_print.assert_any_call("[FilterService] el Dataset no tiene formato válido")
