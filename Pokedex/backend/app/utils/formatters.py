from __future__ import annotations

# Vuelve mayusculas la primera letra de un texto y retira guiones
def capitalize_text(texto: str) -> str:

    return texto.replace('-', ' ').title()

# Convierte la altura de decimetros a metros
def height_format(height: int) -> str:

    return f'{height / 10:.1f} m'

# Convierte el peso de hectogramos a kilogramos
def weight_format(weight: int) -> str:

    return f'{weight / 10:.1f} kg'

# Convierte nombres de la API en nombres legibles y mejores para la UI
def stats_format(stat_name: str) -> str:

    translations = {
        'hp': 'HP',
        'attack':'Attack',
        'defense':'Defense',
        'special-attack':'Sp. Attack',
        'special-defense':'Sp. Defense',
        'speed':'Speed',
    }

    return translations.get(stat_name.lower(), stat_name.replace('-', ' ').title())

# Convierte los tipos de Pokemon en un formato más limpio
def type_format(tipo: str) -> str:

    return tipo.capitalize()

# Limpia los caracteres especiales de la PokeAPI
def flavor_text_format(texto: str) -> str:
    
    return (
        texto.replace('\n', ' ')
        .replace('\f', ' ')
        .replace('\r', ' ')
        .strip()
    )

