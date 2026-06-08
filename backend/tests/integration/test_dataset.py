import json

import pytest

from backend.app.data.scripts.dataset_generator import OUTPUT_FILE


def test_dataset_file_exists():
    """Verifica que el dataset se haya generado en la ruta correcta"""
    assert OUTPUT_FILE.exists(), f"El dataset no existe en: {OUTPUT_FILE}"


def test_dataset_not_empty_and_volume():
    """Abre el archivo y comprueba que contenga los Pokemon"""
    if not OUTPUT_FILE.exists():
        pytest.skip("El dataset no existe todavía. Ejecuta primero el sript ETL")

    with open(OUTPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), "El dataset debería ser una lista de Python"
    assert len(data) == 1025, f"Se esperaban 1025, pero se encontraron {len(data)}"


def test_dataset_first_pokemon_structure():
    """Comprobamos que el primer elemento tenga la estructura y tipos adecuados"""
    if not OUTPUT_FILE.exists():
        pytest.skip("El dataset no existe todavía. Ejecuta primero el script ETL")

    with open(OUTPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    bulbasaur = data[0]

    # Criterios de aceptación de estructura de datos
    required_keys = [
        "id",
        "name",
        "generation",
        "types",
        "hp",
        "attack",
        "defense",
        "speed",
        "base_exp",
        "sprite",
    ]
    for key in required_keys:
        assert key in bulbasaur, f"Falta la llave '{key}' en el esquema del Pokemon"

    assert bulbasaur["id"] == 1
    assert bulbasaur["name"] == "bulbasaur"
    assert bulbasaur["generation"] == 1
    assert isinstance(bulbasaur["types"], list)
    assert bulbasaur["types"] == ["grass", "poison"]
    assert isinstance(bulbasaur["hp"], int)
    assert isinstance(bulbasaur["base_exp"], int)
    assert isinstance(bulbasaur["sprite"], str)
