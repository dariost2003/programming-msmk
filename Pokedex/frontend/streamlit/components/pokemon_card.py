import streamlit as st
from backend.app.clients.pokeapi_client import PokeAPIClient

def render_pokemon_card(pokemon):

    st.image(pokemon['sprite'])

    st.subheader(f'#{pokemon["identifier"]}')