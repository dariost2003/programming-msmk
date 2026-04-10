# Ejercicio 2: Dungeon Crawler en Terminal

## Descripcion

Un roguelike simplificado (dungeon crawler) jugable directamente en la terminal.
El jugador explora una mazmorra generada proceduralmente, se mueve por habitaciones
conectadas con corredores y encuentra enemigos e items.

El juego usa `curses` para renderizar graficos ASCII con colores en la terminal.

## Que esta incluido (codigo base)

- **Bucle de juego** completo: entrada -> actualizacion -> renderizado
- **Generador de mazmorras** procedural usando BSP (Binary Space Partition)
- **Sistema de entidades**: jugador, enemigos e items con atributos
- **Renderizado con colores**: mapa, entidades y barra de estado
- **Movimiento del jugador** con deteccion de colisiones (no puede atravesar muros)
- **Camara** que sigue al jugador (para mapas grandes)
- **Barra de estado** con HP, posicion, nivel y mensajes

## Como ejecutar

```bash
cd ejercicio-2-juego
python main.py
```

Para generar siempre la misma mazmorra (util para depurar):

```bash
python main.py 42
```

El numero es la semilla del generador aleatorio.

## Controles

| Tecla | Accion |
|-------|--------|
| `W` / Flecha arriba | Mover arriba |
| `S` / Flecha abajo | Mover abajo |
| `A` / Flecha izquierda | Mover izquierda |
| `D` / Flecha derecha | Mover derecha |
| `Q` | Salir del juego |

## Simbolos en el mapa

| Simbolo | Significado |
|---------|-------------|
| `@` | Tu personaje |
| `#` | Muro |
| `.` | Suelo / corredor |
| `+` | Puerta |
| `>` | Escaleras (bajada) |
| `g` | Goblin |
| `s` | Esqueleto |
| `D` | Dragon |
| `!` | Pocion |
| `/` | Espada |
| `[` | Escudo |

## Tareas para el estudiante

### Tarea 1: Sistema de combate

Implementar combate cuerpo a cuerpo entre el jugador y los enemigos.

**Donde modificar:** `engine.py` (metodo `_move_player` y nuevo metodo de combate)

- Cuando el jugador intenta moverse a una casilla con un enemigo, se inicia combate
- Formula de dano: `max(1, atacante.attack - defensor.defense)`
- Mostrar mensajes de combate en la barra de estado
- Eliminar enemigos muertos (hp <= 0) de la lista
- Dar XP al jugador por eliminar enemigos
- Si el jugador muere (hp <= 0), terminar el juego

**Tips:**
- Revisa el metodo `_move_player` donde dice `TODO`
- Crea un metodo `_combat(self, enemy)` en la clase `Game`
- Usa `self.messages.append()` para mostrar mensajes

### Tarea 2: Sistema de inventario

Implementar recoleccion y uso de items.

**Donde modificar:** `engine.py` y `entities.py`

- El jugador puede recoger items al caminar sobre ellos
- Agregar una lista `inventory` al jugador
- Tecla `I` para ver inventario, `U` para usar item
- Las pociones restauran HP
- Las espadas aumentan el ataque
- Los escudos aumentan la defensa

**Tips:**
- Agrega el atributo `inventory: list = field(default_factory=list)` a `Player`
- En `_move_player`, verifica si hay un item en la nueva posicion
- Crea metodos `_show_inventory` y `_use_item` en `Game`

### Tarea 3: IA de enemigos

Hacer que los enemigos se muevan y persigan al jugador.

**Donde modificar:** `engine.py` (nuevo metodo para turno de enemigos)

- Los enemigos se mueven despues del turno del jugador
- Comportamiento "idle": no se mueve
- Comportamiento "patrol": movimiento aleatorio
- Comportamiento "chase": perseguir al jugador si esta cerca (distancia < 6)
- Los enemigos no pueden atravesar muros ni otros enemigos

**Tips:**
- Crea un metodo `_enemy_turn(self)` que se llame al final de `_handle_input`
- Para "chase", calcula la distancia Manhattan al jugador
- Mueve al enemigo un paso en la direccion del jugador
- Usa el campo `behavior` de `Enemy`

### Tarea 4: Sistema de puntuacion

Implementar un sistema de puntos y tabla de mejores puntajes.

**Donde modificar:** `main.py` y `engine.py`

- Puntos por: eliminar enemigos, recoger items, bajar pisos, turnos sobrevividos
- Guardar mejores puntajes en un archivo JSON (`scores.json`)
- Mostrar tabla de puntajes al terminar el juego
- Mostrar puntaje actual en la barra de estado

**Tips:**
- Usa el modulo `json` para leer/escribir el archivo de puntajes
- Agrega un atributo `score` a `Game`
- Incrementa el score en los eventos relevantes
- Crea funciones `save_score()` y `load_scores()` en `main.py`

### Tarea 5: Progresion de pisos

Implementar multiples pisos de mazmorra con dificultad creciente.

**Donde modificar:** `engine.py`, `main.py`

- Al pisar las escaleras (`>`), generar un nuevo piso
- Cada piso tiene mas enemigos y enemigos mas fuertes
- El piso actual se muestra en la barra de estado
- A partir del piso 3, pueden aparecer dragones
- Los items de pisos profundos son mejores

**Tips:**
- Crea un metodo `_next_floor(self)` en `Game`
- Usa `DungeonGenerator` para generar un nuevo mapa
- Escala las estadisticas de enemigos con el numero de piso
- Recuerda actualizar `self.grid`, `self.enemies`, `self.items`

## Estructura del proyecto

```
ejercicio-2-juego/
    main.py           # Punto de entrada
    engine.py         # Motor del juego (bucle principal)
    map_generator.py  # Generador de mazmorras BSP
    entities.py       # Clases de entidades
    assets.py         # Caracteres y colores
    requirements.txt  # Dependencias (solo stdlib)
    README.md         # Este archivo
    CRITERIOS.md      # Rubrica de evaluacion
```

## Requisitos del sistema

- Python 3.8 o superior
- Terminal que soporte curses (macOS, Linux)
- En Windows: instalar `windows-curses` con `pip install windows-curses`
- Terminal de al menos 80x24 caracteres
