from __future__ import annotations

import pandas as pd
import pytest

from backend.app.services.analyzer_service import AnalyzerService

# Configuramos un DATASET de prueba
# Necesitamos al menos dos Pokemon del mismo tipo para que stddev funcione,
# y uno muy outlier (estadísticas lejos de la media) para activar
# la detección de anomalías.

FAKE_DATASET = [
    {
        "id": 1,
        "name": "bulbasaur",
        "types": ["grass", "poison"],
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
        "hp": 60,
        "attack": 62,
        "defense": 63,
        "speed": 60,
        "base_exp": 142,
    },
    {
        "id": 3,
        "name": "venusaur",
        "types": ["grass", "poison"],
        "hp": 80,
        "attack": 82,
        "defense": 83,
        "speed": 80,
        "base_exp": 236,
    },
    {
        "id": 4,
        "name": "charmander",
        "types": ["fire"],
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
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "speed": 100,
        "base_exp": 240,
    },
    # Outlier extremo para activar detección por stddev
    {
        "id": 150,
        "name": "mewtwo",
        "types": ["psychic"],
        "hp": 106,
        "attack": 110,
        "defense": 90,
        "speed": 130,
        "base_exp": 340,
    },
    {
        "id": 151,
        "name": "mew",
        "types": ["psychic"],
        "hp": 100,
        "attack": 100,
        "defense": 100,
        "speed": 100,
        "base_exp": 270,
    },
]


def make_service(dataset=None) -> AnalyzerService:
    data = dataset if dataset is not None else FAKE_DATASET

    return AnalyzerService(dataset_loader=lambda: data)


def test_load_dataset_empty_raises_value_error():
    """Este test comprueba la captura del error en caso de que se envíe
    un dataset vacío"""

    service = make_service(dataset=[])
    with pytest.raises(ValueError, match="vacío"):
        service._load_dataframe()


def test_avg_stats_by_type():
    """Este test comprueba que se devuelvan correctamente los promedios
    por tipo"""

    service = make_service()
    result = service.average_stats_by_type()
    assert isinstance(result, list)
    assert len(result) > 0


def test_avg_stats_by_type_correct_format():
    """Este test comprueba que se devuelven las estadísticas
    en la estructura correcta"""

    service = make_service()
    result = service.average_stats_by_type()
    entry = result[0]
    assert hasattr(entry, "type_name")
    assert hasattr(entry, "sample_size")
    assert hasattr(entry, "avg_hp")
    assert hasattr(entry, "avg_attack")
    assert hasattr(entry, "avg_defense")
    assert hasattr(entry, "avg_speed")


def test_avg_stats_by_type_correct():
    """Este test comprueba que se calcula de forma correcta el promedio
    por tipo"""

    service = make_service()
    result = service.average_stats_by_type()

    fire = next(e for e in result if e.type_name == "fire")

    df = pd.DataFrame(FAKE_DATASET)

    df["primary_type"] = df["types"].apply(
        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
    )

    df["secondary_type"] = df["types"].apply(
        lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None
    )
    primary = df.copy()
    primary["type_name"] = primary["primary_type"]

    secondary = df.copy()
    secondary["type_name"] = secondary["secondary_type"]

    df_types = pd.concat([primary, secondary], ignore_index=True)
    df_types = df_types[df_types["type_name"].notna()]

    fire_df = df_types[df_types["type_name"] == "fire"]

    expected_hp = round(fire_df["hp"].mean(), 2)
    expected_attack = round(fire_df["attack"].mean(), 2)
    expected_defense = round(fire_df["defense"].mean(), 2)
    expected_speed = round(fire_df["speed"].mean(), 2)

    assert fire.sample_size == len(fire_df)
    assert fire.avg_hp == expected_hp
    assert fire.avg_attack == expected_attack
    assert fire.avg_defense == expected_defense
    assert fire.avg_speed == expected_speed


def test_avg_stats_by_type_sorted():
    """Este test comprueba que se ordenan alfabéticamente los promedios
    de estadísticas"""

    service = make_service()
    result = service.average_stats_by_type()
    nombres = [e.type_name for e in result]
    assert nombres == sorted(nombres)


def test_avg_stats_by_type_dual_pokemon():
    """Este test comprueba que se toman en cuenta los dos tipos de un Pokemon
    para el cálculo de sus estadísticas promedio"""

    service = make_service()
    result = service.average_stats_by_type()
    tipos = {e.type_name for e in result}
    # siempre deben aparecer los pryimary_type
    assert "grass" in tipos
    assert "fire" in tipos
    assert "psychic" in tipos


def test_avg_stats_by_type_empty_list_return_error():
    """Este test comprueba que en caso de retornar una lista vacía, se captura
    un error"""

    service = make_service(dataset=[])
    with pytest.raises(ValueError):
        service.average_stats_by_type()


