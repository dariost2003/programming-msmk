import streamlit as st

st.set_page_config(page_title='Pokedex', page_icon='◓', layout='wide')

st.title('◓ Pokedex')

st.caption('Explora la Pokedex interactiva, busca estadisticas, evoluciones y caracteristicas más especiales de tus Pokemon favoritos')

st.markdown('---')

col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown(
        """
        ## Bienvenido a tu Pokedex Interactiva

        En esta aplicación podrás:

        - 🔍 Buscar el Pokemon que desees.
        - 🎴 Explora galerias Pokemon.
        - 📊 Analiza las estadisticas de tu Pokemon a traves de graficos.
        - ⚔️ Mira las estadisticas de combate.
        - 🧬 Encuentra su cadena evolutiva y requisitos.
        - ✨ Visualiza las versiones Shiny en una carta estilo coleccionable.

        """
    )

with col2:
    st.image(
        'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png',
        width=350
    )

st.markdown('---')

st.info('Selecciona una página en la barra lateral para comenzar a explorar')