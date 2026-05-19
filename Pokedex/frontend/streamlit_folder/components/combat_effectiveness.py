import streamlit as st
from utils.constants import COLORS_TYPE_POKEMON


def render_combat_effectiveness(effectiveness_data: dict[str, list[tuple[str, float]]]) -> None:
    if not effectiveness_data:
        st.warning('No hay datos disponibles')
        return

    categories = {
        'muy_debil': ('🔥 Muy débil', 'red'),
        'debil': ('⚠️ Débil', 'orange'),
        'resiste': ('🛡️ Resiste', 'blue'),
        'muy_resiste': ('🧱 Muy resistente', 'green'),
        'inmune': ('🚫 Inmune', 'purple')
    }

    for key, (title, _) in categories.items():
        values = effectiveness_data.get(key, [])
        if not values:
            continue

        st.markdown(f'**{title}**')
        html = ""
        for pokemon_type, multiplier in sorted(values, key=lambda x: x[0]):
            color = COLORS_TYPE_POKEMON.get(pokemon_type, '#888')
            html += f"""
            <span title="Recibe x{multiplier} de daño" style='
                background-color: {color};
                color: white;
                padding: 6px 10px;
                border-radius: 12px;
                margin: 4px;
                display: inline-block;
                font-weight: bold;
                font-size: 0.9em;
            '>
                {pokemon_type.capitalize()}
            </span>
            """
        st.markdown(html, unsafe_allow_html=True)

