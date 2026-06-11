import streamlit as st

from frontend.streamlit_folder.views.pokemon_detail_view import render_pokemon_detail

if "pokemon_seleccionado" not in st.session_state:
    st.session_state.pokemon_seleccionado = None

    if st.session_state.pokemon_seleccionado:
        if st.button("⬅ Volver al Buscador", type="secondary"):
            st.session_state.pokemon_seleccionado = None
            st.rerun()

        render_pokemon_detail(
            client=None, identifier=st.session_state.pokemon_seleccionado
        )

    else:
        st.subheader("🔍 Inspección Individual de Pokemon")
        st.caption("Ingresa el nombre o ID de un Pokemon para analizar sus datos")

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
