# Criterios de Evaluacion - Laboratorio de Ciberseguridad

## Puntuacion Total: 100 puntos

---

## 1. Identificacion de vulnerabilidades (15 puntos)

| Criterio | Puntos |
|----------|--------|
| Identificar correctamente cada vulnerabilidad presente | 5 pts |
| Clasificar correctamente la severidad (Alta/Media/Baja) | 5 pts |
| Relacionar con la categoria OWASP Top 10 correspondiente | 5 pts |

**Nota:** Se espera que el estudiante encuentre al menos 4 vulnerabilidades distintas.

---

## 2. Scripts de deteccion y explotacion (15 puntos)

| Criterio | Puntos |
|----------|--------|
| Cada script de deteccion se ejecuta y detecta la vulnerabilidad | 4 pts |
| Cada script de explotacion demuestra el impacto real | 4 pts |
| Los scripts incluyen explicacion paso a paso en comentarios | 4 pts |
| Codigo limpio, con manejo de errores | 3 pts |

---

## 3. Escaner de vulnerabilidades (25 puntos)

| Criterio | Puntos |
|----------|--------|
| Acepta URL base como argumento CLI y funciona correctamente | 4 pts |
| Ejecuta todos los tests de deteccion en secuencia | 4 pts |
| Output con colores en terminal (rojo/amarillo/verde segun severidad) | 4 pts |
| Genera reporte automatico en Markdown con resultados | 4 pts |
| Arquitectura extensible (cada test es una funcion/clase independiente) | 5 pts |
| Manejo robusto de errores (conexion rechazada, timeouts, URLs invalidas) | 4 pts |

---

## 4. WAF - Web Application Firewall (25 puntos)

| Criterio | Puntos |
|----------|--------|
| Funciona como middleware Flask (se inserta sin modificar rutas) | 4 pts |
| Detecta y bloquea intentos de SQL Injection | 4 pts |
| Detecta y bloquea intentos de XSS | 4 pts |
| Detecta y bloquea intentos de Path Traversal | 3 pts |
| Implementa rate limiting por IP | 3 pts |
| Registra intentos bloqueados en archivo de log (JSON) | 3 pts |
| Incluye al menos 5 tests unitarios que demuestren el bloqueo | 4 pts |

---

## 5. Aplicacion parcheada (10 puntos)

| Criterio | Puntos |
|----------|--------|
| Cada vulnerabilidad esta correctamente corregida | 3 pts |
| La aplicacion sigue funcionando despues de los parches | 3 pts |
| El WAF esta integrado como capa de defensa adicional | 2 pts |
| Cada correccion incluye comentario explicando el cambio | 2 pts |

---

## 6. Reporte de seguridad (10 puntos)

| Criterio | Puntos |
|----------|--------|
| Formato profesional y uso de la plantilla proporcionada | 2 pts |
| Descripcion clara de cada vulnerabilidad | 2 pts |
| Pasos de reproduccion detallados y replicables | 2 pts |
| Evidencia incluida (respuestas del servidor, payloads, etc.) | 2 pts |
| Recomendaciones de remediacion claras y correctas | 2 pts |

---

## BONUS: Dashboard de monitoreo (+10 puntos posibles)

| Criterio | Puntos |
|----------|--------|
| Panel web funcional que lee los logs del WAF | +3 pts |
| Muestra log de ataques bloqueados actualizado | +2 pts |
| Graficas de ataques por tipo y/o por IP | +3 pts |
| Estadisticas generales (total bloqueados, tipo mas frecuente) | +2 pts |

---

## Penalizaciones

| Criterio | Penalizacion |
|----------|-------------|
| Scripts que no se ejecutan | -5 pts c/u |
| Parches que rompen funcionalidad | -5 pts c/u |
| WAF que bloquea trafico legitimo (falsos positivos) | -5 pts |
| Reporte incompleto o sin evidencia | -5 pts |
| No seguir la estructura de entrega solicitada | -3 pts |
