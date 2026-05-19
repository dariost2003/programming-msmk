import streamlit as st
from utils.colors import hexadecimal_to_rgba
from utils.constants import COLORS_TYPE_POKEMON

# Renderiza los cuadros de tipo con multiplicadores de daño
def render_type_badges(title: str, list: list[tuple[str, float]], icon: str) -> None:
    
    if not list:
        return
    
    st.markdown(f'###{icon} {title}')

    sorted_list = sorted(list, key=lambda x: x[0])

    html = ""
    for tipo, mult in list:
        color = COLORS_TYPE_POKEMON.get(tipo, '#888')
        label = tipo.upper()
        
        tooltip = f'Recibe x{mult} de daño'

        html += f"""
        <span title="{mult}" style='
            background-color: {color};
            color: white;
            padding: 6px 10px;
            border-radius: 12px;
            margin: 4px;
            display: inline-block;
            font-weight: 0.85em;
            font-size: 0.85em;
        '>
            {label}
        </span>
        """
        
    st.markdown(html, unsafe_allow_html=True)