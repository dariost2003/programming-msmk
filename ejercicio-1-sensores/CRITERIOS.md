# Criterios de Evaluacion - Ejercicio 1: Dashboard de Sensores Industriales

**Total: 100 puntos**

---

## Tarea 1: Vista multi-sensor (20 puntos)

| Criterio | Puntos |
|---|---|
| Los 4 sensores se muestran simultaneamente con graficos de linea | 6 |
| Cada grafico incluye lineas de umbral min/max claramente visibles | 4 |
| Se muestran metricas resumidas (promedio, min, max, std) por sensor | 6 |
| Los graficos son interactivos (zoom, hover con valores) | 2 |
| Presentacion visual clara y organizada (layout, titulos, etiquetas) | 2 |

---

## Tarea 2: Sistema de alertas (20 puntos)

| Criterio | Puntos |
|---|---|
| Deteccion correcta de valores fuera de umbral | 6 |
| Clasificacion adecuada entre "warning" y "critical" | 4 |
| Panel lateral con alertas recientes (al menos ultimas 20) | 4 |
| Contador de alertas por sensor | 3 |
| Contador de alertas por severidad | 3 |

---

## Tarea 3: Controles interactivos (20 puntos)

| Criterio | Puntos |
|---|---|
| Selector de rango de fechas funcional que filtra los datos | 5 |
| Sliders para ajustar umbrales en tiempo real | 5 |
| Control de factor de calibracion por sensor | 5 |
| Selector de frecuencia de muestreo funcional | 3 |
| Los graficos y alertas se actualizan correctamente al cambiar controles | 2 |

---

## Tarea 4: Analisis estadistico (20 puntos)

| Criterio | Puntos |
|---|---|
| Tabla de estadisticas descriptivas por sensor | 4 |
| Valores anomalos resaltados visualmente en los graficos | 5 |
| Media movil configurable (el usuario elige tamano de ventana) | 5 |
| Matriz o grafico de correlacion entre sensores | 4 |
| Interpretacion o explicacion de los resultados mostrados | 2 |

---

## Tarea 5: Simulacion en tiempo real (20 puntos)

| Criterio | Puntos |
|---|---|
| Uso correcto de `SensorSimulator` para alimentar datos | 5 |
| Boton de inicio/pausa funcional | 4 |
| Indicador de progreso de la simulacion | 3 |
| Los graficos se actualizan con nuevas lecturas en tiempo real | 5 |
| Las alertas se generan en tiempo real durante la simulacion | 3 |

---

## Bonificaciones (hasta +10 puntos extra)

| Criterio | Puntos |
|---|---|
| Exportar datos filtrados o alertas a CSV | +3 |
| Tema visual personalizado (colores, estilos coherentes) | +2 |
| Manejo robusto de errores y casos borde | +2 |
| Documentacion del codigo (docstrings, comentarios claros) | +3 |

---

## Penalizaciones

| Criterio | Penalizacion |
|---|---|
| El codigo no ejecuta sin errores | -10 |
| No se usan las clases de `models.py` | -5 |
| Codigo duplicado excesivo (sin funciones auxiliares) | -5 |
| Ausencia total de comentarios | -3 |
