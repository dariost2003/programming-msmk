import streamlit as st
from utils.colors import hexadecimal_to_rgba
from utils.constants import COLORS_TYPE_POKEMON

# Carta estilo coleccionable Pokemon
def render_pokemon_card(pokemon: dict, hexadecimal_color, url_sprite: str):
    
    name = pokemon.get('name', 'UNKNOWN').upper()
    stats = pokemon.get('stats', {})
    types = pokemon.get('types', [])
    abilities = pokemon.get('abilities', [])

    primary_type = types[0] if len(types) > 0 else 'normal'
    secondary_type = types[1] if len(types) > 1 else None

    base_color = COLORS_TYPE_POKEMON.get(primary_type, '#333333') 
    
    rgba_glow = hexadecimal_to_rgba(base_color, 0.4)
    rgba_bg = hexadecimal_to_rgba(base_color, 0.2)

    carta_html = f"""
<style>
    .card-canvas {{
        width: 340px;
        height: 480px;
        border-radius: 18px;
        padding: 12px;
        background: {hexadecimal_to_rgba(base_color, 0.6)};
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        border: 4px solid #e0c068;
        margin: auto;
    }}   
    .card-background-pattern {{
        position: absolute;
        inset: 0;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 50% 30%, {rgba_glow}, transparent 70%),
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
        background: {rgba_bg};
        border: 4px solid rgba(255, 255, 255, 0.3);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 5px;
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.4)
    }}
    .inner-image-box img {{
        transform: scale(1.5);
        height: 160px;
        width: 210px;
        z-index: 11;
        filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.4));
    }}
    .stats-box {{
        background: rgba(255, 255, 255, 0.9);
        margin-top: 10px;
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
            <span style='font-size: 1.2em;'>{name.upper()}</span>
            <span style='color: #fdeec4; font-size: 1.1em'>HP {stats.get('hp', 0)}</span>
        </div>
        <!-- Imagen Shiny -->
        <div class='inner-image-box'>
            <img src='{url_sprite}'>
        </div>
        <!-- Cuerpo de la carta-->
        <div class='stats-container'>
            <p style='font-size: 0.9em; font-weight: bold; margin: 0; color: #666;'>HABILIDADES</p>
            <p style= 'font-size: 1.0em; font-weight: bold; margin-bottom: 12px; color: #111'>
                {', '.join(abilities).upper().replace('-', ' ')}
            </p>                                
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 1em; font-family: monospace;'>
                <div><b>ATK:</b> {stats.get('attack')}</div>
                <div><b>DEF:</b> {stats.get('defense')}</div>
                <div><b>VEL:</b> {stats.get('speed')}</div>
                <div><b>EXP:</b> {pokemon.get('base_experience', 0)}</div>
            </div>
        </div>
    </div>
</div>
"""
    st.markdown(carta_html, unsafe_allow_html=True)