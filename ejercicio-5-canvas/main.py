#!/usr/bin/env python3
"""
main.py - Punto de entrada del Canvas Interactivo.

Ejecutar con: python main.py
Se abrira en el navegador en http://localhost:8080

Para acceder desde otro dispositivo (iPad, movil) en la misma red:
    python main.py
    Luego abrir http://<IP_DE_TU_ORDENADOR>:8080 en el otro dispositivo
"""

from nicegui import ui
from app import CanvasApp

# Crear la aplicacion
app = CanvasApp()


# Construir la interfaz
@ui.page('/')
def index():
    app.build()


# Iniciar el servidor (accesible desde cualquier dispositivo en la red)
ui.run(host='0.0.0.0', port=8080, title='Canvas Interactivo')
