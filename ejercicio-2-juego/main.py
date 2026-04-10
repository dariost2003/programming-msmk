#!/usr/bin/env python3
"""
main.py - Punto de entrada del Dungeon Crawler.

Inicializa curses, genera la mazmorra, crea las entidades
y ejecuta el bucle principal del juego.

Ejecutar con: python main.py
"""

import curses
import random
import sys

from map_generator import DungeonGenerator
from entities import create_player, create_enemy, create_item
from engine import Game


def setup_game(seed=None):
    """
    Configura el juego: genera la mazmorra y coloca entidades.

    Parametros:
        seed: Semilla para generacion procedural (opcional)

    Retorna:
        Instancia de Game lista para ejecutar
    """
    # Generar la mazmorra
    generator = DungeonGenerator(width=80, height=40, min_room_size=5, seed=seed)
    grid = generator.generate()

    # Crear al jugador en la posicion inicial
    start_x, start_y = generator.start_pos
    player = create_player(x=start_x, y=start_y)

    # Obtener posiciones disponibles para colocar entidades
    available_positions = generator.get_floor_positions()
    if seed is not None:
        random.seed(seed + 1)  # Semilla diferente para las entidades
    random.shuffle(available_positions)

    # Colocar enemigos (uno por habitacion, excepto la primera)
    enemies = []
    enemy_types = ["goblin", "goblin", "skeleton", "goblin", "skeleton"]
    positions_used = 0

    for i, enemy_type in enumerate(enemy_types):
        if positions_used < len(available_positions):
            ex, ey = available_positions[positions_used]
            enemies.append(create_enemy(enemy_type, ex, ey))
            positions_used += 1

    # Colocar items
    items = []
    item_types = ["potion", "potion", "sword"]

    for item_type in item_types:
        if positions_used < len(available_positions):
            ix, iy = available_positions[positions_used]
            items.append(create_item(item_type, ix, iy))
            positions_used += 1

    # Crear el juego
    game = Game(grid=grid, player=player, enemies=enemies, items=items)
    return game


def main(stdscr):
    """Funcion principal que se ejecuta dentro del wrapper de curses."""
    # Usar semilla de los argumentos o None para aleatorio
    seed = None
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            pass

    # Configurar y ejecutar el juego
    game = setup_game(seed=seed)
    stats = game.run(stdscr)

    return stats


if __name__ == "__main__":
    # curses.wrapper se encarga de inicializar y limpiar curses
    try:
        stats = curses.wrapper(main)

        # Mostrar mensaje de despedida
        print("\n" + "=" * 40)
        print("  Gracias por jugar!")
        print("=" * 40)
        print(f"  Turnos jugados: {stats['turns']}")
        print(f"  HP final: {stats['hp']}")
        print(f"  Nivel: {stats['level']}")
        print(f"  Experiencia: {stats['xp']}")
        print("=" * 40 + "\n")

    except KeyboardInterrupt:
        print("\nJuego interrumpido. Hasta pronto!")
    except Exception as e:
        # Asegurar que la terminal se restaure
        print(f"\nError: {e}")
        print("Si la terminal se ve rara, ejecuta: reset")
