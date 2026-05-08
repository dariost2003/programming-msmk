# FreeDrawElement.to_svg() 
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class CanvasElement:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

@dataclass
class FreeDrawElement(CanvasElement):
    points: list = field(default_factory=list)
    stroke_color: str = "#333333"
    stroke_width: int = 3
    element_type: str = "freedraw"

    def to_svg(self) -> str:
        if not self.points:
            return ""

        path_data = f"M {self.points[0][0]} {self.points[0][1]}"

        for x, y in self.points[1:]:
            path_data += f" L {x} {y}"

        return f"""
        <path d="{path_data}"
              stroke="{self.stroke_color}"
              stroke-width="{self.stroke_width}"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"/>
        """
#codigo para probar tarea 1: 
if __name__ == "__main__":
    elemento = FreeDrawElement(points=[(10, 10), (20, 20), (30, 15)])
    print(elemento.to_svg())

