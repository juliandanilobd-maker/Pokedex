from __future__ import annotations

import streamlit as st
from api.backend_client import BackendClient
from components.cards import pokemon_card as render_full_card

st.set_page_config(
    page_title="Pokedex - Buscador de Estadísticas", page_icon="🎛️", layout="wide"
)

if "resultados_busqueda" not in st.session_state:
    st.session_state.resultados_busqueda = None


st.markdown("## 🎛️ Panel de Filtrado Avanzado")
st.markdown(
    """
    <p style="
        opacity: 0.7;
    ">
    Refina tu búsqueda combinando tipos elementales y
    rangos estadísticos específicos.</p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

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

TRANSLATE_TYPES = {v: k for k, v in POKEMON_TYPES.items() if v != "Todos"}

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


with st.sidebar:
    st.header("Parámetros de Selección")
    type_es = st.selectbox(
        "Tipo Elemental", options=list(POKEMON_TYPES.keys()), index=0
    )
    type_en = POKEMON_TYPES[type_es]

    gen_es = st.selectbox(
        "Generación / Región", options=list(GENERATIONS.keys()), index=0
    )
    gen_id = GENERATIONS[gen_es]

    st.markdown("---")

    st.subheader("Límites de Atributos")

    min_hp = st.slider("HP mínimo", 0, 150, 0)
    min_attack = st.slider("Ataque mínimo", 0, 150, 0)
    min_defense = st.slider("Defensa mínima", 0, 150, 0)
    min_speed = st.slider("Velocidad mínima", 0, 150, 0)
    min_base_exp = st.slider("Experiencia base mínima", 0, 150, 0)

params = {}

if type_en != "Todos":
    params["pokemon_type"] = type_en

if gen_id > 0:
    params["generation"] = int(gen_id)

if min_hp > 0:
    params["min_hp"] = int(min_hp)

if min_attack > 0:
    params["min_attack"] = int(min_attack)

if min_defense > 0:
    params["min_defense"] = int(min_defense)

if min_speed > 0:
    params["min_speed"] = int(min_speed)

if min_base_exp > 0:
    params["min_base_exp"] = int(min_base_exp)

params.update(
    {
        "min_hp": int(min_hp),
        "min_attack": int(min_attack),
        "min_defense": int(min_defense),
        "min_speed": int(min_speed),
        "min_base_exp": int(min_base_exp),
    }
)

backend_client = BackendClient()

if st.button("Aplicar Filtros", type="primary"):
    try:
        st.session_state.resultados_busqueda = backend_client.filter_pokemons(params)

    except Exception as e:
        st.error("⚠️ Ocurrió un error al procesar los filtros en el Servidor.")
        st.code(str(e))


pokemon_list = st.session_state.resultados_busqueda

if st.session_state.resultados_busqueda is not None:
    if not isinstance(pokemon_list, list) or not pokemon_list:
        st.info("⏳ No se encontraron especímenes que cumplan con los criterios")

    else:
        st.success(f"🎯 Se encontraron {len(pokemon_list)} especímenes: ")

        cols = st.columns(4, gap="small")
        for idx, p in enumerate(pokemon_list):
            with cols[idx % 4]:
                p_id = p.get("id", 0)
                name = p.get("name", "Desconocido")
                types = p.get("types", ["normal"])
                sprite_url = p.get("sprite_url", "").strip()

                render_full_card(
                    p_id=p_id, name=name, types=types, sprite_url=sprite_url
                )
