"""
En este módulo se encuentra el componente visual para representar
el árbol evolutivo
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def _render_single_pokemon_block(
    name: str, sprite_url: str, key_suffix: str = ""
) -> None:

    st.markdown(
        f"""
        <div style="
            background-color: #1A222D;
            padding: 16px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(0,0,0,0.2);
            margin-bottom: 15px;
        ">
            <img src="{sprite_url}" style="
                width: 130px;
                height: 130px;
                object-fit: contain;
                display: block;
                margin: 0 auto;" />
            <strong style="
                color: #FFFFFF;
                display: block;
                margin-top: 12px;
                font-size: 16px;
                text-transform: capitalize;">
                {name}
            </strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    btn_key = f"btn_evo_{name}_{key_suffix}" if key_suffix else f"btn_evo_{name}"

    if st.button(f"Ver {name.capitalize()}", key=btn_key, use_container_width=True):
        st.session_state["pokemon_seleccionado"] = name
        st.rerun()


def _get_requirement_text(poke_node: dict[str, Any]) -> str:

    details_list = poke_node.get("evolution_details", [])

    if not details_list or not isinstance(details_list, list):
        return "Especial"

    details = details_list[0]

    if not details:
        return "Especial"

    gender_req = ""
    if details.get("gender") == 1:
        gender_req = " (Hembra)"
    elif details.get("gender") == 2:
        gender_req = " (Macho)"

    if details.get("min_level"):
        return f"Nivel {details['min_level']}{gender_req}"

    if details.get("item"):
        item_name = f"{details['item']}".replace("-", " ").title()
        return f"{item_name}{gender_req}"

    if details.get("location"):
        loc_name = f"{details['location']}".replace("-", " ").title()
        return f"En {loc_name}"

    happiness = details.get("min_happiness")
    time_day = details.get("time_of_day")

    if happiness and time_day:
        return f"Amistad ({happiness}) + {time_day.title()}{gender_req}"

    if happiness:
        return f"Amistad ({happiness}){gender_req}"

    if time_day:
        return f"Evolución de  {time_day.title()}{gender_req}"

    return "Evolución / Esp."


# Creamos una función que renderice un árbol de evoluciones de forma inteligente
# si un Pokemon tiene distintas ramificaciones, lo reconoce,
# y si no lo renderiza de forma lineal
def render_evolution_tree(evolution_tree: dict[str, Any]) -> None:

    st.markdown("---")
    st.markdown("#### 🧬 Cadena de Evolución")

    if not evolution_tree:
        st.caption("Este Pokemon no posee una cadena evolutiva registrada")
        return

    # Generamos una lista en la que se almacenan todas las transiciones de padre a hijo
    direct_children = []

    def extract_nodes(node: dict[str, Any]) -> None:
        parent_name = node.get("name", "")
        parent_sprite = node.get("sprite_url", "")
        children = node.get("children", [])

        for child in children:
            direct_children.append(
                {
                    "parent_name": parent_name,
                    "parent_sprite": parent_sprite,
                    "child_node": child,
                    "child_name": child.get("name", ""),
                    "child_sprite": child.get("sprite_url", ""),
                }
            )

            # Verificamos todas las posibles evoluciones de un hijo (nodo)
            extract_nodes(child)

    # Extraemos las evoluciones de toda la extructura del JSON
    extract_nodes(evolution_tree)

    if not direct_children:
        st.caption("Este espécimen no tiene líneas evolutivas conocidas")

        return

    for idx, dir in enumerate(direct_children):
        col_base, col_flechas, col_resultados = st.columns([1.2, 0.8, 1.2], gap="small")

        p_name = dir["parent_name"]
        c_name = dir["child_name"]
        p_sprite = dir["parent_sprite"]
        c_sprite = dir["child_sprite"]

        with col_base:
            st.write("")
            _render_single_pokemon_block(
                name=p_name, sprite_url=p_sprite, key_suffix=f"row_{idx}_from_{p_name}"
            )

        with col_flechas:
            req = _get_requirement_text(dir["child_node"])

            st.markdown(
                f"""
                    <div style="
                        text-align: center;
                        margin-top: 75px;
                        margin-bottom: 20px;
                    ">
                        <span style="
                            font-size: 32px;
                            color: var(--primary-color);
                            display: block;
                            font-weight: bold;
                            line-weight: 1;
                        ">➡</span>
                        <span style="
                            background-color: rgba(255,75,75,0.1);
                            color: #FF4B4B;
                            padding: 4px 10px;
                            border-radius: 8px;
                            font-size: 12px;
                            font-weight: 700;
                            display: inline-block;
                            margin-top: 8px;
                            line-height: 1.2;
                        ">{req}</span>
                    </div>
                    """,
                unsafe_allow_html=True,
            )

            with col_resultados:
                _render_single_pokemon_block(
                    name=c_name,
                    sprite_url=c_sprite,
                    key_suffix=f"row_{idx}_to_{c_name}",
                )
