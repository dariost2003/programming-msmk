def hexadecimal_to_rgba(hex_color: str, alpha: float) -> str:
    cleaned = hex_color.strip().lstrip('#')
    if len(cleaned) != 6:
        raise ValueError('El color hexadecimal debe tener 6 caracteres')

    r, g, b = (int(cleaned[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'
