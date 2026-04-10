"""
canvas_manager.py - Gestion del estado del canvas.

Maneja la lista de elementos, la herramienta activa, colores,
cuadricula y generacion del SVG completo.
"""

from __future__ import annotations

from elements import CanvasElement, ArrowElement


class CanvasManager:
    """
    Gestor del estado del canvas interactivo.

    Almacena todos los elementos, la herramienta activa, colores actuales,
    y genera el SVG completo para renderizar.
    """

    def __init__(self):
        self.elements: list[CanvasElement] = []
        self.selected_id: str | None = None
        self.current_tool: str = "select"  # select, freedraw, rect, circle, arrow, text, widget_button, widget_slider, widget_input
        self.stroke_color: str = "#333333"
        self.fill_color: str = "#4A90D9"
        self.stroke_width: int = 2
        self.grid_size: int = 20
        self.grid_visible: bool = True

    # --- Operaciones CRUD de elementos ---

    def add_element(self, element: CanvasElement) -> CanvasElement:
        """Agrega un elemento al canvas."""
        self.elements.append(element)
        return element

    def remove_element(self, element_id: str) -> None:
        """Elimina un elemento por su ID."""
        self.elements = [e for e in self.elements if e.id != element_id]

    def get_element(self, element_id: str) -> CanvasElement | None:
        """Busca un elemento por su ID."""
        for e in self.elements:
            if e.id == element_id:
                return e
        return None

    # --- Seleccion ---

    def select_element(self, element_id: str | None) -> None:
        """Selecciona un elemento (o deselecciona si None)."""
        self.selected_id = element_id

    def get_selected(self) -> CanvasElement | None:
        """Retorna el elemento seleccionado o None."""
        if self.selected_id:
            return self.get_element(self.selected_id)
        return None

    # --- Cuadricula ---

    def snap_to_grid(self, x: float, y: float) -> tuple[float, float]:
        """Ajusta coordenadas a la cuadricula mas cercana."""
        return (
            round(x / self.grid_size) * self.grid_size,
            round(y / self.grid_size) * self.grid_size,
        )

    # --- Busqueda y movimiento ---

    def find_element_at(self, x: float, y: float) -> CanvasElement | None:
        """TODO: Buscar el elemento que contiene el punto (x, y).
        Pistas:
        - Recorrer self.elements en orden inverso (el de arriba primero)
        - Usar el metodo contains_point() de cada elemento
        - Los WidgetElements no se buscan aqui (tienen sus propios handlers)
        - Retornar None si no hay elemento en esa posicion
        """
        return None

    def move_element(self, element_id: str, new_x: float, new_y: float) -> None:
        """TODO: Mover un elemento a una nueva posicion.
        Pistas:
        - Obtener el elemento con get_element()
        - Actualizar sus coordenadas x, y
        - Si hay flechas conectadas, llamar a update_connected_arrows()
        """
        pass

    def update_connected_arrows(self, element_id: str) -> None:
        """TODO: Actualizar las flechas conectadas a un elemento que se movio.
        Pistas:
        - Buscar todas las ArrowElements donde source_id o target_id == element_id
        - Recalcular start_x/y o end_x/y basandose en la posicion actual del elemento
        - Para un resultado visual limpio, calcular el punto en el borde del elemento
          (no el centro)
        """
        pass

    # --- Generacion SVG ---

    def build_svg(self, canvas_width: int = 800, canvas_height: int = 600) -> str:
        """Genera el SVG completo del canvas con todos los elementos."""
        svg_parts = [
            f'<svg width="100%" height="100%" viewBox="0 0 {canvas_width} {canvas_height}" '
            f'xmlns="http://www.w3.org/2000/svg" style="background: #FAFAFA;">'
        ]

        # Dibujar cuadricula si esta visible
        if self.grid_visible:
            svg_parts.append(self._build_grid_svg(canvas_width, canvas_height))

        # Dibujar todos los elementos (excepto widgets, que se renderizan aparte)
        for element in self.elements:
            if element.element_type != "widget":
                svg_str = element.to_svg()
                if svg_str:
                    svg_parts.append(svg_str)

        # Dibujar handles de seleccion
        selected = self.get_selected()
        if selected and selected.element_type != "widget":
            svg_parts.append(self._build_selection_handles(selected))

        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)

    def _build_grid_svg(self, w: int, h: int) -> str:
        """Genera las lineas de la cuadricula."""
        lines = []
        for x in range(0, w + 1, self.grid_size):
            lines.append(
                f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" '
                f'stroke="#E0E0E0" stroke-width="0.5" />'
            )
        for y in range(0, h + 1, self.grid_size):
            lines.append(
                f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" '
                f'stroke="#E0E0E0" stroke-width="0.5" />'
            )
        return '\n'.join(lines)

    def _build_selection_handles(self, element: CanvasElement) -> str:
        """Genera los handles de seleccion para un elemento."""
        x, y, w, h = element.x, element.y, element.width, element.height
        handle_size = 8
        hs = handle_size / 2

        handles = [
            # Borde de seleccion (linea punteada azul)
            f'<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{h + 4}" '
            f'fill="none" stroke="#0078D4" stroke-width="1.5" stroke-dasharray="5,3" />',
        ]

        # 4 handles en las esquinas
        for hx, hy in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
            handles.append(
                f'<rect x="{hx - hs}" y="{hy - hs}" width="{handle_size}" height="{handle_size}" '
                f'fill="white" stroke="#0078D4" stroke-width="1.5" />'
            )

        return '\n'.join(handles)
