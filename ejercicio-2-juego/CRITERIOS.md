# Criterios de Evaluacion - Dungeon Crawler

## Puntuacion total: 100 puntos

---

## Tarea 1: Sistema de combate (25 puntos)

| Criterio | Puntos |
|----------|--------|
| El jugador puede atacar enemigos al moverse hacia ellos | 5 |
| La formula de dano funciona correctamente | 5 |
| Los enemigos muertos se eliminan del mapa | 3 |
| El jugador recibe XP por eliminar enemigos | 3 |
| Se muestran mensajes de combate claros | 4 |
| El juego termina si el jugador muere | 3 |
| El codigo es limpio y esta bien documentado | 2 |

## Tarea 2: Sistema de inventario (20 puntos)

| Criterio | Puntos |
|----------|--------|
| El jugador puede recoger items del suelo | 4 |
| Los items recogidos se almacenan en un inventario | 3 |
| Se puede ver el inventario con una tecla | 3 |
| Se pueden usar items del inventario | 4 |
| Las pociones restauran HP correctamente | 2 |
| Las armas/escudos modifican estadisticas | 2 |
| El codigo es limpio y esta bien documentado | 2 |

## Tarea 3: IA de enemigos (20 puntos)

| Criterio | Puntos |
|----------|--------|
| Los enemigos se mueven despues del turno del jugador | 4 |
| Comportamiento "patrol": movimiento aleatorio funcional | 4 |
| Comportamiento "chase": persecucion al jugador | 5 |
| Los enemigos respetan colisiones (muros, otros enemigos) | 3 |
| Los enemigos pueden atacar al jugador | 2 |
| El codigo es limpio y esta bien documentado | 2 |

## Tarea 4: Sistema de puntuacion (15 puntos)

| Criterio | Puntos |
|----------|--------|
| Se acumulan puntos por diferentes acciones | 4 |
| Los puntajes se guardan en un archivo JSON | 4 |
| Se muestra tabla de mejores puntajes al terminar | 3 |
| El puntaje actual se muestra durante el juego | 2 |
| El codigo es limpio y esta bien documentado | 2 |

## Tarea 5: Progresion de pisos (20 puntos)

| Criterio | Puntos |
|----------|--------|
| Las escaleras generan un nuevo piso al ser pisadas | 5 |
| La dificultad aumenta con cada piso | 4 |
| El numero de piso se muestra en la interfaz | 2 |
| Aparecen dragones en pisos avanzados | 3 |
| Los items mejoran en pisos profundos | 3 |
| La transicion entre pisos es fluida (sin errores) | 1 |
| El codigo es limpio y esta bien documentado | 2 |

---

## Bonificaciones (hasta +10 puntos extra)

| Criterio | Puntos |
|----------|--------|
| Efectos de sonido o animaciones en terminal | +3 |
| Sistema de niveles del jugador (subir de nivel con XP) | +3 |
| Minimap o mapa revelable (fog of war) | +4 |
| Sistema de guardado/carga de partida | +3 |
| Trampas u objetos interactivos en el mapa | +2 |

*Nota: La bonificacion maxima es +10 puntos aunque la suma de los extras supere ese valor.*

---

## Penalizaciones

| Criterio | Descuento |
|----------|-----------|
| El juego no ejecuta sin errores | -10 |
| Codigo sin comentarios ni documentacion | -5 |
| Uso de bibliotecas externas no autorizadas | -5 |
| Codigo copiado de otro estudiante | -100 |
| Variables o funciones con nombres no descriptivos | -3 |
| No manejar errores basicos (division por cero, indices fuera de rango) | -3 |

---

## Notas importantes

- Cada tarea se evalua de forma independiente. No es necesario completar todas.
- Se valora la calidad del codigo tanto como la funcionalidad.
- Documenta tus decisiones de diseno con comentarios.
- Si implementas algo diferente a lo pedido, explica por que en un comentario.
- Pueden trabajar de forma individual o en parejas.
- Fecha de entrega: consultar con el profesor.
