from __future__ import annotations

import pytest

from backend.app.models.pokemon_models import PredictionResult
from backend.app.services.predictor_service import PredictorService

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
        "id": 45,
        "name": "vileplume",
        "types": ["grass", "poison"],
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


def make_predictor() -> PredictorService:
    return PredictorService(dataset_loader=lambda: FAKE_DATASET)


def test_predictor_load_dataframe_empty_raises_error():
    """Este test comprueba que al cargar un dataframe vacío se levanta error"""
    service = PredictorService(dataset_loader=lambda: [])
    with pytest.raises(ValueError, match="vacío"):
        service._load_dataframe()


def test_predictor_load_dataframe_returns_dataframe():
    """Este test comprueba que se devuelve el dataframe correctamente"""
    import pandas as pd

    service = make_predictor()
    df = service._load_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(FAKE_DATASET)


def test_predict_stats_type_does_not_exist_raises_error():
    """Este test comprueba que si se colocan tipos inexistentes
    se lanza error"""
    service = make_predictor()
    with pytest.raises(ValueError, match="dragon"):
        service.predict_stats(primary_type="dragon")


def test_predict_stats_tipo_normalize():
    """Este test comprueba que el servicio hace .lower().strip(),
    no debe fallar con FIRE"""
    service = make_predictor()
    result = service.predict_stats(primary_type="FIRE")
    assert result.primary_type == "fire"


def test_predict_stats_type_dual():
    """Este test comprueba que se hace una predicción correcta de un Pokemon con
    tipo dual"""
    service = make_predictor()
    result = service.predict_stats(primary_type="grass", secondary_type="poison")
    assert result.primary_type == "grass"
    assert result.secondary_type == "poison"


def test_predict_stats_type_dual_does_not_exist_raises_error():
    """Este test comprueba que no se pueden crear una predicción de un tipo o
    combinaciones de tipo que no existan en el dataset ej. fire/psychic no existe en el
    dataset"""
    service = make_predictor()
    with pytest.raises(ValueError):
        service.predict_stats(primary_type="fire", secondary_type="psychic")


def test_predict_stats_returns_prediction_result():
    """Este test comprueba que se dvuelve correctamente una predicción"""
    service = make_predictor()
    result = service.predict_stats(primary_type="fire")
    assert isinstance(result, PredictionResult)


def test_predict_stats():
    """Este test comrpueba que se devuelvan todos las estadísticas establecidas"""
    service = make_predictor()
    result = service.predict_stats(primary_type="fire")
    assert result.primary_type == "fire"
    assert result.secondary_type is None
    assert result.predicted_hp > 0
    assert result.predicted_attack > 0
    assert result.predicted_defense > 0
    assert result.predicted_speed > 0
    assert result.sample_size > 0
    assert len(result.generations_used) >= 2
    assert result.window_size >= 2
    assert result.description != ""


def test_predict_stats_sorted_used_generations():
    """Este test comprueba que se devuelven las generaciones usadas de forma ordenada
    de forma descendente"""
    service = make_predictor()
    result = service.predict_stats(primary_type="fire")
    assert result.generations_used == sorted(result.generations_used)


def test_predict_stats_window_size_max_3():
    """Este test comprueba que se usan máximo 3 generaciones para predecir"""
    service = make_predictor()
    result = service.predict_stats(primary_type="fire")
    assert result.window_size <= 3


def test_predict_stats_group_avg_calculate():
    """Este test comprueba que se calculan los avg stats"""
    service = make_predictor()
    result = service.predict_stats(primary_type="water")
    assert result.group_avg_hp > 0
    assert result.group_avg_attack > 0
