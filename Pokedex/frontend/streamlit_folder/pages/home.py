import streamlit as st

from views.home_view import render_home
from views.pokemon_detail_view import render_pokemon_detail
from api.backend_client import BackendClient

st.set_page_config(layout='wide')

client = BackendClient()

if 'pokemon_seleccionado' not in st.session_state:
    st.session_state.pokemon_seleccionado = None

if "force_reset_home" not in st.session_state:
    st.session_state.force_reset_home =True

if st.session_state.force_reset_home:
    st.session_state.pokemon_seleccionado = None
    st.session_state.force_reset_home = False

if st.session_state.pokemon_seleccionado:
    if st.button('⬅ Volver'):
        st.session_state.pokemon_seleccionado = None
        st.rerun()

    render_pokemon_detail(client, st.session_state.pokemon_seleccionado)
else:

    render_home(client)