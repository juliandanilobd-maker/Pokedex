from __future__ import annotations

from unittest.mock import patch

import pytest

from backend.app.models.pokemon_models import SimulatorResult
from backend.app.services.simulator_service import SimulatorService

FAKE_DATASET = [
    {
        "id": 4,
        "name": "charmander",
        "types": ["fire"],
        "generation": 1,
        "hp": 39,
        "attack": 52,
        "defense": 43,
        "speed": 65,
        "base_exp": 62,
    },
    {
        "id": 5,
        "name": "charmeleon",
        "types": ["fire"],
        "generation": 1,
        "hp": 58,
        "attack": 64,
        "defense": 58,
        "speed": 80,
        "base_exp": 142,
    },
    {
        "id": 6,
        "name": "charizard",
        "types": ["fire", "flying"],
        "generation": 1,
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "speed": 100,
        "base_exp": 240,
    },
    {
        "id": 155,
        "name": "cyndaquil",
        "types": ["fire"],
        "generation": 2,
        "hp": 39,
        "attack": 52,
        "defense": 43,
        "speed": 65,
        "base_exp": 65,
    },
    {
        "id": 156,
        "name": "quilava",
        "types": ["fire"],
        "generation": 2,
        "hp": 58,
        "attack": 64,
        "defense": 58,
        "speed": 80,
        "base_exp": 142,
    },
    {
        "id": 255,
        "name": "torchic",
        "types": ["fire"],
        "generation": 3,
        "hp": 45,
        "attack": 60,
        "defense": 40,
        "speed": 45,
        "base_exp": 62,
    },
    {
        "id": 7,
        "name": "squirtle",
        "types": ["water"],
        "generation": 1,
        "hp": 44,
        "attack": 48,
        "defense": 65,
        "speed": 43,
        "base_exp": 63,
    },
    {
        "id": 8,
        "name": "wartortle",
        "types": ["water"],
        "generation": 1,
        "hp": 59,
        "attack": 63,
        "defense": 80,
        "speed": 58,
        "base_exp": 142,
    },
    {
        "id": 186,
        "name": "politoed",
        "types": ["water"],
        "generation": 2,
        "hp": 90,
        "attack": 75,
        "defense": 75,
        "speed": 70,
        "base_exp": 225,
    },
    {
        "id": 16,
        "name": "pidgey",
        "types": ["normal", "flying"],
        "generation": 1,
        "hp": 40,
        "attack": 45,
        "defense": 40,
        "speed": 56,
        "base_exp": 50,
    },
    {
        "id": 1,
        "name": "bulbasaur",
        "types": ["grass", "poison"],
        "generation": 1,
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "speed": 45,
        "base_exp": 64,
    },
    {
        "id": 2,
        "name": "ivysaur",
        "types": ["grass", "poison"],
        "generation": 1,
        "hp": 60,
        "attack": 62,
        "defense": 63,
        "speed": 60,
        "base_exp": 142,
    },
    {
        "id": 182,
        "name": "bellossom",
        "types": ["grass"],
        "generation": 2,
        "hp": 75,
        "attack": 80,
        "defense": 85,
        "speed": 50,
        "base_exp": 221,
    },
    {
        "id": 252,
        "name": "treecko",
        "types": ["grass"],
        "generation": 3,
        "hp": 40,
        "attack": 45,
        "defense": 35,
        "speed": 70,
        "base_exp": 62,
    },
]


def make_simulator() -> SimulatorService:
    return SimulatorService(dataset_loader=lambda: FAKE_DATASET)


def test_build_type_ranges_returns_dict_with_types():
    """Este test comprueba que en la simulación se devuelve un diccionario con los
    tipos"""
    service = make_simulator()
    ranges = service._build_type_ranges()
    assert isinstance(ranges, dict)
    assert "fire" in ranges


def test_build_type_ranges_stats():
    """Este test comprueba que la simulación contiene las stats esperadas"""
    service = make_simulator()
    ranges = service._build_type_ranges()
    assert "hp" in ranges["fire"]
    assert "mean" in ranges["fire"]["hp"]
    assert "std" in ranges["fire"]["hp"]


def test_build_type_ranges_dataset_empty_returns_dict_empty():
    """Este test comprueba que con un dataset vacío se devuelve un diccionario vacío"""
    service = SimulatorService(dataset_loader=lambda: [])
    ranges = service._build_type_ranges()
    assert ranges == {}


def test_build_type_ranges_dataset_corrupt_returns_dict_empty():
    """Este test comprueba que frente a un dataset corrupto también se devuelve un
    diccionario vacío"""

    def loader_roto():
        raise RuntimeError("Error de lectura")

    service = SimulatorService(dataset_loader=loader_roto)
    ranges = service._build_type_ranges()
    assert ranges == {}


def test_sample_stat_in_valid_range():
    """Este test comprueba que se crean stats dentro del rango válido"""
    from backend.app.services.simulator_service import STAT_MAX, STAT_MIN

    service = make_simulator()
    ranges = service._build_type_ranges()
    for _ in range(20):
        value = service._sample_stat("hp", "fire", ranges)
        assert STAT_MIN <= value <= STAT_MAX


def test_sample_stat_type_no_range_uses_fallback():
    """Este test comprueba el uso de stats fallback en caso de no poder generarlos"""
    from backend.app.services.simulator_service import STAT_MAX, STAT_MIN

    service = make_simulator()
    value = service._sample_stat("hp", "dragon", {})
    assert STAT_MIN <= value <= STAT_MAX


def test_generate_n_zero_raises_error(tmp_path):
    """Este test comprueba que si se envía 0 como valor para n se captura un error"""
    service = make_simulator()
    with (
        patch(
            "backend.app.services.simulator_service.SYNTHETIC_CSV",
            tmp_path / "test.csv",
        ),
        pytest.raises(ValueError, match="entre 1 y 1000"),
    ):
        service.generate(n=0)


