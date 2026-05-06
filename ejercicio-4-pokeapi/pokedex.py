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

TABLA_DE_INTERACCIONES = {
    'normal': {'resist': ['ghost'], 'weak': ['fighting']},
    'fire': {'resist':['fire', 'grass', 'ice', 'bug', 'steel', 'fairy'], 'weak': ['water', 'ground', 'rock']},
    'water': {'resist':['fire', 'water', 'ice', 'steel'], 'weak': ['grass', 'electric']},
    'grass': {'resist': ['water', 'ground', 'electric'], 'weak': ['fire', 'ice', 'poison', 'bug', 'flying']},
    'electric': {'resist': ['electric', 'flying', 'steel'], 'weak': ['ground']},
    'ice': {'resist': ['ice'], 'weak': ['fire', 'fighting', 'rock', 'steel']},
    'fighting': {'resist': ['bug', 'rock', 'dark'], 'weak': ['flying', 'psychic', 'fairy']},
    'poison': {'resist': ['grass', 'fighting', 'poison', 'bug', 'fairy'], 'weak': ['ground', 'psychic']},
    'ground': {'resist': ['poison', 'rock'], 'weak': ['water', 'grass', 'ice'], 'inmune': ['electric']},
    'flying': {'resist': ['grass', 'fighting', 'bug'], 'weak': ['electric', 'ice', 'rock'], 'inmune': ['ground']},
    'psychic': {'resist': ['flying', 'psychic'], 'weak': ['bug', 'ghost', 'dark']},
    'bug': {'resist': ['grass', 'fighting', 'ground'], 'weak': ['fire', 'flying', 'rock']},
    'rock': {'resist': ['normal', 'fire', 'poison', 'flying'], 'weak': ['water', 'grass', 'fighting', 'ground', 'steel']},
    'ghost': {'resist': ['poison', 'bug'], 'weak': ['ghost', 'dark'], 'inmune': ['normal', 'fighting']},
    'dragon': {'resist': ['fire', 'water', 'grass', 'electric'], 'weak': ['ice', 'dragon', 'fairy']},
    'dark': {'resist': ['ghost', 'dark'], 'weak': ['fighting', 'bug', 'fairy'], 'inmune': ['psychic']},
    'steel': {'resist': ['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy'], 'weak': ['fire', 'fighting', 'ground'], 'inmune': ['poison']},
    'fairy': {'resist': ['fighting', 'bug', 'dark'], 'weak': ['poison', 'steel'], 'inmune': ['dragon']}
}

def interacciones(tipos):
    multiplicadores = {t: 1.0 for t in TABLA_DE_INTERACCIONES.keys()}
    for t in tipos:
        data = TABLA_DE_INTERACCIONES.get(t, {})
        for w in data.get('weak', []): multiplicadores[w] *= 2.0 
        for r in data.get('resist', []): multiplicadores[r] *= 0.5
        for i in data.get('inmune', []): multiplicadores[i] *= 0.0
    return multiplicadores

def clasificar_defensas(defensas):
    if not isinstance(defensas, dict):
        raise TypeError('Se esperaba un dict en defensas')
    
    categorias = {
        'muy_debil': [],
        'debil': [],
        'neutral': [],
        'resiste': [],
        'muy_resiste': [],
        'inmune': []
    }
    for tipo, mult in defensas.items():
        if abs(mult - 4.0) < 0.01:
            categorias['muy_debil'].append((tipo, mult))
        elif abs(mult - 2.0) < 0.01:
            categorias['debil'].append((tipo,mult))
        elif abs(mult - 1.0) < 0.01:
            categorias['neutral'].append((tipo,mult))
        elif abs(mult - 0.5) < 0.01:
            categorias['resiste'].append((tipo,mult))
        elif abs(mult - 0.25) < 0.01:
            categorias['muy_resiste'].append((tipo,mult))
        elif abs(mult - 0.0) < 0.01:
            categorias['inmune'].append((tipo,mult))
    
    return categorias
    

def render_categoria(titulo, lista, icono):
    if not lista:
        return
    st.markdown(f'###{icono} {titulo}')

    html = ""
    lista = sorted(lista, key=lambda x: x[0])
    for tipo, mult in lista:
        color = COLORES_TIPO_POKEMON.get(tipo, '#888')
        label = tipo.upper()
        if mult != 1.0:
            label = tipo.upper()

        html += f"""
        <span title="Recibe x {mult} daño" style='
            background-color: {color};
            color: white;
            padding: 6px 10px;
            border-radius: 12px;
            margin: 4px;
            display: inline-block;
            font-weight: normal;
            font-size: 0.85em;
        '>
            {label}
        </span>
        """
        
    st.markdown(html, unsafe_allow_html=True)

