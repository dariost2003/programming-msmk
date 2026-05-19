import streamlit as st
import plotly.graph_objects as go
from utils.colors import hexadecimal_to_rgba
from utils.constants import COLORS_TYPE_POKEMON

def render_radial_chart(pokemon: dict):

    stats = pokemon.get('stats', {})
    types = pokemon.get('types', [])
    name = pokemon.get('name', 'pokemon').capitalize()

    primary_color = COLORS_TYPE_POKEMON.get(types[0], '#fb1b1b') if types else '#fb1b1b'   
    secondary_color = COLORS_TYPE_POKEMON.get(types[1], primary_color) if len(types) > 1 else primary_color

    stats_map = {
        'hp': 'HP',
        'attack':'Ataque',
        'defense':'Defensa',
        'sp_attack':'Ataque sp',
        'sp_defense':'Defensa sp',
        'speed':'Velocidad'
    }
    
    orden = ['hp','attack','defense','sp_attack','sp_defense','speed']
    labels = [stats_map[s] for s in orden]
    values = [stats.get(s, 0) for s in orden]
    

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta= labels + [labels[0]],
        fill='toself',
        fillcolor= hexadecimal_to_rgba(secondary_color, 0.4),
        line=dict(color=primary_color, width=4),
        name=name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0,185], gridcolor = 'rgba(0, 0, 0, 0.1)'),
            angularaxis = dict(gridcolor = 'rgba(0, 0, 0, 0.1)')
        ),
        showlegend=False,
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        margin = dict(t=30, b=30, l=40, r=40)
    ) 
    return fig