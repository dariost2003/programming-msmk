import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from api_client import PokeAPIClient
from models import parse_pokemon

@st.cache_resource
def get_client():
    return PokeAPIClient()

def generador_grafico_radial(pokemon_data):
    stats_map = {s['stat']['name']:s['base_stat'] for s in pokemon_data['stats']}

    categories = ['hp','attack','defense','sp_attack','sp_defense','speed']
    
    nombres = {
        'hp': 'puntos de vida',
        'attack':'ataque',
        'defense':'defensa',
        'sp_attack':'ataque especial',
        'sp_defense':'defensa especial',
        'speed':'velocidad'
    }
    colores = {
        'hp': '#B5FFB6',
        'attack':'#FFB5B5',
        'defense':'#9EA3FF',
        'sp_attack':'#FF4F4F',
        'sp_defense':'#5777FA',
        'speed': '#F3FF85'
    }

    orden = ['hp','attack','defense','sp_attack','sp_defense','speed']
    labels = [nombres.get(s, s) for s in orden]
    values = [stats.get(s, 0) for s in orden]
    colors = [colores.get(s, '#888') for s in orden]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=nombres + [nombres[0]],
        fill='toself',
        name=pokemon_data['name'].capitalize(),
        line_color='#000000'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range[0,255])
        ),
        showlegend=False,
        tittle=f'Stats de {pokemon_data['name'].upper()}'
    )
    return fig

def main():
    st.set_page_config(page_title='PokeDex', page_icon='◓')

    st.title('PokeDex')
    st.caption('Busca tu pokemon favorito, aprende stats, forma equipos, compara pokemones')

    client = get_client()

    nombre = st.text_input(
        'Nombre del Pokemon',
        placeholder='ej: pikachu, charmander, bulbasour'
    )

    if st.button('Buscar', type='primary') and nombre:
        with st.spinner('Consultando PokeAPI...'):
            try:
                data= client.get_pokemon(nombre)
                pokemon = parse_pokemon(data)

                col1, col2 = st.columns([1,2])

                with col1:
                    if pokemon.sprite_url:
                        st.image(pokemon.sprite_url, width=300)
                    st.markdown(f'**#{pokemon.id}**-{pokemon.name.capitalize()}')

                    tipos_texto = '/'.join(t.capitalize() for t in pokemon.types)
                    st.markdown(f'**Tipos**{tipos_texto}')

                    st.markdown(f'**Altura:**{pokemon.height/10:.1f} m')
                    st.markdown(f'**Peso**{pokemon.weight / 10:.1f} m')
                    st.markdown(f'**Exp. Base**{pokemon.base_experience}') 

                    habilidades = ','.join(a.replace('-','').capitalize() for a in pokemon.abilities)
                    st.markdown(f'**Habilidades**:{habilidades}')

                with col2:
                    fig = generador_grafico_radial(pokemon.stats)
                    st.plotly_chart(fig, use_container_width=True)

            except ValueError as e:
                st.error(f'No se encontro el Pokemon: {e}')
            except ConnectionError as e:
                st.error(f'Error de conexion: {e}')
            except Exception as e:
                st.error(f'Error inesperado: {e}')

    with st.sidebar:
        st.header('Pokemones encontrados')
        stats = client.cache.stats()
        st.metric('Encontrados', stats['hits'])
        st.metric('No encontrados', stats['misses'])
        st.metric('Tasa de aciertos', f'{stats['hit_rate']:.1%}') 
        st.metric('Entradas validas', stats['valid_entries']) 

        if st.button('Limpiar cache'):
            client.cache.clear()
            st.success('Cache limpiado')
            st.rerun()

if __name__ == 'main':
    main()



