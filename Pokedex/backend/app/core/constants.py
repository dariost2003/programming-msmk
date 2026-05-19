# Dominio Pokemon

SUPPORTED_LANGUAGES = ['es', 'en']

INTERACTIONS_DATESET = {
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


COLORS_TYPE_POKEMON = {
    'fire':'#ff421c','water':'#2c9be3',
    'grass':'#78cc55', 'electric':'#ffd333',
    'ice':'#7ac7ff', 'fighting':'#bb5544', 
    'poison':'#aa5599', 'ground':'#ddbb55',
    'flying':'#8899ff','psychic':'#ff5599',
    'bug':'#aabb22', 'rock':'#bbaa66',
    'ghost':'#6666bb', 'dragon':'#7766ee',
    'dark':'#775544', 'steel':'#aaaabb',
    'fairy':'#ee99ee', 'normal':'#aaaa99'
}