def test_generate_n_mayor_1000_lanza_error(tmp_path):
    """Este test comprueba que si se envia para n un valor mayor a 1000 se captura un
    error"""
    service = make_simulator()
    with (
        patch(
            "backend.app.services.simulator_service.SYNTHETIC_CSV",
            tmp_path / "test.csv",
        ),
        pytest.raises(ValueError, match="entre 1 y 1000"),
    ):
        service.generate(n=1001)


def test_generate_invalid_type_raises_error(tmp_path):
    """Este test comprueba que si se usa un tipo invalido se captura un error"""
    service = make_simulator()
    with (
        patch(
            "backend.app.services.simulator_service.SYNTHETIC_CSV",
            tmp_path / "test.csv",
        ),
        pytest.raises(ValueError, match="no válido"),
    ):
        service.generate(pokemon_type="faketype")


def test_generate_gen_0_raises_error(tmp_path):
    """Este test comprueba que si para generación se envía 0 se captura un error"""
    service = make_simulator()
    with (
        patch(
            "backend.app.services.simulator_service.SYNTHETIC_CSV",
            tmp_path / "test.csv",
        ),
        pytest.raises(ValueError, match="1-9"),
    ):
        service.generate(generation=0)


def test_generate_generation_greater_than_9_raises_error(tmp_path):
    """Este test comprueba que si para generación se usa una valor mayor a 9 se captura
    un error"""
    service = make_simulator()
    with (
        patch(
            "backend.app.services.simulator_service.SYNTHETIC_CSV",
            tmp_path / "test.csv",
        ),
        pytest.raises(ValueError, match="1-9"),
    ):
        service.generate(generation=10)


def test_generate_return_simulator_result(tmp_path):
    """Este test comprueba que se retorna correctamente la simulación"""
    service = make_simulator()
    with patch(
        "backend.app.services.simulator_service.SYNTHETIC_CSV", tmp_path / "out.csv"
    ):
        result = service.generate(n=5, pokemon_type="fire", generation=1, seed=42)
    assert isinstance(result, SimulatorResult)


def test_generate_creates_file_csv(tmp_path):
    """Este test comprueba que se crea el archivo csv correctamente"""
    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        service.generate(n=3, pokemon_type="water", generation=2, seed=0)
    assert csv_path.exists()


def test_generate_rows_correct(tmp_path):
    """Este test comprueba que se generan la cantidad de filas correctas,
    es decir la cantidad de Pokemon adecuadas"""
    import pandas as pd

    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        result = service.generate(n=5, pokemon_type="fire", generation=1, seed=1)
    df = pd.read_csv(csv_path)
    assert len(df) == 5
    assert result.generated_count == 5


def test_generate_add_rows(tmp_path):
    """Este test comprueba que se añaden filas al archivo si se simulan más Pokemon"""
    import pandas as pd

    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        service.generate(n=3, pokemon_type="fire", generation=1, seed=1)
        service.generate(n=4, pokemon_type="water", generation=2, seed=2)
    df = pd.read_csv(csv_path)
    assert len(df) == 7


def test_generate_total_accumulated(tmp_path):
    """Este test comprueba que el total acumulado de Pokemon es correcto"""
    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        result = service.generate(n=10, pokemon_type="grass", generation=3, seed=5)
    assert result.total_accumulated == 10


def test_generate_type_and_generation_in_result(tmp_path):
    """Este test comprueba que se generan los datos simulados con base a los argumentos
    que establecimos"""
    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        result = service.generate(n=2, pokemon_type="electric", generation=4, seed=7)
    assert result.pokemon_type == "electric"
    assert result.generation == 4


def test_generate_csv_path_in_result(tmp_path):
    """Este test comprueba que se devuelve correctamente la ruta del archivo en los
    resultados"""
    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        result = service.generate(n=1, pokemon_type="normal", generation=1, seed=0)
    assert str(csv_path) in result.csv_path


def test_generate_seed(tmp_path):
    """Este test comprueba que se puede usar una seed correctamente, estableciendo
    que la seed es el patrón de aleatoridad"""
    import pandas as pd

    service = make_simulator()

    csv_a = tmp_path / "a.csv"
    csv_b = tmp_path / "b.csv"

    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_a):
        service.generate(n=5, pokemon_type="fire", generation=1, seed=99)

    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_b):
        service.generate(n=5, pokemon_type="fire", generation=1, seed=99)

    df_a = pd.read_csv(csv_a)[["hp", "attack", "defense", "speed"]]
    df_b = pd.read_csv(csv_b)[["hp", "attack", "defense", "speed"]]
    assert df_a.equals(df_b)


def test_generate_column(tmp_path):
    """Este test comprueba que se generan las columnas correctas en el csv"""
    import pandas as pd

    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        service.generate(n=1, pokemon_type="ice", generation=2, seed=3)
    df = pd.read_csv(csv_path)
    for col in (
        "id",
        "name",
        "types",
        "generation",
        "hp",
        "attack",
        "defense",
        "speed",
        "is_synthetic",
    ):
        assert col in df.columns


def test_generate_is_synthetic_always_true(tmp_path):
    """Este test comprueba que la columna/parametro is synthtic es siempre True
    porque siempre son datos simulados con este servicio"""
    import pandas as pd

    csv_path = tmp_path / "out.csv"
    service = make_simulator()
    with patch("backend.app.services.simulator_service.SYNTHETIC_CSV", csv_path):
        service.generate(n=3, pokemon_type="ghost", generation=1, seed=4)
    df = pd.read_csv(csv_path)
    assert df["is_synthetic"].all()
