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

def hexadecimal_a_rgba(colores_hexadecimales, alpha):
    hex_color = colores_hexadecimales.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2],16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'

def fondo_de_pantalla(colores_hexadecimales):
    rgba_colorfuerte = hexadecimal_a_rgba(colores_hexadecimales, 0.15)
    rgba_colordebil = hexadecimal_a_rgba(colores_hexadecimales, 0.05)

    css = f'''
       <style>
           .stApp {{
               background: radial-gradient(circle at top right, {rgba_colorfuerte}, transparent),
                           radial-gradient(circle at bottom left, {rgba_colordebil}, transparent);
               background-attachment: fixed;
           }}
           [data-testid="stMetric"] {{
               background-color: rgba(255, 255, 255, 0.05);
               padding: 15px;
               border-radius: 15px;
               border: 1px solid {hexadecimal_a_rgba(colores_hexadecimales, 0.2)};
               backdrop-filter: blur(5px)
           }}
    <style>
    '''
    st.markdown(css, unsafe_allow_html=True)

def generador_grafico_radial(pokemon):
    
    color_principal = COLORES_TIPO_POKEMON.get(pokemon.types[0], '#fb1b1b')
    if len(pokemon.types) > 1:
        color_secundario = COLORES_TIPO_POKEMON.get(pokemon.types[1], color_principal)
    else:
        color_secundario = color_principal

    nombres = {
        'hp': 'puntos de vida',
        'attack':'ataque',
        'defense':'defensa',
        'sp_attack':'ataque sp',
        'sp_defense':'defensa sp',
        'speed':'velocidad'
    }
    
    orden = ['hp','attack','defense','sp_attack','sp_defense','speed']
    labels = [nombres.get(s, s) for s in orden]
    values = [pokemon.stats.get(s, 0) for s in orden]
    

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta= labels + [labels[0]],
        fill='toself',
        fillcolor= hexadecimal_a_rgba(color_secundario, 0.4),
        line=dict(color=color_principal, width=4),
        name=pokemon.name.capitalize()
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,160], gridcolor = 'rgba(0, 0, 0, 0.1)'),
            angularaxis = dict(gridcolor = 'rgba(0, 0, 0, 0.1)')
        ),
        showlegend=False,
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        margin = dict(t=30, b=30, l=40, r=40)
    ) 
    return fig

def main():
    st.set_page_config(page_title='PokeDex', page_icon='◓', layout='wide')

    st.title('◓ PokeDex')
    st.caption('Busca tu pokemon favorito, aprende stats, forma equipos, compara pokemones')

    client = get_client()

    nombre = st.text_input(
        'Nombre del Pokemon',
        placeholder='ej: pikachu, charmander, bulbasour'
    ).lower().strip()

    if st.button('Buscar', type='primary') and nombre:
        with st.spinner('Consultando datos...'):
            try:
                data= client.get_pokemon(nombre)
                pokemon = parse_pokemon(data)
                color_tema= COLORES_TIPO_POKEMON.get(pokemon.types[0], '#FF0000')
                fondo_de_pantalla(color_tema)

                col1, col2 = st.columns([1,2], gap='large')

                with col1:
                    if pokemon.sprite_url:
                        st.image(pokemon.sprite_url, width=300)
                    st.header(f'**#{pokemon.id}** - {pokemon.name.capitalize()}')

                    st.write('**Tipos**')
                    cols_tipos = st.columns(len(pokemon.types))
                    for i, t in enumerate(pokemon.types):
                        c = COLORES_TIPO_POKEMON.get(t, '#888')
                        cols_tipos[i].markdown(f'<p style="background-color:{c}; color:white; padding:5px; border-radius:10px; text-align:center;">{t.capitalize()}</p>', unsafe_allow_html=True)

                    st.markdown(f'**Altura:** {pokemon.height/10} m | **Peso:** {pokemon.weight/10} kg')
                    st.markdown(f'**Exp. Base:** {pokemon.base_experience}') 

                    habilidades = ','.join(a.replace('-','').capitalize() for a in pokemon.abilities)
                    st.info(f'**Habilidades:** {habilidades}')

                with col2:
                    st.subheader("Análisis de Estadisticas")
                    fig = generador_grafico_radial(pokemon)
                    st.plotly_chart(fig, use_container_width=True)

            except ValueError as e:
                st.error(f'No se encontro el Pokemon: {e}')
            except ConnectionError as e:
                st.error(f'Error de conexion: {e}')
            except Exception as e:
                st.error(f'Error inesperado: {e}')

    with st.sidebar:
        st.header('Estado del sistema')
        c_stats = client.cache.stats()
        st.metric('Encontrados', c_stats['hits'])
        st.metric('No encontrados', c_stats['misses'])
        st.metric('Tasa de aciertos', f'{c_stats["hit_rate"]:.1%}') 
        st.metric('Entradas validas', c_stats['valid_entries']) 

        if st.button('Limpiar memoria cache'):
            client.cache.clear()
            st.success('Cache limpiado')
            st.rerun()


if __name__ == '__main__':
    main()



