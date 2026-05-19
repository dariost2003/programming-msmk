from __future__ import annotations

import streamlit as st
import random

from api.backend_client import BackendClient
from components.radar_chart import render_radial_chart
from components.pokemon_card import render_pokemon_card
from components.combat_effectiveness import render_combat_effectiveness
from components.evolution_chain import render_evo_chain
from utils.constants import COLORS_TYPE_POKEMON
from utils.colors import hexadecimal_to_rgba
from utils.pokemon_logic import get_pokemon_of_the_day, get_random_pokemons_id

def render_pokemon_detail(client: BackendClient, identifier: str) -> None:
    
    st.title('🔍 Buscar Pokemon')
    st.caption('Explora al detalle un Pokemon')
    st.markdown('---')
    st.subheader('⭐ Pokemon del momento')

    featured_pokemon = None


    try:
        
        featured_pokemon = get_pokemon_of_the_day(client)
    
        if featured_pokemon:
            name = featured_pokemon.get('name')
            if not name:
                raise ValueError('Pokemon del momento sin nombre')
            
            if name:
                species = client.get_flavor_text(name)

                flavor_text = species.get('flavor_text', 'Descripción no disponible')

                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image(featured_pokemon.get('sprite_url', ''), width=280)

                with col2:

                    pokemon_name = featured_pokemon.get("name", "")
                    
                    pokemon_id = featured_pokemon.get('id', 0)

                    st.markdown(f'### {pokemon_name}')
                    st.caption(f'#{pokemon_id:03}')

                    types = featured_pokemon.get('types', [])
                    type_cols = st.columns(len(types))

                    for index, pokemon_type in enumerate(types):
                        color = COLORS_TYPE_POKEMON.get(pokemon_type, '#888888')

                        type_cols[index].markdown(
                            f"""
                            <div style="
                                background-color:{color};
                                color:white;
                                padding:6px;
                                border-radius:10px;
                                text-align:center;
                                font-weight:bold;
                                margin-bottom:10px;
                            ">
                                {pokemon_type.capitalize()}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(f""">*{flavor_text}*""")
                    st.write('Busca este Pokemon para explorar sus estadísticas, evoluciones y habilidades')

    except Exception as e:
        
        st.warning(f'No se pudo cargar el Pokemon del día: {e}')            
       
    with st.spinner('Consultando datos...'):
        try:
            pokemon = client.get_pokemon(identifier)
            evolution_data = client.get_evolution(identifier)
            effectiveness_data = client.get_effectiveness(identifier)
            species = client.get_flavor_text(identifier)
            flavor_text = species.get('flavor_text', 'Descripcion no disponible')
            types = pokemon.get('types', [])
            primary_type = types[0] if types else 'normal'
            base_color = COLORS_TYPE_POKEMON.get(primary_type, '#333333')
            url_shiny = pokemon.get('sprite_shiny') or pokemon.get('sprite_url', '')

            # Fondo temático
            rgba_fuerte = hexadecimal_to_rgba(base_color, 0.15)
            rgba_debil = hexadecimal_to_rgba(base_color, 0.05)
            css = f"""
            <style>
                .stApp {{
                    background: radial-gradient(circle at top right, {rgba_fuerte}, transparent),
                                radial-gradient(circle at bottom left, {rgba_debil}, transparent);
                    background-attachment: fixed;
                }}
            </style>
            """
            st.markdown(css, unsafe_allow_html=True)

            st.title(f"◓ #{pokemon.get('id', 0)} - {pokemon.get('name', '').capitalize()}")
            st.caption('Explora estadísticas, evoluciones y efectividad de combate')

            col1, col2, col3 = st.columns([1.8, 3.0, 1.5], gap='medium')
            with col1:
                st.image(pokemon.get('sprite_url', ''), width=300)
                st.markdown(f"> *{flavor_text}*")
                st.write('**Tipos**')

                type_cols = st.columns(len(types)) if types else []
                for index, pokemon_type in enumerate(types):
                    color = COLORS_TYPE_POKEMON.get(pokemon_type, '#888')
                    type_cols[index].markdown(
                        f"""
                        <p style="
                            background-color:{color};
                            color:white; 
                            padding:5px; 
                            border-radius:10px; 
                            text-align:center; 
                            font-weight:bold;
                        ">
                            {pokemon_type.capitalize()}
                        </p>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown(f'**Altura:** {pokemon.get("height", 0) / 10} m | **Peso:** {pokemon.get("weight", 0) / 10} kg')
                st.markdown(f'**Exp. Base:** {pokemon.get("base_experience", 0)}')

                abilities = pokemon.get('abilities', [])
                formatted_abilities = ', '.join(
                    ability.replace('-', ' ').capitalize() for ability in abilities
                )
                st.info(f'**Habilidades:** {formatted_abilities}')

            with col2:
                st.subheader('Análisis de Estadísticas')
                fig = render_radial_chart(pokemon)
                st.plotly_chart(fig, use_container_width=True)

            with col3:
                st.subheader('⚔️ Efectividad en Combate')
                render_combat_effectiveness(effectiveness_data)

            st.divider()
            render_evo_chain(evolution_data, client)
            
            st.divider()
            st.subheader('🎴 Carta Coleccionable')
            render_pokemon_card(pokemon=pokemon, hexadecimal_color=base_color, url_sprite=url_shiny)

        except ValueError as e:
            st.error(f'No se encontró el Pokémon: {e}')
        except ConnectionError as e:
            st.error(f'Error de conexión: {e}')
        except Exception as e:
            st.error(f'Error inesperado: {e}')
