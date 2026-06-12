from __future__ import annotations

import streamlit as st

from frontend.streamlit_folder.api.backend_client import BackendClient
from frontend.streamlit_folder.components.cards import sprite_component

st.set_page_config(
    page_title="Pokedex - Buscador de Estadísticas", page_icon="🎛️", layout="wide"
)

POKEMON_TYPES = {
    "Todos": "Todos",
    "Normal": "normal",
    "Fuego": "fire",
    "Agua": "water",
    "Planta": "grass",
    "Electrico": "electric",
    "Hielo": "ice",
    "Lucha": "fighting",
    "Veneno": "poison",
    "Tierra": "ground",
    "Volador": "flying",
    "Psíquico": "psychic",
    "Bicho": "bug",
    "Roca": "rock",
    "Fantasma": "ghost",
    "Dragon": "dragon",
    "Hierro": "steel",
    "Hada": "fairy",
}

GENERATIONS = {
    "Todas": 0,
    "Primera generación (Kanto)": 1,
    "Segunda generación (Johto)": 2,
    "Tercera generación (Hoenn)": 3,
    "Cuarta generación (Sinnoh)": 4,
    "Quinta generación (Unova)": 5,
    "Sexta generación (Kalos)": 6,
    "Séptima generación (Alola)": 7,
    "Octava generación (Galar)": 8,
    "Novena generación (Paldea)": 9,
}


def _fetch_filtered_pokemon(
    tipo: str,
    gen: int,
    min_hp: int,
    min_atk: int,
    min_def: int,
    min_spd: int,
    min_base_xp: int,
) -> list[dict]:

    backend_client = BackendClient()

    return backend_client.filter_pokemons(
        type=tipo,
        generation=gen,
        min_hp=min_hp,
        min_atk=min_atk,
        min_def=min_def,
        min_spd=min_spd,
        min_base_xp=min_base_xp,
    )


st.markdown("## 🎛️ Buscador de Equipos Avanzados")
st.markdown("Filtra los especímenes por sus estadísticas, tipos o generación")

with st.expander("🔮 Parámetros de filtrado", expanded=True):
    col_fil_1, col_fil_2 = st.columns(2, gap="medium")

    with col_fil_1:
        selected_type_es = st.selectbox(
            "Tipo Elemental Principal: ", list(POKEMON_TYPES.keys())
        )
        selected_type_en = POKEMON_TYPES[selected_type_es]

        selected_gen_label = st.selectbox(
            "Región / Generación", list(GENERATIONS.keys())
        )

        selected_gen_value = GENERATIONS[selected_gen_label]

    with col_fil_2:
        min_hp = st.slider("HP mínimo", 0, 150, 10)
        min_attack = st.slider("Ataque mínimo", 0, 150, 10)
        min_defense = st.slider("Defensa mínima", 0, 150, 10)
        min_speed = st.slider("Velocidad mínima", 0, 150, 10)
        min_base_exp = st.slider("Experiencia base mínima", 0, 150, 10)

results = _fetch_filtered_pokemon(
    tipo=selected_type_en,
    gen=selected_gen_value,
    min_hp=min_hp,
    min_atk=min_attack,
    min_def=min_defense,
    min_spd=min_speed,
    min_base_xp=min_base_exp,
)

st.markdown("---")
st.markdown(f"### 📋 Especímenes encontrados {len(results)}")

if not results:
    st.warning("No se encontraron especímenes que cumplan con los filtros")

else:
    COLUMS_PER_ROW = 4
    cols = st.columns(COLUMS_PER_ROW, gap="small")

    for index, poke in enumerate(results):
        with cols[index % COLUMS_PER_ROW]:
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(255, 255, 255, 0.03);
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #333;
                    text-align: center;
                    margin-bottom: 10px;
                ">
                    {sprite_component(poke["sprite"])}
                    <div style="
                        text-transform: capitalize;
                        font-weight: bold;
                        font-size: 14px;
                        margin-top: 5px;
                    ">
                        # {poke.get("name", "Desconocido")}
                    </div>
                    <div style="
                        opacity: 0.6;
                        font-size: 11px;
                        margin-top: 2px;
                        margin-bottom: 5px;
                    ">
                        # {poke.get("id", 0):03d}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_key = f"btn_det_{poke.get('id', index)}"
            if st.button("Ver Detalles", key=btn_key, use_container_width=True):
                st.session_state.pokemon_seleccionado = str(poke.get("id", ""))
                st.rerun()
