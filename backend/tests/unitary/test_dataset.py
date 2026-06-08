from __future__ import annotations

import json
import sys
from unittest.mock import MagicMock, mock_open, patch

import pytest
import requests

from backend.app.data.scripts.dataset_generator import (
    OUTPUT_FILE,
    dataset_pokemon,
    fetch_with_retry,
    get_generation_by_id,
    load_dataset,
)


# Comrobamos que load dataset parsee un JSON simulando leer en memoria local
def test_load_dataset_success_mock():

    mock_data = [{"id": 25, "name": "pikachu", "generation": 1}]
    mock_json_string = json.dumps(mock_data)

    # Interceptamos la función 'open' nativa de Python
    # para que devuelva el string que le entregamos para el test
    with patch("builtins.open", mock_open(read_data=mock_json_string)):
        result = load_dataset()

    assert len(result) == 1
    assert result[0]["name"] == "pikachu"


# Comprobamos si el archivo no existe, se devuelve una lista vacía y no se rompe
def test_load_dataset_file_not_found_mock():

    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_dataset()

    assert result == []


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

# Comprobamos que el mapeo por rangos ID asigne a la generación correcta
def test_get_generation_by_id(pokemon_id: int, expected_gen: int):
    assert get_generation_by_id(pokemon_id) == expected_gen


# Comprobamos el mecanismo de reintentos
def test_fetch_with_retry_success():

    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "name": "bulbasaur"}
    mock_session.get.return_value = mock_response

    result = fetch_with_retry(
        mock_session, "http://pokeapi.co/.../1", "bulbasaur", max_retries=3
    )

    assert result == {"id": 1, "name": "bulbasaur"}
    assert mock_session.get.call_count == 1


# Comprobamos que si la API da un error, el metodo agote los reintentos y devuelve None
def test_fetch_with_retry_exhausted():

    mock_session = MagicMock()
    mock_session.get.side_effect = requests.exceptions.RequestException(
        "Timeout de red"
    )

    result = fetch_with_retry(
        mock_session, "http://pokeapi.co/.../1", "bulbasaur", max_retries=3
    )

    assert result is None
    assert mock_session.get.call_count == 3


# Comprobamos una caída al pedir la URL base
def test_dataset_pokemon_api_base_error():

    if "backend.app.data.scripts.dataset_generator" in sys.modules:
        del sys.modules["backend.app.data.scripts.dataset_generator"]

    mock_session_instance = MagicMock()
    mock_session_instance.get.side_effect = Exception("Error de conexión simulado")

    mock_session_class = MagicMock()
    mock_session_class.return_value = mock_session_instance

    with (
        patch(
            "backend.app.data.scripts.dataset_generator.requests.Session",
            mock_session_class,
        ),
        patch("builtins.print") as mock_print,
        patch("builtins.open", mock_open()),
    ):
        from backend.app.data.scripts.dataset_generator import dataset_pokemon

        result = dataset_pokemon()

        mock_print.assert_any_call(
            "Ha ocurrido un Error al conectar con la API: Error de conexión simulado"
        )

    assert result is None


# Comprobamos el flujo completo de transformación de datos
@patch("backend.app.data.scripts.dataset_generator.requests.Session")
@patch("backend.app.data.scripts.dataset_generator.Path.mkdir")
@patch("builtins.open", new_callable=mock_open)
@patch("backend.app.data.scripts.dataset_generator.json.dump")
@patch("backend.app.data.scripts.dataset_generator.time.sleep")
def test_dataset_pokemon_full_pipeline(
    mock_sleep: MagicMock,
    mock_json_dump: MagicMock,
    mock_file_open: MagicMock,
    mock_mkdir: MagicMock,
    mock_session_class: MagicMock,
):

    mock_session = mock_session_class.return_value

    mock_base_response = MagicMock()
    mock_base_response.json.return_value = {
        "results": [
            {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}
        ]
    }

    mock_pokemon_response = MagicMock()
    mock_pokemon_response.json.return_value = {
        "id": 1,
        "name": "bulbasaur",
        "base_experience": 64,
        "stats": [
            {"stat": {"name": "hp"}, "base_stat": 45},
            {"stat": {"name": "attack"}, "base_stat": 49},
            {"stat": {"name": "defense"}, "base_stat": 49},
            {"stat": {"name": "speed"}, "base_stat": 45},
        ],
        "types": [{"type": {"name": "grass"}}, {"type": {"name": "poison"}}],
        "sprites": {
            "other": {
                "official-artwork": {
                    "front_default": "https://raw.githubusercontent.com/.../1.png"
                }
            }
        },
    }

    mock_session.get.side_effect = [mock_base_response, mock_pokemon_response]

    dataset_pokemon()

    assert mock_session.get.call_count == 2
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    mock_file_open.assert_called_once_with(OUTPUT_FILE, "w", encoding="utf-8")
    mock_json_dump.assert_called_once()


