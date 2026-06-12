"""
En este módulo se encuentra el componente visual para representar
el árbol evolutivo
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from frontend.streamlit_folder.components.cards import sprite_component


def _render_single_pokemon_block(name: str, p_id: int, sprite_url: str) -> None:

    image_html = sprite_component(sprite_url)
    st.markdown(
        f"""
        <div style="
            text-align: center;
            margin-bottom: 15px;
        ">
            {image_html}
            <string style="
                text-transform: capitalize;
                font-size: 14px;
            ">{name}</strong>
            <br>
            <span style="
                opacity: 0.6;
                font-size: 11px;
            ">#{p_id:03d}</span>
            </div>
        """,
        unsafe_allow_html=True,
    )


def _get_requirement_text(poke_node: dict[str, Any]) -> str:

    if poke_node.get("min_level"):
        return f"Nivel {poke_node['min_level']}"

    if poke_node.get("item"):
        return f"{poke_node['item']}".replace("-", " ").title()

    happiness = poke_node.get("min_happiness")
    time_day = poke_node.get("time_of_day")

    if happiness and time_day:
        return f"Felicidad ({happiness}) + {time_day.title()}"

    if happiness:
        return f"Felicidad ({happiness})"

    if time_day:
        return f"Evolución de  {time_day.title()}"

    return "Especial"


# Creamos una función que renderice un árbol de evoluciones de forma inteligente
# si un Pokemon tiene distintas ramificaciones, lo reconoce,
# y si no lo renderiza de forma lineal
def render_evolution_tree(evolution_tree: dict[str, Any]) -> None:

    st.markdown("---")
    st.markdown("#### 🧬 Cadena de Evolución")

    if not evolution_tree:
        st.caption("Este Pokemon no posee una cadena evolutiva registrada")
        return

    direct_evolutions = evolution_tree.get("evolutions", [])

    # Iniciamos con una evolución ramificada
    if len(direct_evolutions) > 1:
        col_base, col_flechas, col_resultados = st.columns([1, 0.6, 1.2], gap="small")

        with col_base:
            st.markdown("<div style='height: 40 px;'></div>", unsafe_allow_html=True)
            _render_single_pokemon_block(
                name=evolution_tree.get("name", ""),
                p_id=evolution_tree.get("id", 0),
                sprite_url=evolution_tree.get("sprite_url", ""),
            )

        for evo in direct_evolutions:
            with col_flechas:
                req = _get_requirement_text(evo)

                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        margin-top: 60px;
                        margin-bottom: 40px;
                    ">
                        <span style="
                            font-size: 22px;
                            color: var(--primary-color);
                            display: block;
                            margin-bottom: -5px;
                        ">➡</span>
                        <small style="
                            opacity: 0.7;
                            font-size: 10px;
                            line-height: 1.1;
                            display: block;
                        ">{req}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_resultados:
                _render_single_pokemon_block(
                    name=evo.get("name", ""),
                    p_id=evo.get("id", 0),
                    sprite_url=evo.get("sprite_url", ""),
                )

        return

    tree: list[dict[str, Any]] = []
    current_node = evolution_tree

    while current_node:
        tree.append(current_node)
        next_nodes = current_node.get("evolutions", [])
        current_node = next_nodes[0] if next_nodes else None

    num_elements = len(tree) + (len(tree) - 1)
    col_weights = [1.0 if i % 2 == 0 else 0.4 for i in range(num_elements)]
    columns = st.columns(col_weights, gap="small")

    tree_index = 0
    for i, col in enumerate(columns):
        with col:
            if i % 2 == 0:
                poke = tree[tree_index]
                _render_single_pokemon_block(
                    name=poke.get("name", ""),
                    p_id=poke.get("id", 0),
                    sprite_url=poke.get("sprite_url", ""),
                )

                tree_index += 1

            else:
                next_poke = tree[tree_index]
                req = _get_requirement_text(next_poke)
                st.markdown(
                    f"""
                    <div style="
                        text-align: center;
                        margin-top: 55px;
                    ">
                        <div style="
                            font-size: 24px;
                            color: var(--primary-color);
                        ">➡</div>
                        <small style="
                            opacity: 0.7;
                            font-size: 11px;
                            display: block;
                            line-height: 1.1;
                        ">{req}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
