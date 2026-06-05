import json
from unittest.mock import mock_open, patch

from backend.app.data.scripts.dataset_generator import load_dataset


def test_load_dataset_success_mock():
    """Comprobamos que load_dataset parsee un JSON simulando leer en memoria local"""
    mock_data = [{"id": 25, "name": "pikachu", "generation": 1}]
    mock_json_string = json.dumps(mock_data)

    # Interceptamos la función 'open' nativa de Python
    # para que devuelva el string que le entregamos para el test
    with patch("builtins.open", mock_open(read_data=mock_json_string)):
        result = load_dataset()

    assert len(result) == 1
    assert result[0]["name"] == "pikachu"


def test_load_dataset_file_not_found_mock():
    """Comprobamos si el archivo no existe, se devuelve una lista vacía y no se rompe"""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_dataset()

    assert result == []
