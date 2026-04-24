import streamlit as st
import plotly.graph_objects as go


from api_client import PokeAPIClient
from models import parse_pokemon

@st.cache_resource
def get_client():
    return PokeAPIClient()

COLORES_TIPO_POKEMON = {
    'fire':'#ff421c','water':'#2c9be3',
    'grass':'#78cc55', 'electric':'#ffd333',
    'ice':'#7ac7ff', 'fighting':'#bb5544', 
    'poison':'#aa5599', 'ground':'#ddbb55',
    'flying':'#8899ff','psychic':'#ff5599',
    'bug':'#aabb22', 'rock':'#bbaa66',
    'ghost':'#6666bb', 'dragon':'#7766ee',
    'dark':'#775544', 'steel':'#aaaabb',
    'fairy':'#ee99ee', 'normal':'#aaaa99'
}

def generador_grafico_radial(pokemon):
    stats_map = {s['stat']['name']:s['base_stat'] for s in pokemon['stats']}

    tipo_pokemon = pokemon.types[0].lower()
    colores_hexadecimales = COLORES_TIPO_POKEMON.get(tipo_pokemon, '#333333')
    
    nombres = {
        'hp': 'puntos de vida',
        'attack':'ataque',
        'defense':'defensa',
        'sp-attack':'ataque especial',
        'sp-defense':'defensa especial',
        'speed':'velocidad'
    }
    
    orden = ['hp','attack','defense','sp-attack','sp-defense','speed']
    labels = [nombres.get(s, s) for s in orden]
    values = [stats_map.get(s, 0) for s in orden]
    

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta= labels + [labels[0]],
        fill='toself',
        fillcolor=f'rgba{tuple(int(colores_hexadecimales.lstrip("#")[i:i+2],16) for i in (0, 2, 4))+ (0.5,)}',
        line=dict(color=colores_hexadecimales, width=3),
        name=pokemon.name.capitalize()
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,250], gridcolor= '#eee'),
            angularaxis=dict(gridcolor='#eee')
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bdcolor='rbga(0,0,0,0)',
        title=dict(text=f'Perfil de {pokemon.name.capitalize()}', front=dict(color=colores_hexadecimales))
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

if __name__ == '__main__':
    main()



