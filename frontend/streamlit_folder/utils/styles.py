"""
En este módulo se encuentran las utilidades de diseño y los estilos
CSS para los componentes de la UI
"""

from __future__ import annotations

import streamlit as st


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
            color: black;
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
