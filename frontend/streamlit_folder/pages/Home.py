import streamlit as st
from views.home_view import render_home

if "pokemon_seleccionado" not in st.session_state:
    st.session_state.pokemon_seleccionado = None

render_home(client=None)
