# Ejercicio 1: Dashboard de Sensores Industriales

## Descripcion

En este ejercicio simularas el monitoreo de una **planta de tratamiento de agua** equipada con 4 sensores industriales:

| Sensor | ID | Rango normal | Unidad |
|---|---|---|---|
| Temperatura | TEMP-001 | 20 - 25 | C |
| pH | PH-001 | 6.5 - 7.5 | pH |
| Turbidez | TURB-001 | 1 - 5 | NTU |
| Caudal | FLOW-001 | 100 - 150 | L/min |

Los datos simulan **~3.5 dias** de lecturas cada 30 segundos (~10,000 lecturas por sensor). Incluyen patrones diurnos realistas, ruido, anomalias y valores faltantes.

Tu objetivo es construir un **dashboard interactivo con Streamlit** que permita visualizar, analizar y reaccionar a los datos de estos sensores.

## Que ya esta incluido (codigo base)

- `mock_data/generate_data.py` - Script para generar los datos simulados (ya ejecutado).
- `mock_data/*.csv` - Archivos CSV con los datos de cada sensor.
- `models.py` - Dataclasses para `SensorConfig`, `Reading` y `Alert`.
- `sensor_simulator.py` - Clase `SensorSimulator` que entrega lecturas una por una.
- `app_ejemplo.py` - App minima de ejemplo que muestra un solo sensor.
- `requirements.txt` - Dependencias del proyecto.

## Lo que debes construir

Crea un archivo `dashboard.py` (o modifica `app_ejemplo.py`) con las siguientes funcionalidades:

### Tarea 1: Vista multi-sensor
- Mostrar los 4 sensores simultaneamente con graficos de linea.
- Cada grafico debe incluir lineas horizontales para los umbrales min/max.
- Agregar metricas resumidas (promedio, min, max, desviacion estandar) por sensor.

### Tarea 2: Sistema de alertas
- Detectar automaticamente cuando un valor excede los umbrales definidos en `SensorConfig`.
- Clasificar las alertas como "warning" o "critical" usando el metodo `get_severity()`.
- Mostrar un panel lateral con las alertas mas recientes.
- Incluir un contador de alertas por sensor y por severidad.

### Tarea 3: Controles interactivos
- Selector de rango de fechas para filtrar los datos mostrados.
- Sliders para ajustar los umbrales de cada sensor en tiempo real.
- Control de factor de calibracion por sensor.
- Selector de frecuencia de muestreo (mostrar cada N lecturas).

### Tarea 4: Analisis estadistico
- Calcular y mostrar estadisticas descriptivas por sensor.
- Detectar y resaltar los valores anomalos en los graficos.
- Implementar una media movil configurable (ventana de N lecturas).
- Mostrar la correlacion entre sensores (ej: temperatura vs. caudal).

### Tarea 5: Simulacion en tiempo real
- Usar `SensorSimulator` para alimentar el dashboard con lecturas una por una.
- Implementar un boton de inicio/pausa para la simulacion.
- Mostrar un indicador de progreso de la simulacion.
- Actualizar los graficos y alertas conforme llegan nuevas lecturas.

## Como ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Generar los datos (si no existen los CSV)

```bash
cd mock_data
python generate_data.py
```

### 3. Verificar con el ejemplo

```bash
streamlit run app_ejemplo.py
```

### 4. Ejecutar tu dashboard

```bash
streamlit run dashboard.py
```

## Tips y consejos

- **Empieza simple**: haz que funcione la Tarea 1 antes de avanzar a las demas.
- **Usa `st.columns()`** para organizar multiples graficos en la misma fila.
- **Usa `st.sidebar`** para los controles interactivos y alertas.
- **`st.session_state`** es clave para mantener estado entre recargas (simulacion).
- **Plotly Express** facilita crear graficos interactivos con pocas lineas de codigo.
- Para la media movil, revisa `pandas.DataFrame.rolling()`.
- Para correlaciones, revisa `pandas.DataFrame.corr()` y `plotly.express.imshow()`.
- Los datos ya tienen anomalias y NaN incorporados; tu codigo debe manejarlos.
- Revisa la documentacion de Streamlit: https://docs.streamlit.io/
- Revisa `models.py` para entender las estructuras de datos disponibles.
