"""
assets.py - Caracteres Unicode y constantes de color para el juego.

Define los simbolos visuales para cada tipo de tile, enemigo e item,
asi como los indices de pares de color para curses.
"""

import curses

# --- Tiles del mapa ---
TILES = {
    "wall": "#",
    "floor": ".",
    "corridor": ".",
    "door": "+",
    "stairs": ">",
    "player": "@",
}

# --- Caracteres de enemigos ---
ENEMY_CHARS = {
    "goblin": "g",
    "skeleton": "s",
    "dragon": "D",
}

# --- Caracteres de items ---
ITEM_CHARS = {
    "potion": "!",
    "sword": "/",
    "shield": "[",
}

# --- Indices de pares de color para curses ---
# Se inicializan en init_colors()
COLOR_PAIRS = {
    "wall": 1,
    "floor": 2,
    "corridor": 3,
    "door": 4,
    "stairs": 5,
    "player": 6,
    "enemy": 7,
    "item": 8,
    "status_bar": 9,
    "hp_good": 10,
    "hp_low": 11,
}


def init_colors():
    """Inicializa los pares de color de curses. Llamar despues de curses.start_color()."""
    curses.start_color()
    curses.use_default_colors()

    # Par 1: Muros - gris sobre negro
    curses.init_pair(COLOR_PAIRS["wall"], curses.COLOR_WHITE, -1)
    # Par 2: Suelo - gris oscuro
    curses.init_pair(COLOR_PAIRS["floor"], curses.COLOR_WHITE, -1)
    # Par 3: Corredor - gris
    curses.init_pair(COLOR_PAIRS["corridor"], curses.COLOR_WHITE, -1)
    # Par 4: Puerta - amarillo
    curses.init_pair(COLOR_PAIRS["door"], curses.COLOR_YELLOW, -1)
    # Par 5: Escaleras - cyan
    curses.init_pair(COLOR_PAIRS["stairs"], curses.COLOR_CYAN, -1)
    # Par 6: Jugador - verde brillante
    curses.init_pair(COLOR_PAIRS["player"], curses.COLOR_GREEN, -1)
    # Par 7: Enemigo - rojo
    curses.init_pair(COLOR_PAIRS["enemy"], curses.COLOR_RED, -1)
    # Par 8: Item - magenta
    curses.init_pair(COLOR_PAIRS["item"], curses.COLOR_MAGENTA, -1)
    # Par 9: Barra de estado - blanco sobre azul
    curses.init_pair(COLOR_PAIRS["status_bar"], curses.COLOR_WHITE, curses.COLOR_BLUE)
    # Par 10: HP buena - verde
    curses.init_pair(COLOR_PAIRS["hp_good"], curses.COLOR_GREEN, curses.COLOR_BLUE)
    # Par 11: HP baja - rojo sobre azul
    curses.init_pair(COLOR_PAIRS["hp_low"], curses.COLOR_RED, curses.COLOR_BLUE)