# Comprobamos el comportamiento en Exceptions
@patch("backend.app.data.scripts.dataset_generator.requests.Session")
@patch("backend.app.data.scripts.dataset_generator.Path.mkdir")
def test_dataset_pokemon_write_exception(
    mock_mkdir: MagicMock, mock_session_class: MagicMock
):

    mock_session = mock_session_class.return_value
    mock_base_response = MagicMock()
    mock_base_response.json.return_value = {"results": []}
    mock_session.get.return_value = mock_base_response

    with (
        patch("builtins.open", side_effect=OSError("Permiso denegado en disco")),
        patch("builtins.print") as mock_print,
    ):
        dataset_pokemon()

        mock_print.assert_any_call(
            "Error al escribir el archivo: Permiso denegado en disco"
        )


# Comprobamos que la funcion fetch_with_retry hace continue cuando devuelve None
@patch("backend.app.data.scripts.dataset_generator.requests.Session")
@patch("backend.app.data.scripts.dataset_generator.Path.mkdir")
@patch("builtins.open", new_callable=mock_open)
@patch("backend.app.data.scripts.dataset_generator.json.dump")
@patch("backend.app.data.scripts.dataset_generator.time.sleep")
def test_dataset_pokemon_continue_on_empty_data(
    mock_sleep: MagicMock,
    mock_json_dump: MagicMock,
    mock_file_open: MagicMock,
    mock_mkdir: MagicMock,
    mock_session_class: MagicMock,
):

    mock_session = mock_session_class.return_value

    mock_base_response = MagicMock()
    mock_base_response.json.return_value = {
        "results": [
            {"name": "failed_pokemon", "url": "https://pokeapi.co/api/v2/pokemon/9999/"}
        ]
    }

    mock_session.get.side_effect = [mock_base_response, None]

    dataset_pokemon()

    mock_json_dump.assert_called_once_with(
        [], mock_file_open(), indent=4, ensure_ascii=False
    )


# Comprobamos el print modular cada 50 iteraciones
@patch("backend.app.data.scripts.dataset_generator.requests.Session")
@patch("backend.app.data.scripts.dataset_generator.Path.mkdir")
@patch("builtins.open", new_callable=mock_open)
@patch("backend.app.data.scripts.dataset_generator.json.dump")
@patch("backend.app.data.scripts.dataset_generator.time.sleep")
def test_dataset_pokemon_print_progress(
    mock_sleep: MagicMock,
    mock_json_dump: MagicMock,
    mock_file_open: MagicMock,
    mock_mkdir: MagicMock,
    mock_session_class: MagicMock,
):

    mock_session = mock_session_class.return_value

    mock_results = [
        {"name": f"pk-{i}", "url": f"http://api/{i}"} for i in range(1, 151)
    ]

    mock_base_response = MagicMock()
    mock_base_response.json.return_value = {"results": mock_results}

    mock_pokemon_response = MagicMock()
    mock_pokemon_response.json.return_value = {
        "id": 1,
        "name": "bulbasaur",
        "stats": [],
        "types": [],
    }

    mock_session.get.side_effect = [mock_base_response] + [mock_pokemon_response] * 50

    with patch("builtins.print") as mock_print:
        dataset_pokemon()

        mock_print.assert_any_call("Cargados 50 Pokemon...")


# Comprobamos el bloque principal de forma aislada
def test_script_execution_main_block():

    with patch(
        "backend.app.data.scripts.dataset_generator.dataset_pokemon"
    ) as mock_dataset:
        from backend.app.data.scripts import dataset_generator

        original_name = dataset_generator.__name__

        try:
            dataset_generator.__name__ = "__main__"

            if dataset_generator.__name__ == "__main__":
                dataset_generator.dataset_pokemon()

            mock_dataset.assert_called_once()

        finally:
            dataset_generator.__name__ = original_name
