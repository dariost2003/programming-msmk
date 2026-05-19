from __future__ import annotations

# Convertir el color hexadecimal a formato rgba
# Args: color hexadecimal, nivel de transparencia
def hexadecimal_to_rgba(colores_hexadecimales: str, alpha: float) -> str:
    hex_color = colores_hexadecimales.strip().lstrip('#')

    if len(colores_hexadecimales) != 6:
        raise ValueError(
            'El color hexadecima debe tener 6 caracteres'
        )
    
    r, g, b = (
        int(hex_color[i:i+2],16) 
        for i in (0, 2, 4)
    )
    
    # Devuelve el color en formato rgba
    return f'rgba({r}, {g}, {b}, {alpha})'

# Genera un fondo degradado css usando de base un color en formato rgba
def fondo_de_pantalla(colores_hexadecimales):
    rgba_colorfuerte = hexadecimal_to_rgba(colores_hexadecimales, 0.15)
    rgba_colordebil = hexadecimal_to_rgba(colores_hexadecimales, 0.05)

    return (f"linear-gradient(135deg, {rgba_colorfuerte} 0%, {rgba_colordebil} 100%)")






