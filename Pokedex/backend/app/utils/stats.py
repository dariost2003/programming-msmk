TABLA_DE_INTERACCIONES = {
    'normal': {'resist': ['ghost'], 'weak': ['fighting']},
    'fire': {'resist':['fire', 'grass', 'ice', 'bug', 'steel', 'fairy'], 'weak': ['water', 'ground', 'rock']},
    'water': {'resist':['fire', 'water', 'ice', 'steel'], 'weak': ['grass', 'electric']},
    'grass': {'resist': ['water', 'ground', 'electric'], 'weak': ['fire', 'ice', 'poison', 'bug', 'flying']},
    'electric': {'resist': ['electric', 'flying', 'steel'], 'weak': ['ground']},
    'ice': {'resist': ['ice'], 'weak': ['fire', 'fighting', 'rock', 'steel']},
    'fighting': {'resist': ['bug', 'rock', 'dark'], 'weak': ['flying', 'psychic', 'fairy']},
    'poison': {'resist': ['grass', 'fighting', 'poison', 'bug', 'fairy'], 'weak': ['ground', 'psychic']},
    'ground': {'resist': ['poison', 'rock'], 'weak': ['water', 'grass', 'ice'], 'inmune': ['electric']},
    'flying': {'resist': ['grass', 'fighting', 'bug'], 'weak': ['electric', 'ice', 'rock'], 'inmune': ['ground']},
    'psychic': {'resist': ['flying', 'psychic'], 'weak': ['bug', 'ghost', 'dark']},
    'bug': {'resist': ['grass', 'fighting', 'ground'], 'weak': ['fire', 'flying', 'rock']},
    'rock': {'resist': ['normal', 'fire', 'poison', 'flying'], 'weak': ['water', 'grass', 'fighting', 'ground', 'steel']},
    'ghost': {'resist': ['poison', 'bug'], 'weak': ['ghost', 'dark'], 'inmune': ['normal', 'fighting']},
    'dragon': {'resist': ['fire', 'water', 'grass', 'electric'], 'weak': ['ice', 'dragon', 'fairy']},
    'dark': {'resist': ['ghost', 'dark'], 'weak': ['fighting', 'bug', 'fairy'], 'inmune': ['psychic']},
    'steel': {'resist': ['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy'], 'weak': ['fire', 'fighting', 'ground'], 'inmune': ['poison']},
    'fairy': {'resist': ['fighting', 'bug', 'dark'], 'weak': ['poison', 'steel'], 'inmune': ['dragon']}
}

def interacciones(tipos):
    multiplicadores = {t: 1.0 for t in TABLA_DE_INTERACCIONES.keys()}
    for t in tipos:
        data = TABLA_DE_INTERACCIONES.get(t, {})
        for w in data.get('weak', []): multiplicadores[w] *= 2.0 
        for r in data.get('resist', []): multiplicadores[r] *= 0.5
        for i in data.get('inmune', []): multiplicadores[i] *= 0.0
    return multiplicadores

def clasificar_defensas(defensas):
    if not isinstance(defensas, dict):
        raise TypeError('Se esperaba un dict en defensas')
    
    categorias = {
        'muy_debil': [],
        'debil': [],
        'neutral': [],
        'resiste': [],
        'muy_resiste': [],
        'inmune': []
    }
    for tipo, mult in defensas.items():
        if abs(mult - 4.0) < 0.01:
            categorias['muy_debil'].append((tipo, mult))
        elif abs(mult - 2.0) < 0.01:
            categorias['debil'].append((tipo,mult))
        elif abs(mult - 1.0) < 0.01:
            categorias['neutral'].append((tipo,mult))
        elif abs(mult - 0.5) < 0.01:
            categorias['resiste'].append((tipo,mult))
        elif abs(mult - 0.25) < 0.01:
            categorias['muy_resiste'].append((tipo,mult))
        elif abs(mult - 0.0) < 0.01:
            categorias['inmune'].append((tipo,mult))
    
    return categorias
    