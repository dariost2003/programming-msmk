# Este es solo un ejemplo. Tu tarea es construir el dashboard completo.

"""
App de ejemplo para verificar que el entorno funciona correctamente.

Carga el CSV de temperatura y muestra un grafico de linea basico.
Ejecuta con: streamlit run app_ejemplo.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- Configuracion de la pagina ---
st.set_page_config(
    page_title="Sensores - Ejemplo",
    page_icon="🌡️",
    layout="wide",
)

st.title("Planta de Tratamiento de Agua - Ejemplo Basico")
st.markdown("---")
st.info(
    "Este es solo un ejemplo minimo para verificar que tu entorno funciona. "
    "Tu tarea es construir el dashboard completo con todos los sensores, "
    "alertas, controles interactivos y visualizaciones avanzadas."
)

# --- Cargar datos de temperatura ---
RUTA_DATOS = Path(__file__).parent / "mock_data" / "temperatura.csv"

if not RUTA_DATOS.exists():
    st.error(
        "No se encontro el archivo de datos. "
        "Ejecuta primero: `python mock_data/generate_data.py`"
    )
    st.stop()

df = pd.read_csv(RUTA_DATOS, parse_dates=["timestamp"])

# --- Mostrar informacion basica ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de lecturas", len(df))
with col2:
    st.metric("Valores faltantes", df["value"].isna().sum())
with col3:
    st.metric("Temperatura promedio", f"{df['value'].mean():.2f} C")

# --- Grafico de linea basico ---
st.subheader("Temperatura del agua a lo largo del tiempo")

fig = px.line(
    df.dropna(subset=["value"]),
    x="timestamp",
    y="value",
    title="Sensor TEMP-001: Temperatura",
    labels={"timestamp": "Fecha/Hora", "value": "Temperatura (C)"},
)
fig.update_layout(
    xaxis_title="Fecha/Hora",
    yaxis_title="Temperatura (C)",
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)

# --- Tabla con primeras filas ---
st.subheader("Primeras lecturas")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("---")
st.caption("Ejercicio 1: Dashboard de Sensores Industriales")
