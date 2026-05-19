import random
import streamlit as st


def get_pokemon_of_the_day(client):
    if "pokemon_dia_id" not in st.session_state or st.session_state.pokemon_dia_id is None:
        st.session_state.pokemon_dia_id = random.randint(1, 151)

    return client.get_pokemon(st.session_state.pokemon_dia_id) 
