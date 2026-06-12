"""
En este módulo se encuentra el componente que orquesta el layout de la vista al detalle
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from frontend.streamlit_folder.components.cards import type_badge
from frontend.streamlit_folder.components.charts import render_stats_radar_chart
from frontend.streamlit_folder.components.evolutions import render_evolution_tree
from frontend.streamlit_folder.utils.styles import get_type_color


# Creamos una función que ensamble el panel detallado del Pokemon
def render_pokemon_detail_panel(
    pokemon_data: dict[str, Any],
    effectiveness_data: dict[str, Any],
    evolution_data: dict[str, Any] | None = None,
) -> None:

    name = pokemon_data.get("name", "Desconocido")
    types = pokemon_data.get("types", ["normal"])
    primary_color = get_type_color(types[0])

    weight_kg = pokemon_data.get("weight", 0) / 10
    height_m = pokemon_data.get("height", 0) / 10
    base_exp = pokemon_data.get("base_experience", 0)
    flavor_text = pokemon_data.get("flavor_text", "Sin descripción registrada")

    stats_map = {
        "hp": pokemon_data.get("hp", 0),
        "attack": pokemon_data.get("attack", 0),
        "defense": pokemon_data.get("defense", 0),
        "speed": pokemon_data.get("speed", 0),
        "special-attack": pokemon_data.get("special_attack", 0),
        "special-defense": pokemon_data.get("special_defense", 0),
    }

    col_izquierda, col_central, col_derecha = st.columns([1, 1.2, 1], gap="medium")

    with col_izquierda:
        st.markdown(
            f"""
            <h2 style="
                text-transform: capitalize;
                margin-bottom: 0px;
            ">{name}</h2>
            <span style="
                color: {primary_color};
                font-weight: bold;
                font-size: 16px;
            ">
                ID: #{pokemon_data.get("id", 0):04d}
            </span>
            """,
            unsafe_allow_html=True,
        )

        st.image(
            pokemon_data.get("sprite_url", ""),
            use_container_width=True,
        )

        st.markdown(
            f"""
            <table style="
                width: 100%;
                font-size: 14px;
                margin-top: 10px;
                border-collapse: collapse;
            ">
                <tr style="
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                ">
                    <td style="
                        padding: 6px 0;
                        opacity: 0.7;
                    ">Altura</td>
                    <td style="
                        text-align: right;
                        font-weight: bold;
                    ">{height_m} m</td>
                </tr>
                <tr style="
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                ">
                    <td style="
                        padding: 6px 0;
                        opacity: 0.7;
                    ">Peso</td>
                    <td style="
                        text-align: right;
                        font-weight: bold;
                    ">{weight_kg} kg</td>
                </tr>
                <tr>
                    <td style="
                        padding: 6px 0;
                        opacity: 0.7;
                    ">Exp. Base</td>
                    <td style="
                        text-align: right;
                        font-weight: bold;
                    ">{base_exp} XP</td>
                </tr>
            </table>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="
                background-color: rgba(255, 255, 255, 0.04);
                padding: 12px;
                border-radius: 8px;
                border-left: 3px solid {primary_color};
                font-style: italic;
                margin-top: 15px;
                font-size: 13.5px;
                line-height: 1.4;
            ">
                "{flavor_text}"
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_central:
        st.markdown(
            """
            <h5 style="
                text-align: center;
                margin-bottom: -10px;
            "> Métricas Base de Combate</h6>
            """,
            unsafe_allow_html=True,
        )

        fig_radar = render_stats_radar_chart(
            stats=stats_map, pokemon_name=name, color_hex=primary_color
        )

        st.plotly_chart(
            fig_radar, use_container_width=True, config={"displayModeBar": False}
        )

    with col_derecha:
        st.markdown("<h5>Afinidades Estratégicas</h5>", unsafe_allow_html=True)

        weaknesses = effectiveness_data.get("weaknesses", [])
        resistances = effectiveness_data.get("resistances", [])
        immunities = effectiveness_data.get("immunities", [])

        if weaknesses:
            w_html = "".join(type_badge(w) for w in weaknesses)
            st.markdown(
                """
                <small style="
                    opacity: 0.7;
                    display: block;
                    margin-top: 10px
                "> 🔥 DEBILIDADDES (DAÑO x2.0)</small>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(w_html, unsafe_allow_html=True)

        if resistances:
            r_html = "".join(type_badge(r) for r in resistances)
            st.markdown(
                """
                <small style="
                    opacity: 0.7;
                    display: block;
                    margin-top: 10px;
                "> 🛡️ RESISTENCIAS (DAÑO x0.5)</small>,
                """,
                unsafe_allow_html=True,
            )
            st.markdown(r_html, unsafe_allow_html=True)

        if immunities:
            i_html = "".join(type_badge(i) for i in immunities)
            st.markdown(
                """
                <small style="
                    opacity: 0.7;
                    display: block;
                    margin-top: 10px
                "> 🌟 INMUNIDADES (DAÑO x0.0)</sall>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(i_html, unsafe_allow_html=True)

    if evolution_data:
        render_evolution_tree(evolution_data)

    st.markdown("---")
    st.markdown("#### 🃏 Licencia Oficial de Entrenador")

    _, col_carta_centrada, _ = st.columns([1, 1.5, 1])
    with col_carta_centrada:
        from frontend.streamlit_folder.components.cards import (
            pokemon_card as render_full_card,
        )

        render_full_card(
            p_id=pokemon_data.get("id", 0),
            name=name,
            types=types,
            sprite_url=pokemon_data.get("sprite_url", ""),
        )
