"""
elements.py - Clases para los elementos del canvas interactivo.

Define los tipos de elementos que se pueden dibujar en el canvas:
rectangulos, circulos, texto, flechas, dibujo libre y widgets.
Cada clase incluye su representacion SVG y deteccion de colisiones.

Patron: similar a ejercicio-2-juego/entities.py con dataclasses y funciones de fabrica.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import uuid


# --- Paleta de colores ---

COLORES = {
    "azul": "#4A90D9",
    "rojo": "#E74C3C",
    "verde": "#2ECC71",
    "amarillo": "#F1C40F",
    "morado": "#9B59B6",
    "naranja": "#E67E22",
    "gris": "#95A5A6",
    "negro": "#333333",
}


# --- Clase base ---

@dataclass
class CanvasElement:
    """Elemento base del canvas. Todas las figuras heredan de esta clase."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 60.0
    color: str = "#4A90D9"
    element_type: str = "base"

    def to_svg(self) -> str:
        """Genera representacion SVG del elemento. Sobreescribir en subclases."""
        return ""

    def contains_point(self, px: float, py: float) -> bool:
        """Verifica si un punto esta dentro del elemento.
        TODO: Implementar en cada subclase para deteccion de clicks."""
        return False


# --- Rectangulo ---

@dataclass
class RectElement(CanvasElement):
    """Rectangulo con bordes redondeados."""
    fill_color: str = "#4A90D9"
    border_color: str = "#2C5F8A"
    border_width: int = 2
    border_radius: int = 4
    element_type: str = "rect"

    def to_svg(self) -> str:
        return (
            f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" '
            f'rx="{self.border_radius}" fill="{self.fill_color}" '
            f'stroke="{self.border_color}" stroke-width="{self.border_width}" />'
        )

    # contains_point implementado como ejemplo
    def contains_point(self, px: float, py: float) -> bool:
        return self.x <= px <= self.x + self.width and self.y <= py <= self.y + self.height


# --- Circulo ---

@dataclass
class CircleElement(CanvasElement):
    """Circulo (se dibuja inscrito en el bounding box)."""
    fill_color: str = "#E74C3C"
    border_color: str = "#C0392B"
    border_width: int = 2
    element_type: str = "circle"

    def to_svg(self) -> str:
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        r = min(self.width, self.height) / 2
        return (
            f'<circle cx="{cx}" cy="{cy}" r="{r}" '
            f'fill="{self.fill_color}" stroke="{self.border_color}" '
            f'stroke-width="{self.border_width}" />'
        )

    # contains_point implementado como ejemplo
    def contains_point(self, px: float, py: float) -> bool:
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        r = min(self.width, self.height) / 2
        return ((px - cx) ** 2 + (py - cy) ** 2) <= r ** 2


# --- Texto ---

@dataclass
class TextElement(CanvasElement):
    """Texto posicionado en el canvas."""
    text: str = "Texto"
    font_size: int = 16
    font_color: str = "#333333"
    element_type: str = "text"

    def to_svg(self) -> str:
        """TODO: Implementar renderizado SVG de texto.
        Pista: usar <text x="..." y="..." font-size="..." fill="...">texto</text>
        Nota: la coordenada Y en SVG text es la linea base, no la esquina superior."""
        return (
            f'<text x="{self.x}" y="{self.y + self.font_size}" '
            f'font-size="{self.font_size}" fill="{self.font_color}">'
            f'{self.text}</text>'
        )

# --- Flecha ---

@dataclass
class ArrowElement(CanvasElement):
    """Flecha/conector entre dos puntos (opcionalmente conectada a elementos)."""
    start_x: float = 0.0
    start_y: float = 0.0
    end_x: float = 100.0
    end_y: float = 50.0
    stroke_color: str = "#333333"
    stroke_width: int = 2
    source_id: Optional[str] = None  # ID del elemento origen (si esta conectada)
    target_id: Optional[str] = None  # ID del elemento destino (si esta conectada)
    element_type: str = "arrow"

    def to_svg(self) -> str:
        """TODO: Implementar renderizado SVG de flecha.
        Debe incluir:
        1. Una linea desde (start_x, start_y) hasta (end_x, end_y)
        2. Una punta de flecha (triangulo) en el extremo final
        Pistas:
        - Usar <line> para el cuerpo
        - Usar <polygon> o <path> para la punta
        - Calcular el angulo con math.atan2 para orientar la punta
        - Definir un <marker> SVG para la punta de flecha es otra opcion valida
        """
        return ""


# --- Dibujo libre ---

@dataclass
class FreeDrawElement(CanvasElement):
    """Trazo de dibujo a mano alzada."""
    points: list = field(default_factory=list)  # Lista de (x, y)
    stroke_color: str = "#333333"
    stroke_width: int = 3
    element_type: str = "freedraw"

    def to_svg(self) -> str:
        """TODO: Implementar renderizado SVG del trazo libre.
        Pistas:
        - Usar <path d="M x0 y0 L x1 y1 L x2 y2 ...">
        - M = moveTo (primer punto), L = lineTo (siguientes puntos)
        - fill="none" para que solo se vea el trazo
        - stroke-linecap="round" y stroke-linejoin="round" para suavizar
        """
        return ""

# --- Widget ---

@dataclass
class WidgetElement(CanvasElement):
    """Widget interactivo (boton, slider, input) posicionado sobre el canvas."""
    widget_type: str = "button"  # "button", "slider", "text_input"
    widget_config: dict = field(default_factory=lambda: {"label": "Boton", "value": 0})
    element_type: str = "widget"

    def to_svg(self) -> str:
        """Los widgets no se renderizan como SVG.
        Se renderizan como controles NiceGUI posicionados sobre el canvas.
        Ver canvas_view.py para la implementacion."""
        return ""


# --- Funciones de fabrica ---

def create_rect(x: float, y: float, width: float = 100, height: float = 60, **kwargs) -> RectElement:
    """Crea un rectangulo en la posicion dada."""
    return RectElement(x=x, y=y, width=width, height=height, **kwargs)


def create_circle(x: float, y: float, diameter: float = 60, **kwargs) -> CircleElement:
    """Crea un circulo en la posicion dada."""
    return CircleElement(x=x, y=y, width=diameter, height=diameter, **kwargs)


def create_text(x: float, y: float, text: str = "Texto", **kwargs) -> TextElement:
    """Crea un elemento de texto en la posicion dada."""
    return TextElement(x=x, y=y, text=text, **kwargs)


def create_arrow(start_x: float, start_y: float, end_x: float, end_y: float, **kwargs) -> ArrowElement:
    """Crea una flecha entre dos puntos."""
    return ArrowElement(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y, **kwargs)


def create_freedraw(points: list | None = None, **kwargs) -> FreeDrawElement:
    """Crea un trazo de dibujo libre con los puntos dados."""
    if points is None:
        points = []
    return FreeDrawElement(points=points, **kwargs)


def create_widget(x: float, y: float, widget_type: str = "button", **kwargs) -> WidgetElement:
    """Crea un widget interactivo en la posicion dada."""
    config = {"label": "Boton", "value": 0}
    if widget_type == "slider":
        config = {"label": "Slider", "value": 50, "min": 0, "max": 100}
    elif widget_type == "text_input":
        config = {"label": "Texto", "value": ""}
    return WidgetElement(x=x, y=y, widget_type=widget_type, widget_config=config, **kwargs)
