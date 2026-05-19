import streamlit as st

from views.pokemon_detail_view import render_pokemon_detail, get_pokemon_of_the_day
from api.backend_client import BackendClient
from utils.constants import COLORS_TYPE_POKEMON
from utils.pokemon_logic import render_random_pokemons, get_random_pokemons_id

st.set_page_config(layout='wide')

client = BackendClient()

if 'pokemon_seleccionado' not in st.session_state:
    st.session_state.pokemon_seleccionado = None

if st.session_state.pokemon_seleccionado:
    if st.button('⬅ Volver'):
        st.session_state.pokemon_seleccionado = None
        st.rerun()

    render_pokemon_detail(client, st.session_state.pokemon_seleccionado)

else: 
    pokemon_name = st.text_input('Nombre del Pokemon', placeholder='Ejemplo: pikachu, charizard, o coloca el ID del Pokemon que desees encontrar').strip().lower()

    search_clicked = st.button('Buscar', type='primary')
    
    if search_clicked and pokemon_name:
        st.session_state.pokemon_seleccionado = pokemon_name
        st.session_state.force_reset_home = True
        st.rerun()

    if not search_clicked:

        random_id = get_random_pokemons_id()

        render_random_pokemons(client, random_id)

        

       

    