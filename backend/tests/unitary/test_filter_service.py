from __future__ import annotations

from typing import Any

import pytest

from backend.app.services.filter_service import FilterService


@pytest.fixture
def mock_dataset() -> list[dict[str, Any]]:
    """Usamos fixture para introducir un set datos controlado"""
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


def test_filter_by_type(mock_dataset: list[dict[str, Any]]):
    """Comprobamos el filtrado por tipo"""
    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(pokemon_type=" FIRE ")

    assert len(result) == 1
    assert result[0]["name"] == "charmander"


def test_filter_by_generation(mock_dataset: list[dict[str, Any]]):
    """Comprobamos el filtrado por generación"""
    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(generation=2)

    assert len(result) == 1
    assert result[0]["name"] == "chikorita"


def test_filter_by_combined_stats(mock_dataset: list[dict[str, Any]]):
    """Probamos la busqueda con filtros combinados"""
    service = FilterService()

    service._pokemon_data = mock_dataset

    result = service.filter_pokemons(min_id=2, max_id=165)

    assert len(result) == 2
    assert "bulbasaur" not in [p["name"] for p in result]

    result_defense = service.filter_pokemons(min_defense=49)

    assert len(result_defense) == 2
    assert "charmander" not in [p["name"] for p in result_defense]
