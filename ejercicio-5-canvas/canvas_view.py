"""
canvas_view.py - Componente visual del canvas interactivo.

Renderiza el SVG con todos los elementos y maneja los eventos
de mouse/touch para dibujar, seleccionar y arrastrar.
"""

from nicegui import ui
from canvas_manager import CanvasManager
from elements import create_rect


class CanvasView:
    """
    Vista del canvas interactivo.

    Renderiza el SVG con todos los elementos y maneja los eventos
    de mouse/touch para dibujar, seleccionar y arrastrar.
    """

    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600

    def __init__(self, manager: CanvasManager):
        self.manager = manager
        self.svg_container = None
        self.widget_container = None
        self._is_drawing = False
        self._start_x = 0
        self._start_y = 0

        # Agregar un rectangulo de demo para que el canvas no este vacio
        demo_rect = create_rect(100, 100, width=150, height=80, fill_color="#4A90D9")
        self.manager.add_element(demo_rect)

    def build(self) -> None:
        """Construye el componente visual del canvas."""
        # Contenedor principal con posicion relativa (para widgets absolutos encima)
        self.canvas_wrapper = ui.element('div').style(
            f'position: relative; width: {self.CANVAS_WIDTH}px; height: {self.CANVAS_HEIGHT}px; '
            'border: 2px solid #ccc; border-radius: 8px; overflow: hidden; '
            'cursor: crosshair; touch-action: none; user-select: none; '
            'box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
        )

        with self.canvas_wrapper:
            # Capa SVG (figuras, flechas, dibujo libre)
            self.svg_container = ui.html(
                self.manager.build_svg(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
            )

            # Capa de widgets interactivos (Tarea 5)
            # TODO: Los widgets NiceGUI se posicionaran aqui con CSS absoluto
            # Ejemplo:
            # ui.button('Click').style('position: absolute; left: 200px; top: 300px;')

        # --- Registrar eventos de mouse ---
        self.canvas_wrapper.on(
            'mousedown',
            self._on_mouse_down,
            ['offsetX', 'offsetY', 'button'],
        )
        self.canvas_wrapper.on(
            'mousemove',
            self._on_mouse_move,
            ['offsetX', 'offsetY', 'buttons'],
            throttle=0.03,
        )
        self.canvas_wrapper.on(
            'mouseup',
            self._on_mouse_up,
            ['offsetX', 'offsetY'],
        )

        # Prevenir menu contextual en click derecho
        self.canvas_wrapper.on('contextmenu.prevent', lambda e: None)

    def refresh(self) -> None:
        """Actualiza el SVG del canvas."""
        if self.svg_container:
            self.svg_container.content = self.manager.build_svg(
                self.CANVAS_WIDTH, self.CANVAS_HEIGHT
            )
            self.svg_container.update()

    # --- Handlers de eventos ---

    def _on_mouse_down(self, e) -> None:
        """Maneja el evento de presionar el mouse/dedo."""
        x = e.args['offsetX']
        y = e.args['offsetY']
        self._is_drawing = True
        self._start_x = x
        self._start_y = y

        tool = self.manager.current_tool

        if tool == "select":
            # TODO (Tarea 2): Buscar elemento bajo el cursor con find_element_at()
            # Si hay elemento, seleccionarlo. Si no, deseleccionar.
            # TODO (Tarea 3): Si hay elemento seleccionado bajo el cursor, iniciar drag
            pass

        elif tool == "freedraw":
            # TODO (Tarea 1): Crear un nuevo FreeDrawElement
            # Inicializar con el primer punto (x, y)
            # Agregar al manager
            # Pista: usar create_freedraw(points=[(x, y)], stroke_color=manager.stroke_color)
            pass

        elif tool in ("rect", "circle"):
            # TODO (Tarea 2): Guardar posicion inicial para rubber-band
            # El rectangulo/circulo se creara en mouse_up con las dimensiones del drag
            pass

        elif tool == "arrow":
            # TODO (Tarea 4): Guardar posicion inicial de la flecha
            # Opcionalmente, detectar si se esta conectando a un elemento existente
            pass

        elif tool.startswith("widget_"):
            # TODO (Tarea 5): Colocar un widget interactivo en la posicion del click
            # Pistas:
            # - Crear un WidgetElement con create_widget(x, y, widget_type)
            # - El widget_type se extrae del nombre de la herramienta: tool.replace("widget_", "")
            # - Renderizar el widget NiceGUI con CSS position: absolute
            pass

    def _on_mouse_move(self, e) -> None:
        """Maneja el movimiento del mouse/dedo."""
        if not self._is_drawing:
            return

        x = e.args['offsetX']
        y = e.args['offsetY']
        tool = self.manager.current_tool

        if tool == "freedraw":
            # TODO (Tarea 1): Agregar punto al FreeDrawElement actual
            # Pista: obtener el ultimo elemento agregado, agregar (x, y) a su lista de puntos
            # Llamar a self.refresh() para actualizar el canvas
            pass

        elif tool == "select":
            # TODO (Tarea 3): Si estamos arrastrando un elemento, moverlo
            # Calcular delta desde la posicion anterior
            # Llamar a manager.move_element()
            # Actualizar _start_x, _start_y para el siguiente frame
            # Llamar a self.refresh()
            pass

        elif tool in ("rect", "circle"):
            # TODO (Tarea 2): Actualizar preview (rubber-band)
            # Calcular width/height desde _start_x/_start_y hasta x/y
            # Opcion: crear un elemento temporal y refrescar, o dibujar un preview SVG
            pass

        elif tool == "arrow":
            # TODO (Tarea 4): Actualizar preview de la flecha
            # Dibujar una linea temporal desde el punto inicial hasta la posicion actual
            pass

    def _on_mouse_up(self, e) -> None:
        """Maneja el evento de soltar el mouse/dedo."""
        if not self._is_drawing:
            return

        x = e.args['offsetX']
        y = e.args['offsetY']
        self._is_drawing = False
        tool = self.manager.current_tool

        if tool == "freedraw":
            # TODO (Tarea 1): Finalizar el FreeDrawElement actual
            # El trazo ya esta completo, no hay nada mas que hacer
            pass

        elif tool in ("rect", "circle"):
            # TODO (Tarea 2): Crear el elemento final con las dimensiones del drag
            # Pistas:
            # - Calcular x, y, width, height a partir de _start_x, _start_y, x, y
            # - Usar min() para manejar drag en cualquier direccion
            # - width = abs(x - self._start_x), height = abs(y - self._start_y)
            # - Ignorar si el area es muy pequena (menos de 5x5)
            # - Usar create_rect() o create_circle() con el color actual del manager
            pass

        elif tool == "arrow":
            # TODO (Tarea 4): Crear el ArrowElement final
            # Pistas:
            # - Usar create_arrow(start_x, start_y, end_x, end_y)
            # - Detectar si el extremo esta sobre un elemento (para conectar)
            # - Si hay elemento en el inicio, asignar source_id
            # - Si hay elemento en el final, asignar target_id
            pass

        self.refresh()
