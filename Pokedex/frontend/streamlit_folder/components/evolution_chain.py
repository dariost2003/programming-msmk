import streamlit as st
import streamlit.components.v1 as components
from utils.constants import COLORS_TYPE_POKEMON


def render_evo_chain(evolution_data: dict[str, object], client) -> None:
    st.subheader('🧬 Cadena Evolutiva')

    if not evolution_data:
        st.info('No hay datos de cadena evolutiva disponibles')
        return

    def extract_evolution_names(node: dict, nombres: set) -> None:
        nombres.add(node.get('name', ''))
        for child in node.get('children', []):
            extract_evolution_names(child, nombres)

    nombres = set()
    extract_evolution_names(evolution_data, nombres)
    nombres.discard('')

    if not nombres:
        st.info('No hay evoluciones registradas')
        return

    def flatten_chain(node, result=None):
        if result is None:
            result = []

        result.append(node)

        children = node.get('children', [])
        if children:
            flatten_chain(children[0], result)

        return result 

    chain = flatten_chain(evolution_data)

   
    

    html = """
    <div style="display:flex;
                  align-items:center;
                  justify-content:center;
                  flex-wrap:wrap;
                  gap:20px;
                  margin-top:20px;
                  margin-bottom:0px;
    ">
    """

    for i, evo in enumerate(chain):

        name = evo.get('name', '').capitalize()

        try: 
            p_data = client.get_pokemon(name.lower())
            sprite = p_data.get('sprite_url', "")

        except Exception:
            
            
            sprite = ""

        html += f"""
        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            background:#1f2937;
            padding:18px;
            border-radius:18px;
            min-width:140px;
            box-shadow:0 4px 12px rgba(0,0,0,0.3);
        ">

            <img
                src="{sprite}"
                width="110"
                style="
                    image-rendering:auto;
                    margin-bottom:10px;
                "
            >

            <div style="
                color:white;
                font-weight:bold;
                font-size:18px;
            ">

                {name}
            </div>
        </div>
        """

        if i < len(chain) -1:
            next_evo = chain[i + 1]
            details = next_evo.get('evolution_details', {})

            requisito = 'Evoluciona'

    
            if details.get('min_level'):
                requisito = f"⬆️ Nivel {details['min_level']}"
            elif details.get('min_happiness'):
                requisito = f"❤️ Felicidad {details['min_happiness']}"
            elif details.get('item'):
                item_name = details['item'].get('name', 'Objeto') if isinstance(details['item'], dict) else details['item']
                requisito = f"🪨 {item_name}"
            elif details.get('trigger'):
                trigger_name = details['trigger'].get('name', 'Activador') if isinstance(details['trigger'], dict) else details['trigger']
                requisito = f"⚡ {trigger_name}"
            elif details.get('time_of_day'):
                requisito = f"🌙 {details['time_of_day'].capitalize()}"
            
            html += f"""
            <div style="
                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
                color:white;
            ">

                <div style="
                    font-size:40px;
                    margin-bottom:8px;
                ">

                </div>

                <div style="
                    background:#2563eb;
                    padding:8px 14px;
                    border-radius:999px;
                    font-size:14px;
                    font-weight:bold;
                    white-space:nowrap;
                ">

                    {requisito}
                
                </div>
            </div>
            """
                
    html += "</div>"

    components.html(html, height=200)  

    st.markdown('### Seleccionar evolucion')

    cols = st.columns(len(nombres))

    for idx, name in enumerate(sorted(nombres)):

        with cols[idx]:
            try:
                p_data = client.get_pokemon(name)

                sprite = p_data.get("sprite_url", "")

                if sprite:

                    left, center, right=st.columns([1, 2, 1])

                    with center:
                        st.image(sprite, width=100) 

                st.markdown(
                    f"""
                    <p style="
                        text-align:center;
                        font-weight:bold;
                        margin-top:-10px;
                    ">
                        {name.capitalize()}
                    </p>
                    """,
                    unsafe_allow_html=True
                    ) 

                if st.button(
                    f'Ver {name.capitalize()}',
                    key=f'evo_{name}',
                    use_container_width=True
                ):
                    st.session_state.pokemon_seleccionado=name.lower()
                    st.rerun()

            except Exception:
                st.markdown(
                    f"""
                    <p style="text-align:center;">
                        {name.capitalize()}
                    </p>
                    """,
                    unsafe_allow_html=True
                )


    