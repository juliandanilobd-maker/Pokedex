import streamlit as st


def main() -> None:

    # Establecemos la configuración global única de la interfaz
    st.set_page_config(page_title="Pokedex", page_icon="◓", layout="wide")

    # Inicializamos el Estado Global de la sesión
    if "pokemon_seleccionado" not in st.session_state:
        st.session_state.pokemon_seleccionado = None

    if "pokemon_dia_id" not in st.session_state:
        st.session_state.pokemon_dia_id = None

    # Renderizado de la pantalla de bienvenida
    st.title("◓ Pokedex")
    st.caption(
        "Explora la Pokedex interactiva, busca estadísticas, "
        "evoluciones y características especiales de tus Pokémon favoritos."
    )
    st.markdown("---")

    col1, col2 = st.columns([1.3, 1], gap="large")

    with col1:
        # fmt: off
        st.markdown(
            """
            ## ¡Bienvenido Entrenador Pokemon!

            Utiliza el menú desplegable de la **barra lateral** para navegar
            por las secciones del sistema:

            * **🏠 Home / Galería:** Filtra colecciones completas por tipos,
            generación y estadísticas base.
            * **🔍 Búsqueda Individual:** Inspecciona a fondo un Pokemon,
            su gráfico de rendimiento, debilidades elementales y cadena evolutiva.
            """
        )

    with col2:
        st.image(
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
            "sprites/pokemon/other/official-artwork/25.png",
            width=320,
            caption="Sistema de Gestión Pokemon v0.4.0 (MVP)",
        )

    st.markdown("---")
    st.info(
        "💡 Consejo: Selecciona una página en la barra lateral izquierda"
        "para comenzar a explorar."
    )


if __name__ == "__main__":
    main()
