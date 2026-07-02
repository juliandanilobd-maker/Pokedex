from __future__ import annotations

import datetime

import streamlit as st
from components.detail_panel import render_pokemon_detail_panel
from utils.colors import get_type_color

st.set_page_config(
    page_title="Pokedex - Búsqueda Individual",
    page_icon="🔍",
    layout="wide",
)

if "pokemon_seleccionado" not in st.session_state:
    st.session_state.pokemon_seleccionado = None


@st.cache_data
def _get_pokemon_of_the_day_id(
    today_date: datetime.date, total_pokemon: int = 1025
) -> int:
    date_score = today_date.year + (today_date.month * 31) + today_date.day
    return (date_score % total_pokemon) + 1


@st.cache_data(show_spinner="Accediendo a la base de datos")
def _fetch_pokemon_data(identifier: str) -> tuple[dict, dict, dict | None]:
    from api.backend_client import BackendClient

    backend_client = BackendClient()

    full_response = backend_client.get_pokemon_full_detail(identifier)

    poke_data = full_response.get("pokemon") or {}

    effectiveness_data = full_response.get("effectiveness") or {}

    try:
        evo_data = full_response.get("evolution")

    except Exception:
        evo_data = None

    return poke_data, effectiveness_data, evo_data


if st.session_state.pokemon_seleccionado:
    col_back, _ = st.columns([1.5, 4])
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
        <p style="
            opacity: 0.7;
            margin-bottom: 25px;
        ">
            Ingresa las credenciales del espécimen en la barra de busqueda,
            o analiza nuestra sugerencia diaria de entrenamiento.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_input, col_btn = st.columns([4, 1], gap="small", vertical_alignment="bottom")

    with col_input:
        st.markdown(
            """
            <label style="
                font-size: 14px;
                font-weight: bold;
                opacity: 0.9;
            ">Identificador Pokemon</label>
            """,
            unsafe_allow_html=True,
        )
        pokemon_name = (
            st.text_input(
                "Identificador del Pokemon",
                placeholder="Ejemplo: pikachu, charizard, 149",
                label_visibility="collapsed",
            )
            .strip()
            .lower()
        )

    with col_btn:
        searched_clicked = st.button("Buscar", type="primary", use_container_width=True)

    if searched_clicked and pokemon_name:
        st.session_state.pokemon_seleccionado = pokemon_name
        st.rerun()

    st.markdown("---")

    today = datetime.date.today()
    pokemon_dia_id = str(_get_pokemon_of_the_day_id(today))

    try:
        poke_dia, eff_dia, evo_dia = _fetch_pokemon_data(pokemon_dia_id)

        dia_name = poke_dia.get("name", "Desconocido").capitalize()
        dia_types = poke_dia.get("types", ["normal"])
        dia_color = get_type_color(dia_types[0])
        dia_flavor = poke_dia.get("flavor_text", "Sin descripción registrada")

        st.markdown(
            f"""
            <div style="
                background-color: linear-gradient(
                                      135deg, rgba(
                                        255, 165, 0, 0.08
                                      ) 0%, rgba(0,0,0,0) 100%);
                padding: 20px;
                border-radius: 12px;
                border-left: 5px solid orange;
                margin-bottom: 25px;
            ">
                <span style="
                    background-color: orange;
                    color: black;
                    padding: 3px 8px;
                    border-radius: 5px;
                    font-size: 11px;
                    font-weight: bold;
                    letter-spacing: 1px;
                ">🎯 Recomendación Estratégica del Día:</span>
                <h4 style="
                    margin-top: 10px;
                    margin-bottom: 5px;
                ">¿No sabes que Pokemon buscar?</4>
                <p style="
                    opacity: 0.8;
                    font-size: 14px;
                    margin-bottom: 0px;
                ">
                Mientras decides a quién buscar, analiza la ficha técnica de
                <strong style="
                    color: {dia_color};
                    text-transform: capitalize;
                    font-weight: bold;
                ">{dia_name}</strong> (# {poke_dia.get("id", 0):03d}).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        render_pokemon_detail_panel(
            pokemon_data=poke_dia,
            effectiveness_data=eff_dia,
            evolution_data=evo_dia,
        )

    except Exception as e:
        st.caption(f"Telemetría del Pokemon del día inactiva: {e}")