def cadena_evolutiva(client, pokemon_name):
    st.subheader('🧬 Cadena Evolutiva')
    try:
        species_data = client.get_species(pokemon_name)
        evolucion_url = species_data['evolution_chain']['url']
        evolucion_data = client.get(evolucion_url)
        chain = evolucion_data['chain']
        
        evoluciones = []
        
        def extraer_nombres(nodo, resultado):
            nombre = nodo['species']['name']

            if not nodo['evolves_to']:
                resultado.append((nombre, "", None))
                return
            
            for evo in nodo['evolves_to']:
                evo_name = evo['species']['name']
                detalles = evo.get('evolution_details', [])

                requisito = ""
                if detalles:
                    d = detalles[0]

                    if d.get('min_level'):
                        requisito = f"⬆️ Nivel {d['min_level']}"
                    elif d.get('min_happiness'):
                        requisito = f"❤️ Felicidad {d['min_happiness']}"
                    elif d.get('friendship'):
                        requisito = f"🤝 Amistad"
                    elif d.get('item'):
                        requisito = f"🪨 {d['item']['name']}"
                    elif d.get('trigger'):
                        requisito = f"⚡ {d['trigger']['name']}"
                    elif d.get('time_of_day'):
                        requisito = f"🌙 {d['time_of_day']}"

                resultado.append((nombre, requisito, evo_name))
                
                extraer_nombres(evo, resultado)
        
        extraer_nombres(chain, evoluciones)
        
        if evoluciones:
            st.markdown('### Evolución')

            html = ""             
            for origen, requisito, destino in evoluciones:
                html += f"""
                <div style= '
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    margin: 8px 0;'>
                    <b>{origen.capitalize()}</b>
                    <span style= '
                        background: #222;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 10px;
                        font-size: 0.8em;'>
                            ➜ {requisito if requisito else "Ultima Evolucion"}
                    </span>
                    <b>{destino.capitalize() if destino else ""}</b>
                </div>
                """
            st.markdown(html, unsafe_allow_html=True)

            nombres = set()
            for o, _, d in evoluciones:
                nombres.add(o)

                if d:
                    nombres.add(d)

                   
        
            cols = st.columns(len(nombres))
            
            for idx, name in enumerate(sorted(nombres)):
                with cols[idx]:
                    p_data = client.get_pokemon(name)
                    sprite = p_data['sprites']['front_default']
                    st.image(sprite, width=100)
                    
                    if st.button(name.capitalize(), key=f'evo_{name}'):
                        st.session_state.pokemon_seleccionado = name
                        st.rerun()
        else:
            st.warning('No hay evoluciones')         

    except Exception as e:
        print(f'Informacion evolutiva no disponible. Error: {e}')

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
                species_data = client.get_species(st.session_state.pokemon_seleccionado)
                url_shiny = data.get('sprites',{}).get('front_shiny') or pokemon.sprite_url
                descripcion_pokemon = next((f['flavor_text'] for f in species_data['flavor_text_entries'] if f['language']['name'] in ['es', 'en']),"")
                descripcion_limpia = descripcion_pokemon.replace('\n', ' ').replace('\f', ' ').replace('\r', ' ')
                color_tema= COLORES_TIPO_POKEMON.get(pokemon.types[0], '#FF0000')
                fondo_de_pantalla(color_tema)

                col1, col2, col3 = st.columns([1.8,3.0,1.5], gap='medium')

                with col1:
                    if pokemon.sprite_url:
                        st.image(pokemon.sprite_url, width=300)
                    st.header(f'**#{pokemon.id}** - {pokemon.name.capitalize()}')
                    st.markdown(f"> *{descripcion_limpia}*")                 
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
                
                with col3:
                    st.subheader('Efectividad en Combate')
                    defensas = interacciones(pokemon.types)
                    categorias = clasificar_defensas(defensas)
                    orden = [
                        ('muy_debil', "🔥 Muy debil"),
                        ('debil',  "⚠️ Débil"),
                        ('resiste', "🛡️ Resiste"),
                        ('muy_resiste', "🧱 Muy resistente"),
                        ('inmune', "🚫 Inmune")
                    ]                      
                    for clave, titulo in orden:
                        render_categoria(titulo, categorias[clave], "")
                                                         

                                              

                   
                                   
                st.divider()                
                cadena_evolutiva(client, pokemon.name)
                

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



