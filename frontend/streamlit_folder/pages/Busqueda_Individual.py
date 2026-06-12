from __future__ import annotations

import datetime

import streamlit as st

from frontend.streamlit_folder.components.detail_panel import (
    render_pokemon_detail_panel,
)

st.set_page_config(
    page_title="Pokedex - Búsqueda Individual",
    page_icon="🔍",
    layout="wide",
)

if "pokemon_seleccionado" not in st.session_state:
    st.session_state.pokemon_seleccionado = None


def _get_pokemon_of_the_day_id(total_pokemon: int = 151) -> int:
    today = datetime.date.today()
    date_score = today.year + (today.month * 31) + today.day

    return (date_score % total_pokemon) + 1


def _fetch_pokemon_data(identifier: str) -> tuple[dict, dict, dict | None]:
    from frontend.streamlit_folder.api.backend_client import BackendClient

    backend_client = BackendClient()

    poke_data = backend_client.get_pokemon(identifier)

    effectiveness_data = backend_client.get_effectiveness(identifier)

    try:
        evo_data = backend_client.get_evolution(identifier)

    except Exception:
        evo_data = None

    return poke_data, effectiveness_data, evo_data


if st.session_state.pokemon_seleccionado:
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button(
            "⬅ Volver al Buscador", type="secondary", use_container_width=True
        ):
            st.session_state.pokemon_seleccionado = None
            st.rerun()

    st.write("")

    try:
        poke_data, effectiveness_data, evo_data = _fetch_pokemon_data(
            st.session_state.pokemon_seleccionado
        )

        render_pokemon_detail_panel(
            pokemon_data=poke_data,
            effectiveness_data=effectiveness_data,
            evolution_data=evo_data,
        )

    except Exception as e:
        st.error(
            f"⚠️ Error al conectar con el Servidor: "
            f"'{st.session_state.pokemon_seleccionado}'"
        )
        st.error(f"Detalle técnico: {e}")

else:
    st.markdown(
        """
        <h2 style="
            margin-bottom: 0px;
        ">🔍 Inspección Individual de Pokemon
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            opacity: 0.7;
        ">
        Ingresa las credenciales del espécimen en la barra de búsqueda o analiza nuestra
        sugerencia diara.
        </p>
        """,
        unsafe_allow_html=True,
    )

    pokemon_name = (
        st.text_input(
            "Identificador del Pokemon",
            placeholder="Ejemplo: pikachu, charizard, 149...",
        )
        .strip()
        .lower()
    )

    if st.button("Buscar", type="primary") and pokemon_name:
        st.session_state.pokemon_seleccionado = pokemon_name
        st.rerun()

    st.markdown("---")
    pokemon_dia_id = str(_get_pokemon_of_the_day_id())

    try:
        poke_data, effectiveness_data, evo_data = _fetch_pokemon_data(pokemon_dia_id)

        st.markdown(
            f"""
            <div style="
                background-color: rgba(255, 165, 0, 0.08);
                padding: 12px;
                border-radius: 8px;
                border-left: 4px solid orange;
                margin-bottom: 25px;
                font-size: 14px;
            ">
                🎯 <strong>Recomendación Estratégica del Día:</strong>
                No has ingresado ninguna consulta aún.
                Mientras decides a quién buscar, analiza la ficha técnica de
                <span style="
                    text-transform: capitalize;
                    font-weight: bold;
                ">{poke_data["name"]}</span> (# {poke_data["id"]}).
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_pokemon_detail_panel(
            pokemon_data=poke_data,
            effectiveness_data=effectiveness_data,
            evolution_data=evo_data,
        )

    except Exception as e:
        st.caption(f"Telemetría del Pokemon del día inactiva: {e}")
