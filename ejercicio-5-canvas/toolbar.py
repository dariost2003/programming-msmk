"""
toolbar.py - Barra de herramientas lateral del canvas.

Contiene los botones de herramientas (seleccionar, dibujar, figuras, etc.),
la paleta de colores y el control de grosor de trazo.
"""

from nicegui import ui
from elements import COLORES


def create_toolbar(manager, on_tool_change, on_color_change):
    """
    Crea la barra de herramientas lateral.

    Args:
        manager: Instancia de CanvasManager para leer/modificar estado.
        on_tool_change: Callback que recibe el nombre de la herramienta seleccionada.
        on_color_change: Callback que recibe el color hexadecimal seleccionado.
    """
    with ui.column().classes('gap-2 p-3').style(
        'width: 200px; min-width: 200px; border-right: 1px solid #ddd; '
        'background: #f8f9fa; height: 100vh; overflow-y: auto;'
    ):
        ui.label('Herramientas').classes('text-lg font-bold')

        # --- Botones de herramientas ---
        tools = [
            ("select", "arrow_selector_tool", "Seleccionar"),
            ("freedraw", "edit", "Dibujo libre"),
            ("rect", "crop_square", "Rectangulo"),
            ("circle", "circle", "Circulo"),
            ("arrow", "trending_flat", "Flecha"),
            ("text", "title", "Texto"),
        ]

        for tool_id, icon, label in tools:
            btn = ui.button(label, icon=icon, on_click=lambda t=tool_id: on_tool_change(t))
            btn.classes('w-full justify-start')
            # TODO: Resaltar el boton de la herramienta activa
            # Pista: usar btn.props('color=primary') cuando tool_id == manager.current_tool

        ui.separator()

        # --- Paleta de colores ---
        ui.label('Colores').classes('text-md font-bold')
        with ui.row().classes('gap-1 flex-wrap'):
            for nombre, hex_color in COLORES.items():
                ui.button(
                    '',
                    on_click=lambda c=hex_color: on_color_change(c),
                ).style(
                    f'background-color: {hex_color} !important; '
                    f'min-width: 32px; height: 32px; border-radius: 4px; padding: 0;'
                )

        ui.separator()

        # --- Control de grosor ---
        ui.label('Grosor').classes('text-md font-bold')
        stroke_slider = ui.slider(min=1, max=10, value=2, step=1)
        stroke_slider.on(
            'update:model-value',
            lambda e: setattr(manager, 'stroke_width', int(e.args)),
        )

        ui.separator()

        # --- Cuadricula ---
        ui.label('Cuadricula').classes('text-md font-bold')
        ui.switch('Mostrar', value=True, on_change=lambda e: setattr(manager, 'grid_visible', e.value))

        ui.separator()

        # --- Widgets interactivos (Tarea 5) ---
        ui.label('Widgets').classes('text-md font-bold text-grey')
        ui.label('TODO: Agregar herramientas\nde widgets (Tarea 5)').classes('text-xs text-grey')
        # TODO: Los estudiantes deben agregar botones para:
        # - widget_button: Colocar un boton interactivo en el canvas
        # - widget_slider: Colocar un slider interactivo en el canvas
        # - widget_input: Colocar un campo de texto interactivo en el canvas
        # Ejemplo:
        # ui.button('Boton', icon='smart_button',
        #           on_click=lambda: on_tool_change('widget_button')).classes('w-full justify-start')
