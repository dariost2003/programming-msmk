"""
map_generator.py - Generador procedural de mazmorras usando BSP.

Genera mazmorras con habitaciones conectadas por corredores
usando el algoritmo Binary Space Partition (BSP).

Valores del grid:
    0 = muro
    1 = suelo (habitacion)
    2 = corredor
    3 = puerta
    4 = escaleras (bajada al siguiente piso)
"""

import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Room:
    """Representa una habitacion rectangular en la mazmorra."""
    x: int
    y: int
    width: int
    height: int

    @property
    def center(self) -> Tuple[int, int]:
        """Retorna el centro de la habitacion."""
        return (self.x + self.width // 2, self.y + self.height // 2)

    @property
    def inner(self) -> Tuple[int, int, int, int]:
        """Retorna las coordenadas interiores (sin muros)."""
        return (self.x + 1, self.y + 1, self.x + self.width - 1, self.y + self.height - 1)


@dataclass
class BSPNode:
    """Nodo del arbol BSP para la generacion de mazmorras."""
    x: int
    y: int
    width: int
    height: int
    left: Optional['BSPNode'] = None
    right: Optional['BSPNode'] = None
    room: Optional[Room] = None


class DungeonGenerator:
    """
    Generador de mazmorras usando Binary Space Partition.

    Parametros:
        width: Ancho del mapa en tiles
        height: Alto del mapa en tiles
        min_room_size: Tamano minimo de una habitacion
        seed: Semilla para el generador aleatorio (opcional, para reproducibilidad)
    """

    def __init__(self, width: int = 80, height: int = 24,
                 min_room_size: int = 5, seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.min_room_size = min_room_size
        self.seed = seed

        # El grid de la mazmorra (0=muro por defecto)
        self.grid: List[List[int]] = []
        # Lista de habitaciones generadas
        self.rooms: List[Room] = []
        # Posicion inicial del jugador
        self.start_pos: Tuple[int, int] = (0, 0)
        # Posicion de las escaleras (salida)
        self.exit_pos: Tuple[int, int] = (0, 0)

    def generate(self) -> List[List[int]]:
        """
        Genera una mazmorra completa y retorna el grid.

        Retorna:
            Grid 2D donde cada celda es un entero (0-4)
        """
        # Inicializar semilla si se proporciono
        if self.seed is not None:
            random.seed(self.seed)

        # Inicializar grid con muros
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []

        # Crear arbol BSP
        root = BSPNode(0, 0, self.width, self.height)
        self._split(root, depth=0)

        # Crear habitaciones en las hojas del arbol
        self._create_rooms(root)

        # Conectar habitaciones con corredores
        self._connect_rooms(root)

        # Colocar puertas en las entradas de habitaciones
        self._place_doors()

        # Colocar inicio y salida
        self._place_start_and_exit()

        return self.grid

    def _split(self, node: BSPNode, depth: int) -> None:
        """Divide recursivamente un nodo BSP en dos subnodos."""
        # Limitar profundidad para obtener 5-8 habitaciones
        max_depth = 4
        if depth >= max_depth:
            return

        # Determinar si dividir horizontal o verticalmente
        # Preferir dividir en la dimension mas larga
        if node.width > node.height:
            split_horizontal = False
        elif node.height > node.width:
            split_horizontal = True
        else:
            split_horizontal = random.random() > 0.5

        # Verificar si hay espacio suficiente para dividir
        min_size = self.min_room_size + 2  # Habitacion + muros

        if split_horizontal:
            if node.height < min_size * 2:
                return
            # Punto de division
            split = random.randint(min_size, node.height - min_size)
            node.left = BSPNode(node.x, node.y, node.width, split)
            node.right = BSPNode(node.x, node.y + split, node.width, node.height - split)
        else:
            if node.width < min_size * 2:
                return
            split = random.randint(min_size, node.width - min_size)
            node.left = BSPNode(node.x, node.y, split, node.height)
            node.right = BSPNode(node.x + split, node.y, node.width - split, node.height)

        # Continuar dividiendo recursivamente
        self._split(node.left, depth + 1)
        self._split(node.right, depth + 1)

    def _create_rooms(self, node: BSPNode) -> None:
        """Crea habitaciones en los nodos hoja del arbol BSP."""
        if node.left is not None and node.right is not None:
            # Nodo interno: procesar hijos
            self._create_rooms(node.left)
            self._create_rooms(node.right)
            return

        # Nodo hoja: crear una habitacion
        # Tamano aleatorio dentro del espacio disponible
        room_width = random.randint(
            self.min_room_size,
            max(self.min_room_size, node.width - 2)
        )
        room_height = random.randint(
            self.min_room_size,
            max(self.min_room_size, node.height - 2)
        )

        # Posicion aleatoria dentro del nodo
        room_x = node.x + random.randint(1, max(1, node.width - room_width - 1))
        room_y = node.y + random.randint(1, max(1, node.height - room_height - 1))

        # Asegurar que la habitacion este dentro de los limites
        room_x = max(1, min(room_x, self.width - room_width - 1))
        room_y = max(1, min(room_y, self.height - room_height - 1))
        room_width = min(room_width, self.width - room_x - 1)
        room_height = min(room_height, self.height - room_y - 1)

        room = Room(room_x, room_y, room_width, room_height)
        node.room = room
        self.rooms.append(room)

        # Dibujar la habitacion en el grid
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if 0 <= y < self.height and 0 <= x < self.width:
                    self.grid[y][x] = 1  # Suelo

    def _get_room(self, node: BSPNode) -> Optional[Room]:
        """Obtiene una habitacion de un nodo (busca en hijos si es necesario)."""
        if node.room is not None:
            return node.room
        if node.left is not None:
            left_room = self._get_room(node.left)
            if left_room is not None:
                return left_room
        if node.right is not None:
            right_room = self._get_room(node.right)
            if right_room is not None:
                return right_room
        return None

    def _connect_rooms(self, node: BSPNode) -> None:
        """Conecta las habitaciones de los subnodos con corredores."""
        if node.left is None or node.right is None:
            return

        # Primero conectar las habitaciones de los hijos
        self._connect_rooms(node.left)
        self._connect_rooms(node.right)

        # Obtener una habitacion de cada subarbol
        left_room = self._get_room(node.left)
        right_room = self._get_room(node.right)

        if left_room is None or right_room is None:
            return

        # Conectar los centros de las habitaciones con un corredor en L
        cx1, cy1 = left_room.center
        cx2, cy2 = right_room.center

        # Decidir aleatoriamente si ir horizontal primero o vertical
        if random.random() > 0.5:
            self._carve_h_corridor(cx1, cx2, cy1)
            self._carve_v_corridor(cy1, cy2, cx2)
        else:
            self._carve_v_corridor(cy1, cy2, cx1)
            self._carve_h_corridor(cx1, cx2, cy2)

    def _carve_h_corridor(self, x1: int, x2: int, y: int) -> None:
        """Cava un corredor horizontal."""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                if self.grid[y][x] == 0:  # Solo si es muro
                    self.grid[y][x] = 2  # Corredor

    def _carve_v_corridor(self, y1: int, y2: int, x: int) -> None:
        """Cava un corredor vertical."""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                if self.grid[y][x] == 0:  # Solo si es muro
                    self.grid[y][x] = 2  # Corredor

    def _place_doors(self) -> None:
        """Coloca puertas donde los corredores se encuentran con las habitaciones."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] != 2:  # Solo en corredores
                    continue

                # Verificar si este corredor esta adyacente a una habitacion
                adjacent_floor = False
                adjacent_wall = False

                # Revisar si hay un patron de puerta (corredor entre muro y suelo)
                # Patron horizontal: muro-corredor-suelo o suelo-corredor-muro
                if (self.grid[y][x - 1] == 1 and self.grid[y][x + 1] == 0) or \
                   (self.grid[y][x - 1] == 0 and self.grid[y][x + 1] == 1):
                    if self.grid[y - 1][x] == 0 or self.grid[y + 1][x] == 0:
                        self.grid[y][x] = 3  # Puerta
                        continue

                # Patron vertical
                if (self.grid[y - 1][x] == 1 and self.grid[y + 1][x] == 0) or \
                   (self.grid[y - 1][x] == 0 and self.grid[y + 1][x] == 1):
                    if self.grid[y][x - 1] == 0 or self.grid[y][x + 1] == 0:
                        self.grid[y][x] = 3  # Puerta
                        continue

    def _place_start_and_exit(self) -> None:
        """Coloca la posicion inicial y las escaleras de salida."""
        if len(self.rooms) < 2:
            # Si hay muy pocas habitaciones, usar la primera
            if self.rooms:
                self.start_pos = self.rooms[0].center
                self.exit_pos = self.rooms[0].center
            return

        # El jugador empieza en la primera habitacion
        self.start_pos = self.rooms[0].center

        # Las escaleras estan en la habitacion mas lejana
        max_dist = 0
        exit_room = self.rooms[-1]
        sx, sy = self.start_pos

        for room in self.rooms[1:]:
            cx, cy = room.center
            dist = abs(cx - sx) + abs(cy - sy)  # Distancia Manhattan
            if dist > max_dist:
                max_dist = dist
                exit_room = room

        ex, ey = exit_room.center
        self.exit_pos = (ex, ey)
        # Marcar las escaleras en el grid
        if 0 <= ey < self.height and 0 <= ex < self.width:
            self.grid[ey][ex] = 4

    def get_floor_positions(self) -> List[Tuple[int, int]]:
        """
        Retorna todas las posiciones de suelo disponibles.
        Util para colocar enemigos e items.
        """
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:  # Solo suelo de habitaciones
                    # No incluir inicio ni salida
                    if (x, y) != self.start_pos and (x, y) != self.exit_pos:
                        positions.append((x, y))
        return positions
