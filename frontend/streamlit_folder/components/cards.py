"""
En este módulo se alojan los componentes visuales para representar
a un Pokemon
"""

from __future__ import annotations

import streamlit as st
from utils.colors import get_type_color, hexadecimal_to_rgba
from utils.styles import inject_card_css

POKEMON_TYPES = {
    "Todos": "Todos",
    "normal": "Normal",
    "fire": "Fuego",
    "water": "Agua",
    "grass": "Planta",
    "electric": "Electrico",
    "ice": "Hielo",
    "fighting": "Lucha",
    "poison": "Veneno",
    "ground": "Tierra",
    "flying": "Volador",
    "psychic": "Psíquico",
    "bug": "Bicho",
    "rock": "Roca",
    "ghost": "Fantasma",
    "dragon": "Dragon",
    "steel": "Hierro",
    "fairy": "Hada",
    "dark": "Siniestro",
}


def get_type_translated(type_en: str) -> str:

    return POKEMON_TYPES.get(type_en.strip(), type_en)


# Generamos el codigo HTML para un emblema elemental único
def type_badge(type_name: str, display_name: str | None = None) -> str:

    color = get_type_color(type_name.lower().strip())

    display_name = get_type_translated(type_name)

    label = display_name if display_name else type_name
    html = f"""<span class="poke-badge" style="
                background-color:{color};
                padding: 4px 8px;
                border-radius: 4px;
                color: black;
                margin-right: 4px;
                display: inline-block;
                text-transform: capitalize;
                font-size: 12px;
                font-weight: bold;">{label}</span>"""

    return html.replace("\n", "").strip()


# Generamos el contenedor HTML para el sprite
def sprite_component(sprite_url: str, fallback_id: int = 0) -> str:

    if not sprite_url:
        sprite_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"

    html = (
        f"""<div style="
                margin: 12px 0px;
                min-height: 200px;
                display: flex;
                justify-content: center;
                align-items: center;">"""
        f"""<img src="{sprite_url}" style="
                max-height: 140px;
                filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.3));">"""
        f"</div>"
    )
    return html.replace("\n", "").strip()


# Generamos el contenedor principal, ensambla el sprite_component y type_badges dentro
# de una carta hecha según el tipo principal del Pokemon
def pokemon_card(p_id: int, name: str, types: list[str], sprite_url: str) -> None:

    inject_card_css()

    primary_type = types[0].lower() if types else "normal"
    color_hex = get_type_color(primary_type)

    color_fill_rgba = hexadecimal_to_rgba(color_hex, alpha=0.15)
    color_line_rgba = hexadecimal_to_rgba(color_hex, alpha=0.8)

    badges_html = "".join(type_badge(t) for t in types).replace("\n", "").strip()
    image_html = (
        sprite_component(sprite_url, fallback_id=p_id).replace("\n", "").strip()
    )

    card_html = f"""
    <div class="poke-card" style="
            background-color: {color_fill_rgba};
            border: 2px solid {color_line_rgba};
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    ">
        <div style="text-align: right; width: 100%;">
            <span style="
                color: {color_hex};
                font-weight: bold;
                font-size: 14px;
            ">#{p_id:04d}</span>
        </div>
        <h3 style="
            color: var(--text-color);
            margin: 5px 0px 10px 0px;
            text-transform: capitalize;
            font-size: 20px;
        ">{name}</h3>
        {image_html}
        <div style="margin: 12px; display: flex; justify-content: center;">
            {badges_html}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


def pokemon_collectible_card(
    p_id: int,
    name: str,
    types: list[str],
    sprite_url: str,
    hp: int,
    attack: int,
    special_attack: int,
    defense: int,
    special_defense: int,
    speed: int,
    base_exp: int,
    abilities: list[str],
) -> None:

    inject_card_css()

    primary_type = types[0] if types else "normal"
    color_hex = get_type_color(primary_type.lower())

    color_fill_rgba = hexadecimal_to_rgba(color_hex, alpha=0.18)
    color_line_rgba = hexadecimal_to_rgba(color_hex, alpha=0.9)

    badges_html = "".join(type_badge(type) for type in types).replace("\n", "").strip()
    image_html = (
        sprite_component(sprite_url, fallback_id=p_id).replace("\n", "").strip()
    )

    abilities_clean = [a.replace("-", "").upper() for a in abilities]
    abilities_str = ", ".join(abilities_clean)

    collectible_html = f"""
    <style>
        .card-canvas {{
            width: 340px;
            height: 480px;
            border-radius: 18px;
            padding: 12px;
            background: {hexadecimal_to_rgba(color_hex, 0.6)};
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
            border: 4px solid #e0c068;
            margin: auto;
        }}
        .card-background-pattern {{
            position: absolute;
            inset: 0;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(
                            circle at 50% 30%, {color_fill_rgba}, transparent 70%
                        ),
                        repeating-conic-gradient(from 0deg, rgba(255, 255, 255, 0.1)
                        0deg 20deg, transparent 20deg 40deg);
            z-index: 1;
        }}
        .card-content {{
            position: relative;
            z-index: 2;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        .inner-image-box {{
            margin: 5px;
            height: 200px;
            background: {color_line_rgba};
            border: 4px solid rgba(255, 255, 255, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 5px;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4)
        }}
        .inner-image-box img {{
            transform: scale(1.5);
            height: 160px;
            width: 210px;
            z-index: 11;
            filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.4));
        }}
        .stats-box {{
            background: rgba(255, 255, 255, 0.95);
            margin-top: 10px;
            padding: 20px;
            border-radius: 5px;
            flex-grow: 1;
            color: #111;
            font-family: sans-serif;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2)
        }}
    </style>
    <div class='card-canvas'>
        <div class='card-background-pattern'></div>
        <div class='card-content'>
            <!-- Header -->
            <div style='
                display: flex;
                justify-content: space-between;
                padding: 5px 10px;
                font-weight: bold;
                color: white;
                text-shadow: 1px 1px 3px black;
                font-family: sans-serif;
            '>
                <span style='font-size: 1.2em;'>{name.upper()}</span>
                <span style='
                    color: #fdeec4;
                    font-size: 1.1em
                '>HP {hp}</span>
            </div>
            <!-- Imagen Shiny -->
            <div class='inner-image-box'>
                {image_html}
            </div>
            <!-- Cuerpo de la carta-->
            <div class='stats-container'>
                <div style='
                    margin-bottom: 8px;
                    display: flex;
                    justify-content: flex-start;'>
                    {badges_html}
                </div>
                <p style='
                    font-size: 0.9em;
                    font-weight: bold;
                    margin: 0;
                    color: #666;'>HABILIDADES</p>
                <p style= '
                    font-size: 1.0em;
                    font-weight: bold;
                    margin-bottom: 12px;
                    color: #111'>
                    {abilities_str}
                </p>
                <div style='
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 8px;
                    font-size: 1em;
                    font-family: monospace;'>
                    <div><b>ATK:</b> {attack}</div>
                    <div><b>SP ATK:</b> {special_attack}</div>
                    <div><b>DEF:</b> {defense}</div>
                    <div><b>SP DEF:</b> {special_defense}</div>
                    <div><b>VEL:</b> {speed}</div>
                    <div><b>EXP:</b> {base_exp}</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(collectible_html.replace("\n", "").strip(), unsafe_allow_html=True)
