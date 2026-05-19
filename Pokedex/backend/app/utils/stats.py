from __future__ import annotations

from app.core.constants import INTERACTIONS_DATESET

# Calcula las interacciones de daño de los Pokemon 
# Ej: fire + flying -> water: x2, grass: x0.25, ground: x0

def damage_interactions(types: list[str]) -> dict[str, float]:
   
    multipliers = {type: 1.0 for type in INTERACTIONS_DATESET.keys()}
    
    for tipo in types:

        data = INTERACTIONS_DATESET.get(tipo, {})

        # Debilidades
        for weak_type in data.get('weak', []): 
            multipliers[weak_type] *= 2.0 

        # Resistencias
        for resist_type in data.get('resist', []): 
            multipliers[resist_type] *= 0.5

        # Inmunidades
        for inmune_type in data.get('inmune', []): 
            multipliers[inmune_type] *= 0.0

    return multipliers

# Clasifica los multiplicadores de la defensa en categorias para la interfaz de usuario
def classify_defense(defenses: dict[str, float]) -> dict[str, list[tuple[str, float]]]:
    
    if not isinstance(defenses, dict):
        raise TypeError('Se esperaba un diccionario en defensas')
    
    categories = {
        'muy_debil': [],
        'debil': [],
        'neutral': [],
        'resiste': [],
        'muy_resiste': [],
        'inmune': []
    }

    for type, multipliers in defenses.items():
        if abs(multipliers - 4.0) < 0.01:
            categories['muy_debil'].append((type, multipliers))

        elif abs(multipliers - 2.0) < 0.01:
            categories['debil'].append((type,multipliers))

        elif abs(multipliers - 1.0) < 0.01:
            categories['neutral'].append((type,multipliers))

        elif abs(multipliers - 0.5) < 0.01:
            categories['resiste'].append((type,multipliers))

        elif abs(multipliers - 0.25) < 0.01:
            categories['muy_resiste'].append((type,multipliers))

        elif abs(multipliers - 0.0) < 0.01:
            categories['inmune'].append((type,multipliers))
    
    return categories

# Función que unifica las defensas
def get_offensive_brief(types: list[str]) -> dict:

    defenses = damage_interactions(types)

    return classify_defense(defenses)
    