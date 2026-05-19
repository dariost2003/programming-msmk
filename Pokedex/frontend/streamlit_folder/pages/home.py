import streamlit as st

from api.backend_client import BackendClient
from pages.pokemon_detail import render_pokemon_detail
from utils.constants import COLORS_TYPE_POKEMON
from utils.colors import hexadecimal_to_rgba

client = BackendClient()


def render_home() -> None:
    st.set_page_config(page_title='PokeDex', page_icon='◓', layout='wide')
    st.title('◓ PokeDex')
    st.caption('Busca tu pokémon favorito, aprende stats, forma equipos, compara pokémons')

    if 'pokemon_seleccionado' not in st.session_state:
        st.session_state.pokemon_seleccionado = None

    search_value = st.text_input('Buscar Pokémon', key='search_input').strip().lower()
    search_clicked = st.button('Buscar', type='primary')

    if search_clicked and search_value:
        st.session_state.pokemon_seleccionado = search_value

    if st.session_state.pokemon_seleccionado:
        if st.button('Volver a galería'):
            st.session_state.pokemon_seleccionado = None
            st.rerun()
        render_pokemon_detail(client, st.session_state.pokemon_seleccionado)
        return

    with st.sidebar:
        st.header('🔍 Filtros Avanzados')
        tipo = st.multiselect('Tipo', list(COLORS_TYPE_POKEMON.keys()))

        generaciones = {
            'Todas': None,
            '1ra Gen (Kanto)': (1, 151),
            '2da Gen (Johto)': (152, 251),
            '3ra Gen (Hoenn)': (252, 386),
            '4ta Gen (Sinnoh)': (387, 493),
            '5ta Gen (Unova)': (494, 649)
        }

        generacion_seleccionada = st.selectbox('Generación', list(generaciones.keys()))
        rango_id = generaciones[generacion_seleccionada]

        ataque_minimo = st.slider('Ataque mínimo', 0, 200, 0)
        hp_minimo = st.slider('HP mínimo', 0, 200, 0)
        defensa_minima = st.slider('Defensa mínima', 0, 200, 0)
        velocidad_minima = st.slider('Velocidad mínima', 0, 200, 0)
        min_base_exp = st.slider('Exp. Base mínima', 0, 200, 0)

    min_id, max_id = (rango_id if rango_id is not None else (0, 0))

    filters = {
        'pokemon_type': tipo[0] if len(tipo) == 1 else None,
        'min_id': min_id,
        'max_id': max_id,
        'min_attack': ataque_minimo,
        'min_hp': hp_minimo,
        'min_defense': defensa_minima,
        'min_base_exp': min_base_exp
    }

    try:
        data = client.filter_pokemons(**filters)
    except RuntimeError as error:
        st.error(str(error))
        return

    if len(tipo) > 1:
        data = [
            pokemon for pokemon in data
            if any(selected_type in pokemon.get('types', []) for selected_type in tipo)
        ]

    if not data:
        st.warning('No se encontró ningún Pokémon con esos filtros.')
        return

    st.subheader('🎴 Galería de Resultados')
    columns = st.columns(5)

    for index, pokemon in enumerate(data[:150]):
        column = columns[index % len(columns)]
        with column:
            sprite = pokemon.get('sprite', '')
            column.image(sprite, caption=f"#{pokemon.get('id', 0)} {pokemon.get('name', '').capitalize()}")
            if column.button('Ver Detalle', key=f"pokemon_{pokemon.get('id', index)}" , use_container_width=True):
                st.session_state.pokemon_seleccionado = pokemon.get('name', '').lower()
                st.rerun()

   