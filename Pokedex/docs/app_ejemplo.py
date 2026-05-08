"""
Ejemplo minimo de una app Streamlit que consulta la PokeAPI.

Ejecutar con:
    streamlit run app_ejemplo.py

Este es solo un ejemplo. Tu tarea es construir el PokeDex completo.
"""

import streamlit as st
import plotly.graph_objects as go

from backend.app.clients.pokeapi_client import PokeAPIClient
from AB_Programming_Coding.Pokedex.docs.models import parse_pokemon


# Inicializar el cliente de API (se reutiliza entre recargas gracias a st.cache_resource)
@st.cache_resource
def get_client():
    return get_client


def crear_grafico_stats(stats: dict) -> go.Figure:
    """Crea un grafico de barras horizontales con las estadisticas del Pokemon."""
    # Nombres mas legibles para las estadisticas
    nombres = {
        "hp": "HP",
        "attack": "Ataque",
        "defense": "Defensa",
        "sp_attack": "At. Especial",
        "sp_defense": "Def. Especial",
        "speed": "Velocidad",
    }

    # Colores por estadistica
    colores = {
        "hp": "#FF5959",
        "attack": "#F5AC78",
        "defense": "#FAE078",
        "sp_attack": "#9DB7F5",
        "sp_defense": "#A7DB8D",
        "speed": "#FA92B2",
    }

    # Ordenar las stats en el orden clasico de los juegos
    orden = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
    labels = [nombres.get(s, s) for s in orden]
    values = [stats.get(s, 0) for s in orden]
    colors = [colores.get(s, "#888") for s in orden]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=values,
        textposition="auto",
    ))

    fig.update_layout(
        title="Estadisticas Base",
        xaxis_title="Valor",
        xaxis_range=[0, 260],
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
    )

    return fig


def main():
    st.set_page_config(page_title="PokeDex - Ejemplo", page_icon="🔴")

    st.title("PokeDex - Ejemplo Basico")
    st.caption("Este es solo un ejemplo. Tu tarea es construir el PokeDex completo.")

    client = get_client()

    # --- Buscador simple ---
    nombre = st.text_input(
        "Nombre del Pokemon",
        placeholder="ej: pikachu, charizard, mewtwo",
    )

    if st.button("Buscar", type="primary") and nombre:
        with st.spinner("Consultando PokeAPI..."):
            try:
                # Obtener datos crudos de la API
                data = client.get_pokemon(nombre)
                # Convertir a nuestro modelo limpio
                pokemon = parse_pokemon(data)

                # --- Mostrar resultados ---
                col1, col2 = st.columns([1, 2])

                with col1:
                    if pokemon.sprite_url:
                        st.image(pokemon.sprite_url, width=200)
                    st.markdown(f"**#{pokemon.id}** — {pokemon.name.capitalize()}")

                    # Mostrar tipos con colores
                    tipos_texto = " / ".join(t.capitalize() for t in pokemon.types)
                    st.markdown(f"**Tipos:** {tipos_texto}")

                    # Datos fisicos
                    st.markdown(f"**Altura:** {pokemon.height / 10:.1f} m")
                    st.markdown(f"**Peso:** {pokemon.weight / 10:.1f} kg")
                    st.markdown(f"**Exp. base:** {pokemon.base_experience}")

                    # Habilidades
                    habilidades = ", ".join(a.replace("-", " ").capitalize() for a in pokemon.abilities)
                    st.markdown(f"**Habilidades:** {habilidades}")

                with col2:
                    # Grafico de estadisticas
                    fig = crear_grafico_stats(pokemon.stats)
                    st.plotly_chart(fig, use_container_width=True)

            except ValueError as e:
                st.error(f"No se encontro el Pokemon: {e}")
            except ConnectionError as e:
                st.error(f"Error de conexion: {e}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")

    # --- Informacion del cache ---
    with st.sidebar:
        st.header("Cache")
        stats = client.cache.stats()
        st.metric("Aciertos", stats["hits"])
        st.metric("Fallos", stats["misses"])
        st.metric("Tasa de acierto", f"{stats['hit_rate']:.1%}")
        st.metric("Entradas validas", stats["valid_entries"])

        if st.button("Limpiar cache"):
            client.cache.clear()
            st.success("Cache limpiado")
            st.rerun()


if __name__ == "__main__":
    main()