def test_top_n_return_elements():
    """Este test comprueba que se devuelvan elementos al calculo de los Pokemon
    Top-N"""

    service = make_service()
    result = service.top_n(metric="attack", n=3)
    assert len(result) == 3


def test_top_n_sorted():
    """Este test comprueba que se devuelven los Top-N ordenados de manera descendente"""

    service = make_service()
    result = service.top_n(metric="attack", n=5)
    values = [e.value for e in result]
    assert values == sorted(values, reverse=True)


def test_top_n_correct():
    """Este test comprueba que la métrica del Top-N se calcule correctamente"""

    service = make_service()
    result = service.top_n(metric="hp", n=1)
    assert result[0].name == "mewtwo"
    assert result[0].metric == "hp"


def test_top_n_all_metrics_valid():
    """Este test comprueba que las métricas calculadas sean válidas"""

    service = make_service()
    for metric in ("hp", "attack", "defense", "speed", "base_exp"):
        result = service.top_n(metric=metric, n=2)
        assert len(result) == 2


def test_top_n_metric_invalid_raises_error():
    """Este test comprueba que se captura el error en caso de métricas
    inválidas"""

    service = make_service()
    with pytest.raises(ValueError, match="no válida"):
        service.top_n(metric="stamina")


def test_top_n_zero_raises_error():
    """Este test comprueba que una métrica 0 capture error"""

    service = make_service()
    with pytest.raises(ValueError, match="entero positivo"):
        service.top_n(n=0)


def test_top_n_negative_metric_raises_error():
    """Este test comprueba que en caso de una métrica negativa
    se capture un error"""

    service = make_service()
    with pytest.raises(ValueError, match="entero positivo"):
        service.top_n(n=-1)


def test_top_n_dataset_empty_raises_error():
    """Este test comprueba la captura del error en caso de un dataset
    vacío"""

    service = make_service(dataset=[])
    with pytest.raises(ValueError):
        service.top_n()


def test_detect_anomalies_return_list():
    """Este test comprueba que se devuelve una lista de anomalías"""

    service = make_service()
    result = service.detect_anomalies()
    assert isinstance(result, list)


def test_detect_anomalies_right_structure():
    """Este test comprueba que se devuelva la estructura models correcta
    de anomalías"""

    service = make_service()
    result = service.detect_anomalies()
    if result:
        entry = result[0]
        assert hasattr(entry, "id")
        assert hasattr(entry, "name")
        assert hasattr(entry, "stat_total")
        assert hasattr(entry, "method")
        assert hasattr(entry, "deviation")
        assert hasattr(entry, "reason")


def test_detect_anomalies_method_stddev_or_percentile():
    """Este test comprueba tanto el método stddev o calculo del percentil"""

    service = make_service()
    result = service.detect_anomalies()
    for entry in result:
        assert entry.method in ("stddev", "percentile")


def test_detect_anomalies_sorted():
    """Este test comprueba que se ordenen de forma descendente de acuerdo a la
    desviación estandar"""

    service = make_service()
    result = service.detect_anomalies()
    deviations = [abs(e.deviation) for e in result]
    assert deviations == sorted(deviations, reverse=True)


def test_detect_anomalies_low_threshold():
    """Este test comprueba que la deteccion de anomalias con un umbral bajo
    detecta más"""

    service = make_service()
    result_estricto = service.detect_anomalies(stdev_threshold=3.0)
    result_permisivo = service.detect_anomalies(stdev_threshold=0.5)
    assert len(result_permisivo) >= len(result_estricto)


def test_detect_anomalies_no_duplicate():
    """Este test comprueba que no existen duplicados en la
    detección de anomalías"""

    service = make_service()
    result = service.detect_anomalies()
    ids = [e.id for e in result]
    assert len(ids) == len(set(ids))


def test_detect_anomalies_empty_dataset_raise_error():
    """Este test comprueba que se captura un error frente a un dataset vacío"""

    service = make_service(dataset=[])
    with pytest.raises(ValueError):
        service.detect_anomalies()


def test_detect_anomalies_single_type_no_stddev():
    """Este test comprueba que para un Pokemon con un solo tipo no se calcule
    stddev, simplemente lo omite"""

    single_type_dataset = [
        {
            "id": 1,
            "name": "solo",
            "primary_type": "dragon",
            "types": ["dragon"],
            "hp": 50,
            "attack": 50,
            "defense": 50,
            "speed": 50,
            "base_exp": 100,
        },
        {
            "id": 2,
            "name": "otro",
            "primary_type": "fire",
            "types": ["fire"],
            "hp": 50,
            "attack": 50,
            "defense": 50,
            "speed": 50,
            "base_exp": 100,
        },
    ]
    service = make_service(dataset=single_type_dataset)
    result = service.detect_anomalies()
    assert isinstance(result, list)
