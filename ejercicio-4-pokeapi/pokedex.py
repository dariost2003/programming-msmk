import streamlit as st
import plotly.graph_objects as go
import json


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
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

def generador_grafico_radial(pokemon):
    
    color_principal = COLORES_TIPO_POKEMON.get(pokemon.types[0], '#fb1b1b')
    if len(pokemon.types) > 1:
        color_secundario = COLORES_TIPO_POKEMON.get(pokemon.types[1], color_principal)
    else:
        color_secundario = color_principal

    nombres = {
        'hp': 'HP',
        'attack':'Ataque',
        'defense':'Defensa',
        'sp_attack':'Ataque sp',
        'sp_defense':'Defensa sp',
        'speed':'Velocidad'
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

def carta_pokemon(pokemon, colores_hexadecimales, url_sprite):
    if len(pokemon.types) >1:
        color_contraste_fondo = COLORES_TIPO_POKEMON.get(pokemon.types[1], colores_hexadecimales)
    else:
        color_contraste_fondo = '#333333'
    
    rgba_brillo = hexadecimal_a_rgba(colores_hexadecimales, 0.4)
    rgba_fondo = hexadecimal_a_rgba(colores_hexadecimales, 0.2)

    carta_html = f"""
<style>
    .card-canvas {{
        width: 340px;
        height: 480px;
        background: {hexadecimal_a_rgba(colores_hexadecimales, 0.6)};
        border-radius: 18px;
        padding: 12px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        border: 4px solid #e0c068;
        margin: auto;
    }}   
    .card-background-pattern {{
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 30%, {rgba_brillo}, transparent 70%),
                    repeating-conic-gradient(from 0deg, rgba(255, 255, 255, 0.1) 0deg 20deg, transparent 20deg 40deg);
        z-index: 1;
    }}
    .card-content {{
        position: relative;
        z-index: 2;
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    .inner-image-box {{
        margin: 5px;
        height: 200px;
        background: {hexadecimal_a_rgba(color_contraste_fondo, 0.5)};
        border: 4px solid rgba(255, 255, 255, 0.3);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 5px;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4)
    }}
    .inner-image-box img {{
        transform: scale(2.9);
        height: 160px;
        width: 210px;
        z-index: 11;
        filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.4));
    }}
    .stats-box {{
        background: rgba(255, 255, 255, 0.9);
        margin: 5px;
        padding: 20px;
        border-radius: 5px;
        flex-grow: 1;
        color: #111;
        font-family: sans-serif;
    }}
</style>
<div class='card-canvas'>
    <div class='card-background-pattern'></div>
    <div class='card-content'>
        <!-- Header -->
        <div style='display: flex; justify-content: space-between; padding: 5px 10px; font-weight: bold; color: white; text-shadow: 1px 1px 3px black; font-family: sans-serif;'>
            <span style='font-size: 1.2em;'>{pokemon.name.upper()}</span>
            <span style='color: #fdeec4; font-size: 1.1em'>HP {pokemon.stats.get('hp', 0)}</span>
        </div>
        <!-- Imagen Shiny -->
        <div class='inner-image-box'>
            <img src='{url_sprite}'>
        </div>
        <!-- Cuerpo de la carta-->
        <div class='stats-container'>
            <p style='font-size: 0.9em; font-weight: bold; margin: 0; color: #666;'>HABILIDADES</p>
            <p style= 'font-size: 1.0em; font-weight: bold; margin-bottom: 12px; color: #111'>
                {', '.join(pokemon.abilities).upper().replace('-', ' ')}
            </p>                                
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 1em; font-family: monospace;'>
                <div><b>ATK:</b> {pokemon.stats.get('attack')}</div>
                <div><b>DEF:</b> {pokemon.stats.get('defense')}</div>
                <div><b>VEL:</b> {pokemon.stats.get('speed')}</div>
                <div><b>EXP:</b> {pokemon.base_experience}</div>
            </div>
        </div>
    </div>
</div>
"""
    st.markdown(carta_html, unsafe_allow_html=True)

@st.cache_data
def cargar_minibiblioteca():
    try:
        with open('datos_basicos_filtro.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return[]
        
def main():

    if 'pokemon_seleccionado' not in st.session_state:
        st.session_state.pokemon_seleccionado = None
    
    st.set_page_config(page_title='PokeDex', page_icon='◓', layout='wide')

    st.title('◓ PokeDex')
    st.caption('Busca tu pokemon favorito, aprende stats, forma equipos, compara pokemones')

    client = get_client()

    nombre = st.text_input(
        'Buscar Pokemon', key='barra de busqueda').lower().strip()
    
    boton_busqueda = st.button('Buscar', type = 'primary')
    
    if boton_busqueda and nombre:
        st.session_state.pokemon_seleccionado = nombre
    if st.session_state.pokemon_seleccionado:
        if st.button('Volver a galeria'):
            st.session_state.pokemon_seleccionado = None
            st.rerun()
            
        with st.spinner('Consultando datos...'):
            try:
                data= client.get_pokemon(st.session_state.pokemon_seleccionado)
                pokemon = parse_pokemon(data)
                url_shiny = data.get('sprites',{}).get('front_shiny') or pokemon.sprite_url
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

                st.divider()
                st.subheader('🎴 Carta coleccionable')
                carta_pokemon(pokemon, color_tema, url_shiny)

               
            except ValueError as e:
                st.error(f'No se encontro el Pokemon: {e}')
            except ConnectionError as e:
                st.error(f'Error de conexion: {e}')
            except Exception as e:
                st.error(f'Error inesperado: {e}')
                if st.button('Limpiar Error'):
                    st.session_state.pokemon_seleccionado = None
                    st.rerun()

    else: 
        st.subheader('Galeria de Resultados')
        
        with st.sidebar:
            st.header('🔍 Filtros Avanzados')
            
            tipo = st.multiselect('Tipo', list(COLORES_TIPO_POKEMON.keys()))

            generaciones = {
            'Todas': (1,1025),
            '1ra Gen (Kanto)': (1, 151),
            '2da Gen (Johto)': (152, 251),
            '3ra Gen (Hoenn)': (252, 386),
            '4ta Gen (Sinnoh)': (387, 493),
            '5ta Gen (Unova)': (494, 649)
            }

            generaciones_seleccionador = st.selectbox('Generacion', list(generaciones.keys()))
            rango_id = generaciones[generaciones_seleccionador]

            ataque_minimo = st.slider('Ataque minimo', 0, 200, 0)
            hp_minimo = st.slider('HP minimo', 0, 200, 0)
            defensa_minima = st.slider('Defensa Minima', 0, 200, 0)
            velocidad_minima = st.slider('Velocidad Minima', 0, 200, 0)
            min_base_exp = st.slider('Min_base_exp', 0, 200, 0)
                
        minibiblioteca = cargar_minibiblioteca()
        if not minibiblioteca:
            st.warning(f"No se encontró el archivo. Por favor ejecuta el script de 'pokemon_filter_seed.py' primero")
            return
            
        datos_filtrados = [
            p for p in minibiblioteca
            if (not tipo or any(t in p['types'] for t in tipo)) and
            (rango_id[0] <= p['id'] <= rango_id[1]) and
            (p['atk'] >= ataque_minimo) and
            (p['hp'] >= hp_minimo) and
            (p['def'] >= defensa_minima) and
            (p['speed'] >= velocidad_minima) and
            (p['base_exp'] >= min_base_exp)
        ]

        if not datos_filtrados:
            st.error(f'No se encuentra un Pokemon que coincida con los filtros.')
        else:
            cols = st.columns(5)
            for i, p in enumerate(datos_filtrados[:50]):
                with cols[i % 5]:
                    st.image(p['sprite'], caption=f"#{p['id']} {p['name'].capitalize()}")
                    if st.button('Ver Detalle', key=f"btn_{p['id']}"):
                        st.session_state.pokemon_seleccionado = p['name']
                        st.rerun()
                    

if __name__ == '__main__':
    main()



