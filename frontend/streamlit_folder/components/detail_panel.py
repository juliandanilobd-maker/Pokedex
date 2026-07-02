"""
En este módulo se encuentra el componente que orquesta el layout de la vista al detalle
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from components.cards import (
    pokemon_collectible_card as render_full_card,
    type_badge,
)
from components.charts import render_stats_radar_chart
from components.evolutions import render_evolution_tree
from utils.colors import get_type_color

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

    return POKEMON_TYPES.get(type_en.lower().strip(), type_en)


# Creamos una función que ensamble el panel detallado del Pokemon
def render_pokemon_detail_panel(
    pokemon_data: dict[str, Any],
    effectiveness_data: dict[str, Any],
    evolution_data: dict[str, Any] | None = None,
) -> None:

    if not pokemon_data:
        st.warning("No se encontraron datos para este Pokemon")
        return

    id = pokemon_data.get("id", 0)
    name = pokemon_data.get("name", "Desconocido")
    sprite_url = pokemon_data.get("sprite_url", "")
    sprite_shiny = pokemon_data.get("sprite_shiny", "")
    types = pokemon_data.get("types", ["normal"])
    primary_color = get_type_color(types[0])

    weight_kg = pokemon_data.get("weight", 0)
    height_m = pokemon_data.get("height", 0)
    base_exp = pokemon_data.get("base_experience", 0)
    abilities = pokemon_data.get("abilities", "")
    flavor_text = pokemon_data.get("flavor_text_entry", "Sin descripción registrada")

    api_stats = pokemon_data.get("stats", {})
    stats_map = {
        "hp": api_stats.get("hp", 0),
        "attack": api_stats.get("attack", 0),
        "defense": api_stats.get("defense", 0),
        "speed": api_stats.get("speed", 0),
        "special_attack": api_stats.get("special-attack", 0),
        "special_defense": api_stats.get("special-defense", 0),
    }

    card_stats_map = {
        "hp": api_stats.get("hp", 0),
        "attack": api_stats.get("attack", 0),
        "defense": api_stats.get("defense", 0),
        "speed": api_stats.get("speed", 0),
        "special_attack": api_stats.get("special-attack", 0),
        "special_defense": api_stats.get("special-defense", 0),
        "base_exp": base_exp,
        "abilities": abilities,
    }

    cleaned_hex = primary_color.strip().lstrip("#")
    r, g, b = (int(cleaned_hex[i : i + 2], 16) for i in (0, 2, 4))

    style_background = f"""
        <style>
            .stApp {{
                background: radial-gradient(
                                circle at top right, rgba(
                                    {r}, {g}, {b}, 0.15
                                ), transparent),
                            radial-gradient(
                                circle at bottom left, rgba(
                                    {r}, {g}, {b}, 0.05
                                ), transparent);
                background-attachment: fixed;
            }}
        </style>
        """

    st.markdown(style_background, unsafe_allow_html=True)

    col_izquierda, col_central, col_derecha = st.columns([1.8, 3.0, 1.5], gap="medium")

    with col_izquierda:
        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 10px; margin-bottom: 5px;">
                <span style="font-size: 26px;"> ◓ </span>
                <h2 style="
                    margin: 0;
                    font-size: 28px;
                    font-weight: 800;
                    color: #1E1E1E;">
                    #{id:03d} - {name.capitalize()}
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if sprite_url:
            st.image(sprite_url, use_container_width=True)

        else:
            st.image(
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png",
                width=150,
            )

        badges_html = ""
        for t in types:
            tipo_es = get_type_translated(t.lower().strip())
            color_type = get_type_color(t.lower().strip())

            badges_html += f"""
            <span style="
                background-color: {color_type};
                color: white;
                padding: 6px 16px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 15px;
                text-transform: uppercase;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">{tipo_es}</span>
            """

        st.markdown(
            f"""
            <div style="
                margin-top: -10px;
                margin-bottom: 25px;
                display: flex;
                gap: 10px;">
                {badges_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                font-size: 15px;
                color: #4A4A4A;
                line-height: 1.6;
                font-family: sans-serif;">
                <p style="
                    margin: 4px 0;">
                    <strong>Altura:</strong> {height_m:.1f} m &nbsp;|&nbsp;
                    <strong>Peso:</strong> {weight_kg:.1f} kg</p>
                <p style="margin: 4px 0;"><strong>Exp. Base:</strong> {base_exp}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        abilities_str = (
            ", ".join([a.title() for a in abilities])
            if isinstance(abilities, list)
            else str(abilities)
        )

        st.markdown(
            f"""
            <div style="
                background-color: rgba(0,0,0,0.05);
                border-left: 4px solid {primary_color};
                padding: 10px 15px;
                border-radius: 8px;
                margin-top: 15px;
            ">
                <span style="
                    font-size: 13px;
                    color: #333333;
                    font-weight: 600;
                    display: block;
                    margin-bottom: 2px;">
                    🥊 Habilidades
                </span>
                <span style="
                    font-size: 14px;
                    color: #555555;
                    font-family: monospace;">
                    {abilities_str}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_central:
        st.markdown(
            """
            <h4 style="
                text-align: center;
                margin-bottom: -10px;
            ">📊 Métricas Base de Combate</h4>
            """,
            unsafe_allow_html=True,
        )

        fig_radar = render_stats_radar_chart(
            stats=stats_map, pokemon_name=name, color_hex=primary_color
        )

        st.plotly_chart(
            fig_radar,
            use_container_width=True,
            config={"displayModeBar": False, "responsive": True},
        )

    with col_derecha:
        st.markdown(
            """
            <h4 style="
                margin-bottom: 15px;
            ">⚔️ Afinidades Estratégicas</h4>
            """,
            unsafe_allow_html=True,
        )

        weaknesses_x4 = effectiveness_data.get("weaknesses_x4", [])
        weaknesses = effectiveness_data.get("weaknesses", [])
        resistances = effectiveness_data.get("resistances", [])
        resistances_x025 = effectiveness_data.get("resistances_x025", [])
        immunities = effectiveness_data.get("immunities", [])

        if weaknesses_x4:
            w_x4_html = "".join(
                type_badge(str(w_x4), get_type_translated(str(w_x4)))
                for w_x4 in weaknesses_x4
            )
            st.markdown(
                '<small style="'
                "opacity: 0.7;"
                "display: block;"
                'margin-top: 10px"> ⚔️ DAÑO CRITICO (RECIBE DAÑO x4.0)</small>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="margin-top: 5px;">{w_x4_html}</div>',
                unsafe_allow_html=True,
            )
        if weaknesses:
            w_html = "".join(
                type_badge(str(w), get_type_translated(str(w))) for w in weaknesses
            )
            st.markdown(
                '<small style="'
                "opacity: 0.7;"
                "display: block;"
                'margin-top: 10px"> 🔥 DAÑO AUMENTADO (RECIBE DAÑO x2.0)</small>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="margin-top: 5px;">{w_html}</div>', unsafe_allow_html=True
            )

        if resistances:
            r_html = "".join(
                type_badge(str(r), get_type_translated(str(r))) for r in resistances
            )
            st.markdown(
                '<small style="'
                "opacity: 0.7;"
                "display: block;"
                'margin-top: 10px;"> 🛡️ RESISTENTE (DAÑO x0.5)</small>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="margin-top: 5px;">{r_html}</div>', unsafe_allow_html=True
            )

        if resistances_x025:
            r_x025_html = "".join(
                type_badge(str(r_x025), get_type_translated(r_x025))
                for r_x025 in resistances_x025
            )
            st.markdown(
                '<small style="'
                "opacity: 0.7;"
                "display: block;"
                'margin-top: 10px"> ⛓️ DAÑO REDUCIDO (DAÑO x0.25)</small>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="margin-top: 5px;">{r_x025_html}</div>',
                unsafe_allow_html=True,
            )

        if immunities:
            i_html = "".join(
                type_badge(str(i), get_type_translated(i)) for i in immunities
            )
            st.markdown(
                '<small style="'
                "opacity: 0.7;"
                "display: block;"
                'margin-top: 10px;"> 🌟 INMUNIDADES (DAÑO x0.0)</small>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="margin-top: 5px;">{i_html}</div>', unsafe_allow_html=True
            )

    st.write("")
    if flavor_text and isinstance(flavor_text, dict):
        text = flavor_text.get("text", "")
        version = flavor_text.get("version", "Desconocida").capitalize()
        language = flavor_text.get("language", "es")

        st.markdown(
            f"""
            <div style="
                background-color: rgba({r}, {g}, {b}, 0.06);
                padding: 20px;
                border-radius: 12px;
                border-left: 5px solid {primary_color};
                font-style: italic;
                margin-top: 25px;
                margin-bottom: 5px;
                font-size: 16px;
                line-height: 1.6;
                box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            ">
                "{text}"
                <span style="
                    display: block;
                    font-style: normal;
                    font-size: 12px;
                    font-weight: bold;
                    margin-top: 10px;
                    opacity: 0.7;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;">
                    📖 Descripción registrada en Pokemon Edicion **{version}**
                    ({language.upper()})
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div style="
                background-color: rgba(0,0,0,0.03);
                padding: 15px;
                border-radius: 12px;
                border-left: 5px solid #CCCCCC;
                margin-top: 25px;
                font-size: 14px;
                color: #666666;">
                Este Pokemon no posee una descripción biográfica en los registros
            </div>
            """,
            unsafe_allow_html=True,
        )

    if evolution_data:
        render_evolution_tree(evolution_data)

    st.markdown("---")
    st.markdown("#### 🃏 Carta")

    _, col_carta_centrada, _ = st.columns([1, 1.5, 1])
    with col_carta_centrada:
        render_full_card(
            p_id=id, name=name, types=types, sprite_url=sprite_shiny, **card_stats_map
        )
