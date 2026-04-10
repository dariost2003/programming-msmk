"""
app.py - Aplicacion principal del Canvas Interactivo.

Combina el CanvasManager, CanvasView y la Toolbar en una
interfaz completa usando NiceGUI.
"""

from nicegui import ui
from canvas_manager import CanvasManager
from canvas_view import CanvasView
from toolbar import create_toolbar


class CanvasApp:
    """Aplicacion principal del Canvas Interactivo."""

    def __init__(self):
        self.manager = CanvasManager()
        self.canvas_view = CanvasView(self.manager)
        self.status_label = None
        self.coords_label = None
        self.elements_label = None

    def build(self) -> None:
        """Construye la interfaz completa."""
        # Configurar pagina
        ui.page_title('Canvas Interactivo')

        # Layout principal: toolbar izquierda + canvas central
        with ui.row().classes('w-full h-screen no-wrap'):
            # Toolbar lateral
            create_toolbar(
                manager=self.manager,
                on_tool_change=self._on_tool_change,
                on_color_change=self._on_color_change,
            )

            # Area principal
            with ui.column().classes('flex-grow items-center p-4 gap-4'):
                ui.label('Canvas Interactivo').classes('text-2xl font-bold')

                # Canvas
                self.canvas_view.build()

                # Barra de estado
                with ui.row().classes('w-full gap-4 items-center'):
                    self.status_label = ui.label('Herramienta: select')
                    self.coords_label = ui.label('Coordenadas: (0, 0)')
                    self.elements_label = ui.label(
                        f'Elementos: {len(self.manager.elements)}'
                    )

    def _on_tool_change(self, tool: str) -> None:
        """Cambia la herramienta activa."""
        self.manager.current_tool = tool
        if self.status_label:
            self.status_label.text = f'Herramienta: {tool}'

    def _on_color_change(self, color: str) -> None:
        """Cambia el color activo."""
        self.manager.fill_color = color
        self.manager.stroke_color = color
