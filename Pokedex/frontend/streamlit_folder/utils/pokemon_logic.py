import random
import streamlit as st



def get_pokemon_of_the_day(client):
    if "pokemon_dia_id" not in st.session_state or st.session_state.pokemon_dia_id is None:
        st.session_state.pokemon_dia_id = random.randint(1, 151)

    return client.get_pokemon(st.session_state.pokemon_dia_id) 


def get_random_pokemons_id(total = 6):
    random_ids = random.sample(range(1,152), total)

    return random_ids

def render_random_pokemons(client, random_id):

    st.divider()
    st.subheader('🌟 Explora Pokemons aleatorios')
    st.info('✨ Descubre Pokemons aleatorios o usa la barra de busqueda para encontrar el que quieras')
    
    random_id = get_random_pokemons_id()
        

    cols = st.columns(3)

    for index, pokemon_id in enumerate(random_id):
                        
        pokemon = client.get_pokemon(pokemon_id)

        with cols[index % 3]:
            st.image(pokemon.get('sprite_url', ''), width=180)

            st.markdown(f'### {pokemon.get("id")} {pokemon.get("name", "").capitalize()}')

            if st.button('Ver Detalle', key=f'random{pokemon_id}'):
                st.session_state.pokemon_seleccionado = pokemon.get('name')
                st.rerun() 
