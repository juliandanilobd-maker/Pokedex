"""
En este módulo se alojan los componentes visuales para representar
a un Pokemon
"""

from __future__ import annotations

import streamlit as st

from frontend.streamlit_folder.utils.styles import get_type_color, inject_card_css


# Generamos el codigo HTML para un emblema elemental único
def type_badge(type_name: str) -> str:

    color = get_type_color(type_name)
    return (
        f'<span class="poke-badge" style="background-color:{color};">{type_name}</span>'
    )


# Generamos el contenedor HTML para el sprite
def sprite_component(sprite_url: str, fallback_id: int = 0) -> str:

    if not sprite_url:
        sprite_url = (
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
            "sprites/items/poke-ball.png"
        )

    return (
        f'<div style="margin: 12px 0px; min-height: 140px; display: flex;>'
        f'justify-content: center; align-items: center;">'
        f'<img src="{sprite_url}" style="max-height: 140px; '
        f'filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));">'
        f"</div>"
    )


# Generamos un componente propio de Streamlit para mostrar datos rápidos informativos
def info_panel(label: str, value: str | int) -> None:

    st.markdown(
        f"""
        <div style="backgorund-color: rgba(255, 255, 255, 0.05);
                    padding: 8px 12px;
                    border-radius: 8px;
                    border-left: 3px solid var(--text-color);
                    margin: 4px 0px;">
            <small style="opacity: 0.7; text-transform: uppercase;">{label}</small>
            <div style="font-size: 16px; font-weight: bold;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Generamos el contenedor principal, ensambla el sprite_component y type_badges dentro
# de una carta hecha según el tipo principal del Pokemon
def pokemon_card(p_id: int, name: str, types: list[str], sprite_url: str) -> None:

    inject_card_css()

    primary_type = types[0] if types else "normal"
    bg_color = get_type_color(primary_type)

    badges_html = "".join(type_badge(t) for t in types)

    image_html = sprite_component(sprite_url, fallback_id=p_id)

    card_html = f"""
    <div class="
        poke-card style="
            background-color: {bg_color}22;
            border: 2px solid {bg_color};
    ">
        <span style="
            color: {bg_color};
            font-weight: bold;
            font-size: 14px;
        ">#{p_id:04d}</span>
        <h3 style="
            color: var(--text-color);
            margin: 5px 0px;
            text-transform: capitalize;
        ">{name}</h3>
        <div style:"
            margin: 10px 0px;
        ">
            <img src="
                {image_html}"
                style="
                    max-height: 140px;
                    filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));
            ">
        </div>
        <div>
            {badges_html}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)
