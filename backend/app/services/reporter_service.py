"""En este módulo se encuentra el encargado de realizar reportes exportables
y gráficos ASCII en consola

No depende del backend, sino que recibe los datos obtenidos por client_cli y
y los transforma en CSV

La exportación a CSV utiliza pandas, que gestiona automáticamente el enconding,
caracteres especiales y aplanando los datos.

Los gráficos ASCII no necesitan pandas, por lo que se trabajan unicamente con
aritmética, ya que trabajan con listas simples de valores ya procesados"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPORTS_DIR = Path(__file__).resolve().parents[3] / "data" / "reports"

# Ancho máximo de las barras ASCII, en caracteres
BAR_MAX_WIDTH = 40
BAR_CHAR = "█"


def export_filtered_pokemons_csv(
    pokemons: list[dict], filename: str = "filtro_pokemon.csv"
) -> Path:
    """Exporta el resultado de /filter a un CSV usando pandas.

    Args:
        pokemons: lista de diccionarios devuelta por api_get_filtered.
        filename: nombre del fichero de salida dentro de data/reports/.

    Returns:
        Ruta absoluta del fichero generado.

    Raises:
        ValueError: si la lista de pokemons está vacía (nada que exportar).
    """

    if not pokemons:
        raise ValueError(
            "No hay resultados para exportar. Realiza un filtro con datos primero."
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / filename

    df = pd.DataFrame(pokemons)

    # Convertimos las listas a strings para poder abrir el csv en Excel sin corchetes
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

    df.to_csv(output_path, index=False, encoding="utf-8")

    return output_path


def export_top_n_csv(
    top_entries: list[dict], filename: str = "top_n_pokemon.csv"
) -> Path:
    """Exporta el resultado de /analytics/top a un CSV usando pandas.

    Args:
        top_entries: lista de diccionarios devuelta por api_get_top.
        filename: nombre del fichero de salida dentro de data/reports/.

    Returns:
        Ruta absoluta del fichero generado.

    Raises:
        ValueError: si la lista está vacía.
    """

    if not top_entries:
        raise ValueError("No hay resultados de Top-N para exportar.")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORTS_DIR / filename

    df = pd.DataFrame(top_entries)

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(
                lambda x: ", ".join(x) if isinstance(x, list) else x
            )

    df.to_csv(output_path, index=False, encoding="utf-8")

    return output_path


def _normalize_bar_widths(values: list[float]) -> list[int]:
    """Convierte una lista de valores numéricos en anchos de barra
    proporcionales al valor máximo, con un techo de BAR_MAX_WIDTH caracteres."""

    max_value = max(values) if values else 0

    if max_value == 0:
        return [0 for _ in values]

    return [round((v / max_value) * BAR_MAX_WIDTH) for v in values]


def print_pokemon_stats_chart(pokemon: dict) -> None:
    """Imprime un gráfico de barras ASCII con los stats (hp/attack/defense/
    speed) de un único Pokemon.

    Args:
        pokemon: diccionario con al menos las claves name, hp/stats.
                 Soporta tanto el formato de PokemonDetail (con "stats" como
                 dict) como el formato plano del dataset/teams (hp/attack/
                 defense/speed como claves directas).
    """

    name = pokemon.get("name", "desconocido")

    # Soportamos ambos formatos: PokemonDetail.stats (dict anidado) y el
    # formato plano del dataset local / TeamMember
    if "stats" in pokemon and isinstance(pokemon["stats"], dict):
        raw_stats = pokemon["stats"]
        stat_pairs = [
            ("hp", raw_stats.get("hp", 0)),
            ("attack", raw_stats.get("attack", 0)),
            ("defense", raw_stats.get("defense", 0)),
            ("speed", raw_stats.get("speed", 0)),
        ]
    else:
        stat_pairs = [
            ("hp", pokemon.get("hp", 0)),
            ("attack", pokemon.get("attack", 0)),
            ("defense", pokemon.get("defense", 0)),
            ("speed", pokemon.get("speed", 0)),
        ]

    values = [v for _, v in stat_pairs]
    widths = _normalize_bar_widths(values)

    print(f"\n📊 Stats de {name.capitalize()}")
    print("-" * 60)

    for (stat_name, value), width in zip(stat_pairs, widths, strict=True):
        bar = BAR_CHAR * width
        print(f"{stat_name:<10}| {bar} {value}")

    print("-" * 60)


def print_type_average_chart(
    type_stats: list[dict], metric: str = "avg_attack"
) -> None:
    """Imprime un gráfico de barras ASCII comparando una métrica promedio
    entre todos los tipos elementales (resultado de /analytics/average-by-type).

    Args:
        type_stats: lista de diccionarios devuelta por api_get_average_by_type.
        metric: cuál de los promedios graficar (avg_hp/avg_attack/avg_defense/avg_speed)
    """

    if not type_stats:
        raise ValueError("No hay datos de promedio por tipo para graficar.")

    valid_metrics = ("avg_hp", "avg_attack", "avg_defense", "avg_speed")

    if metric not in valid_metrics:
        raise ValueError(
            f"Métrica '{metric}' no válida. Usa una de: {', '.join(valid_metrics)}."
        )

    # Ordenamos de mayor a menor para que el gráfico sea más legible
    ordered = sorted(type_stats, key=lambda t: t.get(metric, 0), reverse=True)

    values = [t.get(metric, 0) for t in ordered]
    widths = _normalize_bar_widths(values)

    print(f"\n📊 Comparativa de '{metric}' por tipo elemental")
    print("-" * 60)

    for entry, width in zip(ordered, widths, strict=True):
        bar = BAR_CHAR * width
        type_name = entry.get("type_name", "?")
        value = entry.get(metric, 0)
        print(f"{type_name:<10}| {bar} {value}")

    print("-" * 60)
