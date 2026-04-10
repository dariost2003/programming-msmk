#!/usr/bin/env python3
"""
app_ejemplo.py - Ejemplo minimo de un canvas interactivo con NiceGUI.

Este archivo es completamente independiente (no importa otros modulos del proyecto).
Demuestra:
  - Un canvas SVG dentro de un contenedor con eventos de mouse
  - Un rectangulo estatico renderizado como SVG
  - Dibujo libre a mano alzada basico
  - Botones de color para cambiar el trazo

Ejecutar con:
    python app_ejemplo.py

Luego abrir http://localhost:8080 en el navegador.

# Este es solo un ejemplo. Tu tarea es construir el canvas interactivo completo.
"""

from nicegui import ui


# --- Estado global del ejemplo ---
class EstadoEjemplo:
    def __init__(self):
        self.trazos: list[dict] = []       # Lista de trazos completados
        self.trazo_actual: list = []        # Puntos del trazo en progreso
        self.dibujando: bool = False
        self.color: str = "#333333"
        self.grosor: int = 3


estado = EstadoEjemplo()
svg_container = None


def generar_svg() -> str:
    """Genera el SVG completo con el rectangulo de demo y todos los trazos."""
    partes = [
        '<svg width="100%" height="100%" viewBox="0 0 800 500" '
        'xmlns="http://www.w3.org/2000/svg" style="background: #FAFAFA;">',
        # Cuadricula simple
    ]

    # Cuadricula
    for x in range(0, 801, 20):
        partes.append(f'<line x1="{x}" y1="0" x2="{x}" y2="500" stroke="#E8E8E8" stroke-width="0.5" />')
    for y in range(0, 501, 20):
        partes.append(f'<line x1="0" y1="{y}" x2="800" y2="{y}" stroke="#E8E8E8" stroke-width="0.5" />')

    # Rectangulo de demo
    partes.append(
        '<rect x="80" y="80" width="160" height="100" rx="6" '
        'fill="#4A90D9" stroke="#2C5F8A" stroke-width="2" />'
    )
    partes.append(
        '<text x="110" y="140" font-size="16" fill="white" '
        'font-family="sans-serif">Rectangulo</text>'
    )

    # Trazos completados
    for trazo in estado.trazos:
        svg_path = _puntos_a_path(trazo['puntos'])
        if svg_path:
            partes.append(
                f'<path d="{svg_path}" fill="none" '
                f'stroke="{trazo["color"]}" stroke-width="{trazo["grosor"]}" '
                f'stroke-linecap="round" stroke-linejoin="round" />'
            )

    # Trazo actual (en progreso)
    if estado.trazo_actual:
        svg_path = _puntos_a_path(estado.trazo_actual)
        if svg_path:
            partes.append(
                f'<path d="{svg_path}" fill="none" '
                f'stroke="{estado.color}" stroke-width="{estado.grosor}" '
                f'stroke-linecap="round" stroke-linejoin="round" opacity="0.7" />'
            )

    partes.append('</svg>')
    return '\n'.join(partes)


def _puntos_a_path(puntos: list) -> str:
    """Convierte una lista de (x, y) a un path SVG."""
    if len(puntos) < 2:
        return ""
    d = f"M {puntos[0][0]} {puntos[0][1]}"
    for px, py in puntos[1:]:
        d += f" L {px} {py}"
    return d


def refrescar():
    """Actualiza el SVG en la interfaz."""
    global svg_container
    if svg_container:
        svg_container.content = generar_svg()
        svg_container.update()


# --- Handlers de eventos ---

def on_mouse_down(e):
    estado.dibujando = True
    x = e.args['offsetX']
    y = e.args['offsetY']
    estado.trazo_actual = [(x, y)]


def on_mouse_move(e):
    if not estado.dibujando:
        return
    x = e.args['offsetX']
    y = e.args['offsetY']
    estado.trazo_actual.append((x, y))
    refrescar()


def on_mouse_up(e):
    if not estado.dibujando:
        return
    estado.dibujando = False
    if len(estado.trazo_actual) >= 2:
        estado.trazos.append({
            'puntos': estado.trazo_actual[:],
            'color': estado.color,
            'grosor': estado.grosor,
        })
    estado.trazo_actual = []
    refrescar()


def cambiar_color(color: str):
    estado.color = color


def limpiar():
    estado.trazos.clear()
    estado.trazo_actual.clear()
    refrescar()


# --- Interfaz ---

@ui.page('/')
def pagina_principal():
    global svg_container

    ui.page_title('Ejemplo - Canvas Basico')

    with ui.column().classes('items-center p-4 gap-4'):
        ui.label('Ejemplo: Canvas Basico con NiceGUI').classes('text-xl font-bold')
        ui.label('Dibuja con el mouse sobre el canvas. Este es solo un ejemplo minimo.').classes('text-grey')

        # Botones de color
        with ui.row().classes('gap-2'):
            colores = {
                'Negro': '#333333',
                'Rojo': '#E74C3C',
                'Azul': '#4A90D9',
                'Verde': '#2ECC71',
                'Naranja': '#E67E22',
            }
            for nombre, hex_color in colores.items():
                ui.button(nombre, on_click=lambda c=hex_color: cambiar_color(c)).style(
                    f'background-color: {hex_color} !important; color: white;'
                )
            ui.button('Limpiar', icon='delete', on_click=limpiar).props('outline')

        # Canvas
        canvas = ui.element('div').style(
            'position: relative; width: 800px; height: 500px; '
            'border: 2px solid #ccc; border-radius: 8px; overflow: hidden; '
            'cursor: crosshair; touch-action: none; user-select: none; '
            'box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
        )

        with canvas:
            svg_container = ui.html(generar_svg())

        # Registrar eventos
        canvas.on('mousedown', on_mouse_down, ['offsetX', 'offsetY', 'button'])
        canvas.on('mousemove', on_mouse_move, ['offsetX', 'offsetY', 'buttons'], throttle=0.03)
        canvas.on('mouseup', on_mouse_up, ['offsetX', 'offsetY'])
        canvas.on('contextmenu.prevent', lambda e: None)

        ui.label(
            'Este es solo un ejemplo. Tu tarea es construir el canvas interactivo completo.'
        ).classes('text-sm text-grey italic')


# Iniciar servidor
ui.run(host='0.0.0.0', port=8080, title='Ejemplo Canvas')
