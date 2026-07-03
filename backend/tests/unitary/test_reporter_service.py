from __future__ import annotations

import re
from unittest.mock import patch

import pytest

from backend.app.services.reporter_service import (
    _normalize_bar_widths,
    export_filtered_pokemons_csv,
    export_top_n_csv,
    print_pokemon_stats_chart,
    print_type_average_chart,
)

# A continuación generamos datos ficticios para usarlos al momento de testear
SAMPLE_POKEMONS = [
    {"id": 1, "name": "bulbasaur", "types": ["grass", "poison"]},
    {"id": 4, "name": "charmander", "types": ["fire"]},
]

SAMPLE_TOP_ENTRIES = [
    {
        "id": 6,
        "name": "charizard",
        "types": ["fire", "flying"],
        "value": 84,
        "metric": "attack",
    },
    {
        "id": 3,
        "name": "venusaur",
        "types": ["grass", "poison"],
        "value": 82,
        "metric": "attack",
    },
]

SAMPLE_TYPE_STATS = [
    {
        "type_name": "fire",
        "avg_hp": 70.0,
        "avg_attack": 84.0,
        "avg_defense": 60.0,
        "avg_speed": 80.0,
    },
    {
        "type_name": "grass",
        "avg_hp": 65.0,
        "avg_attack": 70.0,
        "avg_defense": 72.0,
        "avg_speed": 55.0,
    },
]


def test_export_filtered_pokemons_csv_creates_file(tmp_path):
    """Este test comprueba que se crea correctamente el reporte csv de filtros"""
    with patch("backend.app.services.reporter_service.REPORTS_DIR", tmp_path):
        result = export_filtered_pokemons_csv(
            SAMPLE_POKEMONS, filename="test_filter.csv"
        )

    assert result.exists()

    content = result.read_text(encoding="utf-8")

    assert "bulbasaur" in content
    assert "charmander" in content


def test_export_filtered_pokemons_csv_correct_headers(tmp_path):
    """Este test comprueba las cabeceras correctas en el reporte csv"""
    with patch("backend.app.services.reporter_service.REPORTS_DIR", tmp_path):
        result = export_filtered_pokemons_csv(
            SAMPLE_POKEMONS, filename="test_filter.csv"
        )

    header = result.read_text(encoding="utf-8").splitlines()[0]

    assert "id" in header
    assert "name" in header
    assert "types" in header


def test_export_filtered_pokemons_empty_list_error():
    """Este test comprueba el csv filtered en caso de presentarse unicamente
    una lista vacía para el reporte"""
    with pytest.raises(
        ValueError,
        match=re.escape(
            "No hay resultados para exportar. Realiza un filtro con datos primero."
        ),
    ):
        export_filtered_pokemons_csv([])


def test_export_filtered_pokemon_csv_fallback_name(tmp_path):
    """Este test comprueba que en caso de no especificar un nombre para el archivo
    cae en el fallback"""
    with patch("backend.app.services.reporter_service.REPORTS_DIR", tmp_path):
        result = export_filtered_pokemons_csv(SAMPLE_POKEMONS)

    assert result.name == "filtro_pokemon.csv"


def test_export_top_n_csv_creates_file(tmp_path):
    """Este test comprueba que se crea correctamente el reporte csv de top-n"""
    with patch("backend.app.services.reporter_service.REPORTS_DIR", tmp_path):
        result = export_top_n_csv(SAMPLE_TOP_ENTRIES, filename="test_top.csv")

    assert result.exists()

    content = result.read_text(encoding="utf-8")

    assert "charizard" in content


def test_export_top_n_csv_empty_list_error():
    """Este test comprueba el csv top-n en caso de presentarse unicamente
    una lista vacía para el reporte"""
    with pytest.raises(
        ValueError, match=re.escape("No hay resultados de Top-N para exportar.")
    ):
        export_top_n_csv([])


def test_export_top_n_csv_fallback_name(tmp_path):
    """Este test comprueba que en caso de no especificar un nombre para el archivo
    cae en el fallback"""
    with patch("backend.app.services.reporter_service.REPORTS_DIR", tmp_path):
        result = export_top_n_csv(SAMPLE_TOP_ENTRIES)

    assert result.name == "top_n_pokemon.csv"


def test_normalize_bar_widths():
    """Este test comprueba que se normalizan correctamente el ancho de las barras a
    representarse en el gráfico de barras de estadísticas"""
    from backend.app.services.reporter_service import BAR_MAX_WIDTH

    widths = _normalize_bar_widths([100, 50, 0])

    assert widths[0] == BAR_MAX_WIDTH


def test_normalize_bar_widths_proportions():
    """Este test comprueba las proporciones de las barras del gráfico de acuerdo a la
    estadística que representan"""
    widths = _normalize_bar_widths([100, 50])

    assert widths[0] == widths[1] * 2


def test_normalize_bar_widths_empty_list_error():
    """Este test comprueba el comportamiento en caso de una lista vacía para el ancho
    de las barras"""
    assert _normalize_bar_widths([]) == []


def test_normalize_bar_widths_all_zero():
    """Este testo comprueba que se usan valores 0 para normalizar el
    ancho de las barras"""
    assert _normalize_bar_widths([0, 0, 0]) == [0, 0, 0]


def test_print_pokemon_stats_chart_dict_stats(capsys):
    """Este test comprueba la impresión correcta de los datos en el gráfico ASCII"""
    pokemon = {
        "name": "pikachu",
        "stats": {"hp": 35, "attack": 55, "defense": 40, "speed": 90},
    }

    print_pokemon_stats_chart(pokemon)
    output = capsys.readouterr().out

    assert "pikachu" in output.lower()
    assert "hp" in output
    assert "speed" in output


def test_print_pokemon_stats_plain_text(capsys):
    """Este test comprueba que se imprimen correctamente los datos
    en formato texto plano"""
    pokemon = {"name": "ditto", "hp": 48, "attack": 48, "defense": 48, "speed": 48}

    print_pokemon_stats_chart(pokemon)
    output = capsys.readouterr().out

    assert "ditto" in output.lower()
    assert "48" in output


def test_print_pokemon_stats_chart_no_name(capsys):
    """Este test comprueba el comportamiento en caso de un gráfico sin datos"""
    print_pokemon_stats_chart({})
    output = capsys.readouterr().out

    assert "desconocido" in output.lower()


def test_print_type_avg_chart_types(capsys):
    """Este test comprueba la impresión del gráfico ASCII de
    promedios de estadísticas"""
    print_type_average_chart(SAMPLE_TYPE_STATS, metric="avg_attack")
    output = capsys.readouterr().out

    assert "fire" in output
    assert "grass" in output


def test_print_type_avg_chart_invalid_metric():
    """Este test comprueba la impresión del gráfico de promedios de estadísticas
    en caso de metras inválidas"""
    with pytest.raises(ValueError, match="no válida"):
        result = print_type_average_chart(SAMPLE_TYPE_STATS, metric="avg_stamina")

        assert result is None


def test_print_avg_type_chart(capsys):
    """Este test comprueba la impresión de nombres de estadísticas avg,
    obviando el avg_"""
    for metric in ("avg_hp", "avg_attack", "avg_defense", "avg_speed"):
        print_type_average_chart(SAMPLE_TYPE_STATS, metric=metric)
        output = capsys.readouterr().out

        assert metric.replace("avg_", "") in output or output
