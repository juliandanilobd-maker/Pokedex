from __future__ import annotations

import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from backend.app.data.scripts.dataset_generator import (
    create_session,
    dataset_pokemon,
    get_generation_by_id,
    load_dataset,
)


# Comprobamos la lógica de generaciones
@pytest.mark.parametrize(
    ("pokemon_id", "expected_gen"),
    [
        (1, 1),
        (151, 1),
        (152, 2),
        (251, 2),
        (386, 3),
        (493, 4),
        (649, 5),
        (721, 6),
        (809, 7),
        (898, 8),
        (899, 9),
        (1025, 9),
    ],
)

# Verificamos el cálculo matemático por generaciones
def test_get_generation_by_id(pokemon_id: int, expected_gen: int):
    assert get_generation_by_id(pokemon_id) == expected_gen


# Comprobamos que la sesión se configure con adaptadores HTTP y reintentos
def test_create_session():
    session = create_session()

    assert session.adapters is not None
    assert "https://" in session.adapters


# Comprobamos que el load_dataset devuelva la lista si el archivo JSON existe
def test_load_dataset_success():
    mock_data = [{"id": 1, "name": "bulbasaur"}]

    json_content = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=json_content)):
        result = load_dataset()
        assert result == mock_data


# Comprobamos que si el dataset no existe, se capture el error
def test_load_dataset_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_dataset()
        assert result == []


# Comprobamos el ciclo de vida completo del script ETL
def test_dataset_pokemon_execution_with_mocks():

    mock_index_response = MagicMock()
    mock_index_response.json.return_value = {
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
            {"name": "charmander", "url": "https://pokeapi.co/api/v2/pokemon/4/"},
        ]
    }

    mock_pokemon_response = MagicMock()
    mock_pokemon_response.json.return_value = {
        "id": 1,
        "name": "bulbasaur",
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 45},
            {"stat": {"name": "attack"}, "base_stat": 49},
            {"stat": {"name": "defense"}, "base_stat": 49},
            {"stat": {"name": "speed"}, "base_stat": 45},
        ],
        "sprites": {
            "other": {
                "official-artwork": {"front_default": "http://image.url/bulbasaur.png"}
            }
        },
        "types": [{"type": {"name": "grass"}}],
        "base_experience": 64,
    }

    target_session = "backend.app.data.scripts.dataset_generator.create_session"

    with patch(target_session) as mock_session:
        session_instance = mock_session.return_value

        session_instance.get.side_effect = [
            mock_index_response,
            mock_pokemon_response,
            mock_pokemon_response,
        ]

        with patch("builtins.open", mock_open()), patch("pathlib.Path.mkdir"):
            dataset_pokemon()

        assert session_instance.get.call_count == 3


# Comprobamos el comportamiento frente a errores de API
def test_dataset_pokemon_api_critical_error():
    target_session = "backend.app.data.scripts.dataset_generator.create_session"

    with patch(target_session) as mock_session:
        session_instance = mock_session.return_value
        session_instance.get.side_effect = Exception("Conexión rechazada por el host")
        dataset_pokemon()

        assert session_instance.get.call_count == 1


# Comprovamos el except cuando falla una request procesando single_pokemon
def test_process_single_pokemon_exception():

    from backend.app.data.scripts.dataset_generator import process_single_pokemon

    mock_session = MagicMock()
    mock_session.get.side_effect = Exception("Error de red simulado")

    entry = {"name": "skeledirge", "url": "https://pokeapi.co/api/v2/pokemon/911/"}

    resultado = process_single_pokemon(entry, mock_session)

    assert resultado is None


# Comprobamos el comportamiento cuando el procesamiento llega a los 100 Pokemons
def test_Dataset_pokemon_progress_print():
    mock_results = [{"name": f"poke_{i}", "url": f"http://api/{i}"} for i in range(101)]

    mock_index_response = MagicMock()
    mock_index_response.json.return_value = {"results": mock_results}

    target_session = "backend.app.data.scripts.dataset_generator.create_session"

    with patch(target_session) as mock_session:
        session_instance = mock_session.return_value

        mock_poke = MagicMock()
        mock_poke.json.return_value = {
            "id": 1,
            "name": "test",
            "stats": [],
            "types": [],
            "base_experience": 10,
        }

        session_instance.get.side_effect = [mock_index_response] + [mock_poke] * 101

        with patch("builtins.open", mock_open()), patch("pathlib.Path.mkdir"):
            dataset_pokemon()

        assert session_instance.get.call_count == 102


# Comprobamos el exception si el escritor del archivo falla
def test_dataset_pokemon_write_exception():

    mock_index_response = MagicMock()
    mock_index_response.json.return_value = {"results": []}

    target_session = "backend.app.data.scripts.dataset_generator.create_session"

    with patch(target_session) as mock_session:
        session_instance = mock_session.return_value
        session_instance.get.return_value = mock_index_response

        with patch(
            "pathlib.Path.mkdir", side_effect=Exception("Permiso de escritura denegado")
        ):
            dataset_pokemon()

        assert session_instance.get.call_count == 1
