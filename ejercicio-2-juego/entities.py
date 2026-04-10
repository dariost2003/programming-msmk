"""
entities.py - Clases base para entidades del juego.

Define las clases Entity, Player, Enemy e Item con sus atributos,
y funciones de fabrica para crear instancias facilmente.
"""

from dataclasses import dataclass, field
from assets import TILES, ENEMY_CHARS, ITEM_CHARS


# --- Clase base ---

@dataclass
class Entity:
    """Entidad base del juego con posicion y representacion visual."""
    x: int
    y: int
    char: str
    color: str  # Clave en COLOR_PAIRS de assets.py
    name: str


# --- Jugador ---

@dataclass
class Player(Entity):
    """El jugador controlado por el usuario."""
    hp: int = 20
    max_hp: int = 20
    attack: int = 5
    defense: int = 2
    level: int = 1
    xp: int = 0


# --- Enemigo ---

@dataclass
class Enemy(Entity):
    """Un enemigo en la mazmorra."""
    hp: int = 10
    max_hp: int = 10
    attack: int = 3
    defense: int = 1
    enemy_type: str = "goblin"
    # Comportamiento del enemigo (placeholder para que los estudiantes lo implementen)
    # Valores posibles: "idle", "patrol", "chase", "flee"
    behavior: str = "idle"


# --- Item ---

@dataclass
class Item(Entity):
    """Un objeto que el jugador puede recoger."""
    item_type: str = "potion"
    # Valor del efecto (placeholder para que los estudiantes lo implementen)
    # Ejemplo: pocion restaura effect_value HP, espada da effect_value de ataque
    effect_value: int = 5


# --- Estadisticas de enemigos por tipo ---

ENEMY_STATS = {
    "goblin": {"hp": 8, "attack": 3, "defense": 1, "name": "Goblin"},
    "skeleton": {"hp": 12, "attack": 4, "defense": 2, "name": "Esqueleto"},
    "dragon": {"hp": 50, "attack": 10, "defense": 5, "name": "Dragon"},
}

# --- Estadisticas de items por tipo ---

ITEM_STATS = {
    "potion": {"name": "Pocion de vida", "effect_value": 10},
    "sword": {"name": "Espada", "effect_value": 3},
    "shield": {"name": "Escudo", "effect_value": 2},
}


# --- Funciones de fabrica ---

def create_player(x: int = 0, y: int = 0) -> Player:
    """Crea un jugador en la posicion dada."""
    return Player(
        x=x,
        y=y,
        char=TILES["player"],
        color="player",
        name="Heroe",
    )


def create_enemy(enemy_type: str, x: int, y: int) -> Enemy:
    """
    Crea un enemigo del tipo dado en la posicion (x, y).

    Tipos validos: 'goblin', 'skeleton', 'dragon'
    """
    stats = ENEMY_STATS.get(enemy_type, ENEMY_STATS["goblin"])
    char = ENEMY_CHARS.get(enemy_type, "?")

    return Enemy(
        x=x,
        y=y,
        char=char,
        color="enemy",
        name=stats["name"],
        hp=stats["hp"],
        max_hp=stats["hp"],
        attack=stats["attack"],
        defense=stats["defense"],
        enemy_type=enemy_type,
        behavior="idle",
    )


def create_item(item_type: str, x: int, y: int) -> Item:
    """
    Crea un item del tipo dado en la posicion (x, y).

    Tipos validos: 'potion', 'sword', 'shield'
    """
    stats = ITEM_STATS.get(item_type, ITEM_STATS["potion"])
    char = ITEM_CHARS.get(item_type, "?")

    return Item(
        x=x,
        y=y,
        char=char,
        color="item",
        name=stats["name"],
        item_type=item_type,
        effect_value=stats["effect_value"],
    )
