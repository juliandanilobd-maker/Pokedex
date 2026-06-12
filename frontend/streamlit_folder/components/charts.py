"""
Es módulo contiene los componentes de gráficos y visualizaciones de estadísticas
"""

from __future__ import annotations

import plotly.graph_objects as go


def render_stats_radar_chart(
    stats: dict[str, int], pokemon_name: str, color_hex: str
) -> go.Figure:

    categories = [
        "HP",
        "Ataque",
        "Defensa",
        "Velocidad",
        "Ataque Especial",
        "Defensa Esepcial",
    ]

    values = [
        stats.get("hp", 0),
        stats.get("Ataque", 0),
        stats.get("Defensa", 0),
        stats.get("Velocidad", 0),
        stats.get("Ataque Especial", 0),
        stats.get("Defensa Esepcial", 0),
    ]

    # En un gráfico de radar el circuito tiene que cerrarse reconectando
    # el primer valor con el último
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=pokemon_name.capitalize(),
            fillcolor=f"{color_hex}33",
            line={"color":color_hex, "width":2.5},
            marker={"size": 6, "color": color_hex},
            hoverinfo="r+theta",
        )
    )

    fig.update_layout(
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "visible": "True",
                "range": [0, 255],
                "showticklabels": False,
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "angle": 90,
            },
            "angularaxis": {
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "linecolor": "rgba(255, 255, 255, 0.2)",
                "tickfont": {"size":12, "color":"var(--text-color)"},
            },
        },
        showlegend=False,
        margin={"l":40, "r":40, "t":20, "b":20},
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig
