# Ejercicio 5: Canvas Interactivo

## Descripcion

Construir una aplicacion de canvas/pizarra interactiva (similar a un Excalidraw simplificado) usando NiceGUI. Permite dibujar a mano alzada, crear figuras geometricas, conectar elementos con flechas, y colocar widgets interactivos (botones, sliders, inputs) directamente sobre el canvas.

La aplicacion funciona como servidor web, accesible desde cualquier navegador. Compatible con desktop, tablet (iPad) y movil.

## Que esta incluido (codigo base)

| Archivo | Descripcion |
|---------|-------------|
| `main.py` | Punto de entrada, inicia el servidor NiceGUI |
| `app.py` | Clase principal que combina toolbar + canvas + barra de estado |
| `canvas_view.py` | Componente visual del canvas con eventos de mouse |
| `canvas_manager.py` | Gestion del estado: elementos, herramienta activa, generacion SVG |
| `toolbar.py` | Barra de herramientas lateral con botones, colores y controles |
| `elements.py` | Dataclasses para los tipos de elementos (rect, circle, text, arrow, freedraw, widget) |
| `app_ejemplo.py` | Ejemplo minimo independiente con dibujo libre basico |
| `requirements.txt` | Dependencias del proyecto |

**Lo que ya funciona:**
- Interfaz completa con toolbar lateral y canvas central
- Renderizado SVG con cuadricula
- Un rectangulo de demo visible en el canvas
- Eventos de mouse registrados (mousedown, mousemove, mouseup)
- Paleta de colores y control de grosor
- Barra de estado con herramienta activa
- Clases base para todos los tipos de elementos
- `contains_point()` implementado para RectElement y CircleElement
- `to_svg()` implementado para RectElement, CircleElement y TextElement

## Como ejecutar

```bash
cd ejercicio-5-canvas
pip install -r requirements.txt
python main.py
```

Se abrira automaticamente en el navegador en **http://localhost:8080**

### Ejemplo minimo (independiente)

Para ver un ejemplo basico de dibujo libre sin las demas dependencias:

```bash
python app_ejemplo.py
```

### Acceder desde iPad/movil

1. Asegurate de que tu ordenador y el dispositivo estan en la misma red WiFi
2. Ejecuta `python main.py`
3. Busca la IP de tu ordenador (en macOS: `ifconfig | grep inet`)
4. En el iPad/movil, abre el navegador y ve a `http://<TU_IP>:8080`

## Tareas para el estudiante

### Tarea 1: Sistema de dibujo libre

Implementar el dibujo a mano alzada en el canvas.

**Donde modificar:**
- `elements.py` - metodo `FreeDrawElement.to_svg()`: renderizar el trazo como path SVG
- `canvas_view.py` - metodos `_on_mouse_down`, `_on_mouse_move`, `_on_mouse_up`: capturar puntos del trazo

**Que hacer:**
- Al presionar el mouse con la herramienta "freedraw", crear un `FreeDrawElement`
- Al mover el mouse, agregar puntos a la lista y refrescar el canvas
- Al soltar, finalizar el trazo
- El color y grosor deben tomarse de los controles de la toolbar

**Tips:**
- Mira `app_ejemplo.py` para ver como funciona el dibujo libre en un ejemplo simple
- En SVG, un path se define como: `M x0 y0 L x1 y1 L x2 y2 ...`
- Usa `fill="none"` para que solo se vea el trazo
- `stroke-linecap="round"` y `stroke-linejoin="round"` suavizan el trazo

### Tarea 2: Creacion y seleccion de figuras

Implementar la creacion de rectangulos, circulos y texto, y la seleccion con click.

**Donde modificar:**
- `canvas_manager.py` - metodo `find_element_at()`: buscar elemento bajo el cursor
- `canvas_view.py` - handlers de mouse para herramientas "rect", "circle" y "select"
- `elements.py` - metodo `ArrowElement.to_svg()` (preparacion para Tarea 4)

**Que hacer:**
- Herramienta "rect": al arrastrar, crear un rectangulo con las dimensiones del drag
- Herramienta "circle": igual pero creando un circulo
- Herramienta "text": al hacer click, crear un TextElement (opcionalmente pedir el texto con un dialogo)
- Herramienta "select": al hacer click, buscar el elemento bajo el cursor y seleccionarlo

**Tips:**
- Calcula `width = abs(x - start_x)` y `height = abs(y - start_y)` para manejar drag en cualquier direccion
- Usa `min(x, start_x)` para la esquina superior izquierda
- Ignora areas muy pequenas (menos de 5x5 pixeles) para evitar clicks accidentales
- `find_element_at()` debe recorrer la lista en orden inverso (el ultimo dibujado esta encima)

### Tarea 3: Arrastrar y reposicionar

Implementar el movimiento de elementos arrastrando con el mouse.

**Donde modificar:**
- `canvas_manager.py` - metodo `move_element()`: actualizar posicion del elemento
- `canvas_view.py` - handler de "select" en `_on_mouse_move`: calcular delta y mover

**Que hacer:**
- Con la herramienta "select", si hay un elemento bajo el cursor al presionar, iniciar drag
- Al mover, calcular el desplazamiento (delta) y actualizar la posicion del elemento
- El movimiento debe ser fluido (actualizar en cada evento mousemove)
- Opcionalmente, aplicar snap-to-grid al soltar

**Tips:**
- Guarda la posicion del mouse anterior para calcular el delta: `dx = x - prev_x`
- Distingue entre click (seleccionar) y drag (mover) usando un umbral minimo de movimiento
- `snap_to_grid()` ya esta implementado en CanvasManager

### Tarea 4: Flechas y conectores

Implementar flechas que conecten puntos o elementos entre si.

**Donde modificar:**
- `elements.py` - metodo `ArrowElement.to_svg()`: renderizar la flecha con punta
- `canvas_manager.py` - metodo `update_connected_arrows()`: actualizar flechas al mover elementos
- `canvas_view.py` - handlers de mouse para la herramienta "arrow"

**Que hacer:**
- Dibujar una flecha desde el punto donde se presiona hasta donde se suelta
- La flecha debe tener una punta visible (triangulo) en el extremo final
- Si el inicio o fin de la flecha esta sobre un elemento, conectarla (guardar source_id/target_id)
- Al mover un elemento conectado, las flechas deben actualizarse automaticamente

**Tips:**
- Para la punta de flecha, calcula el angulo con `math.atan2(dy, dx)` y dibuja un triangulo rotado
- Otra opcion es usar `<marker>` SVG para la punta de flecha (busca "SVG marker arrowhead")
- Para conectar: usa `find_element_at()` en el punto de inicio y fin del drag

### Tarea 5: Widgets interactivos

Colocar controles NiceGUI reales (botones, sliders, inputs) sobre el canvas.

**Donde modificar:**
- `toolbar.py` - agregar botones para widget_button, widget_slider, widget_input
- `canvas_view.py` - handler `_on_mouse_down` para herramientas widget_*
- `elements.py` - clase `WidgetElement` (puede necesitar campos adicionales)

**Que hacer:**
- Agregar botones en la toolbar para colocar cada tipo de widget
- Al hacer click en el canvas con una herramienta de widget, crear el widget NiceGUI en esa posicion
- Los widgets deben ser funcionales (el boton hace algo, el slider mueve, el input acepta texto)
- Los widgets deben ser arrastrables (se pueden mover por el canvas)

**Tips:**
- Los widgets NiceGUI se posicionan con CSS absoluto: `style('position: absolute; left: Xpx; top: Ypx;')`
- Usa `ui.button()`, `ui.slider()`, `ui.input()` dentro del `canvas_wrapper`
- Para hacer un widget arrastrable, necesitaras handlers de mouse adicionales en el propio widget
- Los widgets NO se renderizan como SVG (por eso `WidgetElement.to_svg()` retorna cadena vacia)

## Conceptos clave de NiceGUI

| Concepto | Ejemplo |
|----------|---------|
| Renderizar HTML/SVG | `ui.html('<svg>...</svg>')` |
| Contenedor con estilo | `ui.element('div').style('position: relative; ...')` |
| Eventos de mouse | `elemento.on('mousedown', handler, ['offsetX', 'offsetY'])` |
| Throttle de eventos | `elemento.on('mousemove', handler, args, throttle=0.03)` |
| Actualizar contenido | `html_element.content = nuevo_svg; html_element.update()` |
| Botones e inputs | `ui.button('Texto', on_click=handler)`, `ui.slider(min=1, max=10)` |
| Layout | `ui.row()`, `ui.column()`, `ui.card()` |
| Posicion absoluta | `.style('position: absolute; left: 100px; top: 200px;')` |

## Estructura del proyecto

```
ejercicio-5-canvas/
    main.py              # Punto de entrada
    app.py               # Aplicacion principal (layout)
    canvas_view.py       # Componente visual del canvas
    canvas_manager.py    # Gestion del estado y generacion SVG
    toolbar.py           # Barra de herramientas lateral
    elements.py          # Clases de elementos del canvas
    app_ejemplo.py       # Ejemplo minimo independiente
    requirements.txt     # Dependencias (nicegui)
    README.md            # Este archivo
    CRITERIOS.md         # Rubrica de evaluacion
```

## Recursos

- [Documentacion de NiceGUI](https://nicegui.io/documentation)
- [Referencia SVG (MDN)](https://developer.mozilla.org/es/docs/Web/SVG)
- [SVG Path (tutorial)](https://developer.mozilla.org/es/docs/Web/SVG/Tutorial/Paths)
- [SVG Markers (flechas)](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker)
