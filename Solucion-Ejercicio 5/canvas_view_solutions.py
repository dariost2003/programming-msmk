from elements import create_freedraw

#elif tool == "freedraw":
            # TODO (Tarea 1): Crear un nuevo FreeDrawElement
            # Inicializar con el primer punto (x, y)
            # Agregar al manager
            # Pista: usar create_freedraw(points=[(x, y)], stroke_color=manager.stroke_color)
#pass

#mouse down 
def _on_mouse_down(self, e):
    x = e.args['offsetX']
    y = e.args['offsetY']
    tool = self.manager.current_tool

    self._is_drawing = True

    if tool == "freedraw":
        element = create_freedraw(
            points=[(x, y)],
            stroke_color=self.manager.stroke_color,
            stroke_width=self.manager.stroke_width,
        )

        self.manager.add_element(element)

#Mouse Move: 
def _on_mouse_move(self, e):
    if not self._is_drawing:
        return

    x = e.args['offsetX']
    y = e.args['offsetY']
    tool = self.manager.current_tool

    if tool == "freedraw":
        element = self.manager.elements[-1]
        element.points.append((x, y))
        self.refresh()

#Mouse up: 
def _on_mouse_up(self, e):
    self._is_drawing = False
    self.refresh()

