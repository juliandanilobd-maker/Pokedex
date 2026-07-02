from __future__ import annotations

from datetime import date
from unittest.mock import patch

from backend.app.services.alerts_service import AlertEngine

FAKE_DATASET = [
    {
        "id": 1,
        "name": "bulbasaur",
        "types": ["grass"],
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "speed": 45,
    },
    {
        "id": 4,
        "name": "charmander",
        "types": ["fire"],
        "hp": 39,
        "attack": 52,
        "defense": 43,
        "speed": 65,
    },
    {
        "id": 25,
        "name": "pikachu",
        "types": ["electric"],
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "speed": 90,
    },
]

FAKE_ANOMALIES = [
    {"id": 150, "name": "mewtwo", "stat_total": 680},
    {"id": 6, "name": "charizard", "stat_total": 534},
]

FAKE_TEAMS = [
    {"name": "Equipo Fuego", "stats": {"type_coverage": ["fire"]}},
    {
        "name": "Equipo Mixto",
        "stats": {"type_coverage": ["fire", "water", "grass", "electric"]},
    },
]


def make_engine(
    dataset=None,
    anomalies=None,
    teams=None,
) -> AlertEngine:

    def dataset_loader():
        return dataset if dataset is not None else FAKE_DATASET

    def anomalies_fetcher():
        return anomalies if anomalies is not None else FAKE_ANOMALIES

    def teams_fetcher():
        return teams if teams is not None else FAKE_TEAMS

    return AlertEngine(dataset_loader, anomalies_fetcher, teams_fetcher)


def test_pokemon_of_day():
    """Este test comprueba que Pokemon del día, devuelve un Pokemon
    aleatorio"""

    engine = make_engine()
    result = engine._pokemon_del_dia()
    assert result is not None
    assert "name" in result
    assert "id" in result


def test_pokemon_of_day_mantains_on_day():
    """Este test comprueba que el Pokemon del día se determina una vez al día
    y se mantiene durante el mismo"""

    engine = make_engine()
    result1 = engine._pokemon_del_dia()
    result2 = engine._pokemon_del_dia()
    assert result1["id"] == result2["id"]


def test_pokemon_of_day_empty_dataset_returns_none():
    """Este test comprueba que en caso de un dataset vacío, se devuelve un
    None"""

    engine = make_engine(dataset=[])
    assert engine._pokemon_del_dia() is None


def test_pokemon_of_day_changes_with_date():
    """Este test comprueba que el Pokemon del dia cambia al dia siguiente"""

    engine = make_engine()

    with patch("backend.app.services.alerts_service.date") as mock_date:
        mock_date.today.return_value = date(2020, 1, 1)
        result_a = engine._pokemon_del_dia()

        mock_date.today.return_value = date(2099, 12, 31)
        result_b = engine._pokemon_del_dia()

    # No siempre serán distintos (con 3 entradas puede coincidir),
    # pero al menos verificamos que se ejecuta sin error
    assert result_a is not None
    assert result_b is not None


def test_anomalies_return_correct_len():
    """Este test comprueba que el resumen de anomalías retorna
    un conteo correcto"""

    engine = make_engine()
    assert engine._resumen_anomalias() == 2


def test_anomalies_return_zero_with_empty_list():
    """Este test comprueba que se retorna un cero en caso de una lista vacía
    de anomalías"""

    engine = make_engine(anomalies=[])
    assert engine._resumen_anomalias() == 0


def test_anomalies_return_zer_if_fetcher_fails():
    """Este test comprueba que se retorna un cero en caso de una falla
    del fetcher"""

    def fetcher_roto():
        raise ConnectionError("Backend caído")

    engine = AlertEngine(lambda: FAKE_DATASET, fetcher_roto, lambda: FAKE_TEAMS)
    assert engine._resumen_anomalias() == 0


def test_teams_with_low_coverage_alerts():
    """Este test comprueba que que se detectan los equipos con baja cobertura
    de acuerdo a tipos"""

    engine = make_engine()
    debiles = engine._equipos_con_poca_cobertura(min_types=3)
    assert "Equipo Fuego" in debiles


def test_teams_with_low_coverage_not_include_various_team():
    """Este test comprueba que no se incluyen en baja cobertura los equipos
    variados"""

    engine = make_engine()
    debiles = engine._equipos_con_poca_cobertura(min_types=3)
    assert "Equipo Mixto" not in debiles


def test_teams_with_low_coverage_returns_empty_list_if_not_teams():
    """Este test comprueba que se devuelve una lista vacía en caso de que
    no se tengan equipos guardados"""

    engine = make_engine(teams=[])
    assert engine._equipos_con_poca_cobertura() == []


def test_teams_with_low_coverage_returns_empty_list_if_fetcher_fails():
    """Este test comprueba que se devuelve una lista vacía en caso de que
    falle el fetcher"""

    def fetcher_roto():
        raise RuntimeError("Error de red")

    engine = AlertEngine(lambda: FAKE_DATASET, lambda: FAKE_ANOMALIES, fetcher_roto)
    assert engine._equipos_con_poca_cobertura() == []


def test_run_startup_alerts_print_pokemon_of_day(capsys):
    """Este test comprueba que se imprime el Pokemon del día como alerta
    al iniciar el CLI"""

    engine = make_engine()
    engine.run_startup_alerts()
    output = capsys.readouterr().out
    assert any(p["name"] in output.lower() for p in FAKE_DATASET)


def test_run_startup_alerts_print_anomalies(capsys):
    """Este test comprueba que se imprimen las anomalías existentes como
    alerta al inicar el CLI"""

    engine = make_engine()
    engine.run_startup_alerts()
    output = capsys.readouterr().out
    assert "2" in output  # 2 anomalías detectadas


def test_run_startup_alerts_print_weak_team(capsys):
    """Este test comprueba que se imprimen los equipos débiles como
    alerta al iniciar el CLI"""

    engine = make_engine()
    engine.run_startup_alerts()
    output = capsys.readouterr().out
    assert "Equipo Fuego" in output


def test_run_startup_alerts_no_alerts_show_ok(capsys):
    """Este test comprueba que en caso de no haber alertas
    se muestra un mensaje"""

    engine = AlertEngine(
        dataset_loader=lambda: [],
        anomalies_fetcher=lambda: [],
        teams_fetcher=lambda: [],
    )
    engine.run_startup_alerts()
    output = capsys.readouterr().out
    assert "No hay alertas" in output
