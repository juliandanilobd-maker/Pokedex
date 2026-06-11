"""
En este módulo se encuentran las utilidades de diseño y los estilos
CSS para los componentes de la UI
"""

from __future__ import annotations

import streamlit as st

POKEMON_TYPE_COLORS: dict[str, str] = {
    "fire": "#ff421c",
    "water": "#2c9be3",
    "grass": "#78cc55",
    "electric": "#ffd333",
    "ice": "#7ac7ff",
    "fighting": "#bb5544",
    "poison": "#aa5599",
    "ground": "#ddbb55",
    "flying": "#8899ff",
    "psychic": "#ff5599",
    "bug": "#aabb22",
    "rock": "#bbaa66",
    "ghost": "#6666bb",
    "dragon": "#7766ee",
    "dark": "#775544",
    "steel": "#aaaabb",
    "fairy": "#ee99ee",
    "normal": "#aaaa99",
}


def get_type_color(type_name: str) -> str:
    return POKEMON_TYPE_COLORS.get(type_name.lower(), "#A8A878")


# Establecemos el estilo CSS base para las cartas coleccionables
def inject_card_css() -> None:

    st.markdown(
        """
        <style>
        .poke-card {
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            color: white;
            transition: transform 0.2s;
        }
        .poke-card: hover {
            transform: scale(1.03);
        }
        .poke-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin: 3px;
            border: 1px solid rgba(255,255,255,0.4);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
