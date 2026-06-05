"""
Punto de entrada para la aplicacion TechStore.

*** ADVERTENCIA ***
ESTA APLICACION ES INTENCIONALMENTE VULNERABLE.
NO DESPLEGAR EN PRODUCCION NI EN REDES PUBLICAS.
Solo para uso educativo en entornos locales controlados.

Ejecutar con: python run.py
"""

from vulnerable_app.app import app
from vulnerable_app.database import init_db, seed_db

if __name__ == "__main__":
    print("=" * 60)
    print("  TechStore - Aplicacion Web de Ejemplo")
    print("  ADVERTENCIA: Aplicacion intencionalmente vulnerable")
    print("  Solo para uso educativo local")
    print("=" * 60)
    print()

    # Inicializar y poblar la base de datos
    init_db()
    seed_db()

    print("[*] Servidor iniciando en http://127.0.0.1:5000")
    print("[*] Presiona Ctrl+C para detener el servidor")
    print()

    # Ejecutar la aplicacion en modo de desarrollo
    app.run(debug=True, host="127.0.0.1", port=5000)
