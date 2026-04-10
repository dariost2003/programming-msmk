"""
engine.py - Motor principal del juego.

Contiene la clase Game con el bucle principal:
    entrada -> actualizacion -> renderizado

Maneja la entrada del usuario, movimiento del jugador,
deteccion de colisiones y renderizado del mapa con curses.
"""

import curses
from typing import List, Optional
from assets import TILES, COLOR_PAIRS, init_colors
from entities import Entity, Player, Enemy, Item


class Game:
    """
    Motor principal del dungeon crawler.

    Atributos:
        grid: Mapa de la mazmorra (grid 2D de enteros)
        player: El jugador
        enemies: Lista de enemigos en el mapa
        items: Lista de items en el mapa
        messages: Cola de mensajes para mostrar al jugador
        running: Indica si el juego sigue ejecutandose
        turns: Contador de turnos
    """

    def __init__(self, grid: List[List[int]], player: Player,
                 enemies: List[Enemy] = None, items: List[Item] = None):
        self.grid = grid
        self.map_height = len(grid)
        self.map_width = len(grid[0]) if grid else 0
        self.player = player
        self.enemies = enemies or []
        self.items = items or []
        self.messages: List[str] = ["Bienvenido a la mazmorra. Usa WASD o flechas para moverte."]
        self.running = True
        self.turns = 0
        # Desplazamiento de la camara (para mapas mas grandes que la terminal)
        self.camera_x = 0
        self.camera_y = 0

    def run(self, stdscr) -> dict:
        """
        Ejecuta el bucle principal del juego.

        Parametros:
            stdscr: Ventana principal de curses

        Retorna:
            Diccionario con estadisticas finales del juego
        """
        # Configurar curses
        self._setup_curses(stdscr)

        # Bucle principal del juego
        while self.running:
            # Actualizar camara
            self._update_camera(stdscr)

            # Renderizar
            self._render(stdscr)

            # Entrada del usuario
            key = stdscr.getch()

            # Procesar entrada
            self._handle_input(key)

        # Retornar estadisticas finales
        return {
            "turns": self.turns,
            "hp": self.player.hp,
            "level": self.player.level,
            "xp": self.player.xp,
        }

    def _setup_curses(self, stdscr) -> None:
        """Configura curses para el juego."""
        curses.curs_set(0)  # Ocultar cursor
        stdscr.nodelay(False)  # Esperar entrada (juego por turnos)
        stdscr.keypad(True)  # Habilitar teclas especiales
        init_colors()

    def _handle_input(self, key: int) -> None:
        """
        Procesa la entrada del teclado.

        Teclas soportadas:
            WASD / Flechas: Movimiento
            Q: Salir del juego
        """
        dx, dy = 0, 0

        # Movimiento
        if key in (ord('w'), ord('W'), curses.KEY_UP):
            dy = -1
        elif key in (ord('s'), ord('S'), curses.KEY_DOWN):
            dy = 1
        elif key in (ord('a'), ord('A'), curses.KEY_LEFT):
            dx = -1
        elif key in (ord('d'), ord('D'), curses.KEY_RIGHT):
            dx = 1
        elif key in (ord('q'), ord('Q')):
            self.running = False
            return
        else:
            return  # Tecla no reconocida, no hacer nada

        # Intentar mover al jugador
        self._move_player(dx, dy)

        # Incrementar turno
        self.turns += 1

        # TODO: Aqui los estudiantes pueden agregar:
        # - Turno de los enemigos (movimiento, IA)
        # - Verificar combate
        # - Verificar items recogidos
        # - Verificar si el jugador llego a las escaleras

    def _move_player(self, dx: int, dy: int) -> None:
        """
        Mueve al jugador si la posicion destino es transitable.

        Parametros:
            dx: Desplazamiento en X (-1, 0, 1)
            dy: Desplazamiento en Y (-1, 0, 1)
        """
        new_x = self.player.x + dx
        new_y = self.player.y + dy

        # Verificar limites del mapa
        if not (0 <= new_x < self.map_width and 0 <= new_y < self.map_height):
            return

        # Verificar colision con muros
        tile = self.grid[new_y][new_x]
        if tile == 0:  # Muro
            return

        # TODO: Aqui los estudiantes pueden agregar:
        # - Colision con enemigos (iniciar combate)
        # - Recoger items
        # - Detectar escaleras (cambio de piso)

        # Verificar si hay un enemigo en la posicion destino
        for enemy in self.enemies:
            if enemy.x == new_x and enemy.y == new_y:
                # Por ahora solo mostrar mensaje (estudiantes implementaran combate)
                self.messages.append(f"Ves un {enemy.name} amenazante!")
                return

        # Mover al jugador
        self.player.x = new_x
        self.player.y = new_y

        # Verificar escaleras
        if tile == 4:
            self.messages.append("Has encontrado las escaleras! (Progresion pendiente)")

        # Verificar puerta
        if tile == 3:
            self.messages.append("Abres una puerta...")

    def _update_camera(self, stdscr) -> None:
        """Actualiza la posicion de la camara para centrar al jugador."""
        max_y, max_x = stdscr.getmaxyx()
        # Reservar espacio para la barra de estado (2 lineas abajo)
        view_height = max_y - 2
        view_width = max_x

        # Centrar la camara en el jugador
        self.camera_x = self.player.x - view_width // 2
        self.camera_y = self.player.y - view_height // 2

        # Limitar la camara a los bordes del mapa
        self.camera_x = max(0, min(self.camera_x, self.map_width - view_width))
        self.camera_y = max(0, min(self.camera_y, self.map_height - view_height))

    def _render(self, stdscr) -> None:
        """Renderiza el mapa, entidades y la barra de estado."""
        try:
            stdscr.erase()
            max_y, max_x = stdscr.getmaxyx()

            # Verificar tamano minimo de terminal
            if max_y < 5 or max_x < 20:
                stdscr.addstr(0, 0, "Terminal muy pequena!")
                stdscr.refresh()
                return

            view_height = max_y - 2  # Reservar 2 lineas para barra de estado

            # Dibujar el mapa
            self._render_map(stdscr, view_height, max_x)

            # Dibujar enemigos
            self._render_entities(stdscr, self.enemies, view_height, max_x)

            # Dibujar items
            self._render_entities(stdscr, self.items, view_height, max_x)

            # Dibujar al jugador
            self._render_player(stdscr, view_height, max_x)

            # Dibujar barra de estado
            self._render_status_bar(stdscr, max_y, max_x)

            stdscr.refresh()
        except curses.error:
            # Ignorar errores de curses (ej: terminal redimensionada)
            pass

    def _render_map(self, stdscr, view_height: int, view_width: int) -> None:
        """Dibuja los tiles del mapa visibles."""
        tile_chars = {
            0: (TILES["wall"], COLOR_PAIRS["wall"], curses.A_DIM),
            1: (TILES["floor"], COLOR_PAIRS["floor"], curses.A_DIM),
            2: (TILES["corridor"], COLOR_PAIRS["corridor"], curses.A_DIM),
            3: (TILES["door"], COLOR_PAIRS["door"], curses.A_BOLD),
            4: (TILES["stairs"], COLOR_PAIRS["stairs"], curses.A_BOLD),
        }

        for screen_y in range(min(view_height, self.map_height)):
            map_y = screen_y + self.camera_y
            if map_y < 0 or map_y >= self.map_height:
                continue

            for screen_x in range(min(view_width, self.map_width)):
                map_x = screen_x + self.camera_x
                if map_x < 0 or map_x >= self.map_width:
                    continue

                tile = self.grid[map_y][map_x]
                char, color_idx, attr = tile_chars.get(tile, (" ", 1, 0))

                try:
                    stdscr.addch(
                        screen_y, screen_x,
                        char,
                        curses.color_pair(color_idx) | attr
                    )
                except curses.error:
                    pass

    def _render_entities(self, stdscr, entities: List[Entity],
                         view_height: int, view_width: int) -> None:
        """Dibuja una lista de entidades en el mapa."""
        for entity in entities:
            screen_x = entity.x - self.camera_x
            screen_y = entity.y - self.camera_y

            if 0 <= screen_x < view_width and 0 <= screen_y < view_height:
                color_idx = COLOR_PAIRS.get(entity.color, 1)
                try:
                    stdscr.addch(
                        screen_y, screen_x,
                        entity.char,
                        curses.color_pair(color_idx) | curses.A_BOLD
                    )
                except curses.error:
                    pass

    def _render_player(self, stdscr, view_height: int, view_width: int) -> None:
        """Dibuja al jugador en el mapa."""
        screen_x = self.player.x - self.camera_x
        screen_y = self.player.y - self.camera_y

        if 0 <= screen_x < view_width and 0 <= screen_y < view_height:
            try:
                stdscr.addch(
                    screen_y, screen_x,
                    self.player.char,
                    curses.color_pair(COLOR_PAIRS["player"]) | curses.A_BOLD
                )
            except curses.error:
                pass

    def _render_status_bar(self, stdscr, max_y: int, max_x: int) -> None:
        """Dibuja la barra de estado en las ultimas 2 lineas."""
        status_y = max_y - 2

        # --- Linea 1: Informacion del jugador ---
        hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp > 0 else 0
        hp_color = COLOR_PAIRS["hp_good"] if hp_ratio > 0.3 else COLOR_PAIRS["hp_low"]

        # Fondo de la barra de estado
        status_line = " " * (max_x - 1)
        try:
            stdscr.addstr(status_y, 0, status_line,
                          curses.color_pair(COLOR_PAIRS["status_bar"]))
        except curses.error:
            pass

        # Nombre y nivel
        info = f" {self.player.name} | Nv.{self.player.level} "
        try:
            stdscr.addstr(status_y, 0, info,
                          curses.color_pair(COLOR_PAIRS["status_bar"]) | curses.A_BOLD)
        except curses.error:
            pass

        # HP
        hp_text = f"HP: {self.player.hp}/{self.player.max_hp}"
        hp_pos = len(info)
        try:
            stdscr.addstr(status_y, hp_pos, hp_text,
                          curses.color_pair(hp_color) | curses.A_BOLD)
        except curses.error:
            pass

        # Posicion y turno
        pos_text = f" | Pos:({self.player.x},{self.player.y}) | Turno:{self.turns} "
        pos_start = hp_pos + len(hp_text)
        try:
            stdscr.addstr(status_y, pos_start, pos_text,
                          curses.color_pair(COLOR_PAIRS["status_bar"]))
        except curses.error:
            pass

        # XP
        xp_text = f" | XP:{self.player.xp} "
        xp_start = pos_start + len(pos_text)
        try:
            stdscr.addstr(status_y, xp_start, xp_text,
                          curses.color_pair(COLOR_PAIRS["status_bar"]))
        except curses.error:
            pass

        # --- Linea 2: Ultimo mensaje ---
        msg_y = max_y - 1
        msg_line = " " * (max_x - 1)
        try:
            stdscr.addstr(msg_y, 0, msg_line,
                          curses.color_pair(COLOR_PAIRS["status_bar"]))
        except curses.error:
            pass

        if self.messages:
            # Mostrar el ultimo mensaje
            last_msg = self.messages[-1]
            # Truncar si es muy largo
            if len(last_msg) > max_x - 2:
                last_msg = last_msg[:max_x - 5] + "..."
            try:
                stdscr.addstr(msg_y, 1, last_msg,
                              curses.color_pair(COLOR_PAIRS["status_bar"]))
            except curses.error:
                pass
