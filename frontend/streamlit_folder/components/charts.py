"""
Es módulo contiene los componentes de gráficos y visualizaciones de estadísticas
"""

from __future__ import annotations

import plotly.graph_objects as go
from utils.colors import hexadecimal_to_rgba


def render_stats_radar_chart(
    stats: dict[str, int], pokemon_name: str, color_hex: str
) -> go.Figure:

    labels = {
        "hp": "HP",
        "attack": "Ataque",
        "defense": "Defensa",
        "speed": "Velocidad",
        "special-attack": "At. Especial",
        "special-defense": "Def. Espcial",
    }

    stats_keys = list(stats.keys())

    # En un gráfico de radar el circuito tiene que cerrarse reconectando
    # el primer valor con el último
    categories = [labels.get(k, k.capitalize()) for k in stats_keys]
    values = [int(stats[k]) for k in stats_keys]

    categories_closed = [*categories, [categories[0]]]
    values_closed = [*values, [values[0]]]

    fig = go.Figure()

    color_fill_rgba = hexadecimal_to_rgba(color_hex, alpha=0.3)

    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            name=pokemon_name.capitalize(),
            fillcolor=color_fill_rgba,
            line={"color": color_hex, "width": 2.5},
            marker={"size": 6, "color": color_hex},
            hoverinfo="r+theta",
        )
    )

    max_stat = max(values)
    upper_limit = max(100, max_stat + 5)

    fig.update_layout(
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "visible": True,
                "range": [0, upper_limit],
                "showticklabels": False,
                "gridcolor": "rgba(0, 0, 0, 0.08)",
                "angle": 90,
            },
            "angularaxis": {
                "gridcolor": "rgba(0, 0, 0, 0.08)",
                "linecolor": "rgba(0, 0, 0, 0.1)",
                "tickfont": {
                    "size": 12,
                    "color": "var(--text-color)",
                    "family": "sans-serif",
                },
            },
        },
        showlegend=False,
        margin={"l": 45, "r": 45, "t": 15, "b": 15},
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
