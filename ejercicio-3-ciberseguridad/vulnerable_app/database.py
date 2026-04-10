"""
Modulo de base de datos para la aplicacion web.
Maneja la conexion SQLite y la inicializacion de datos.

*** ESTA APLICACION ES INTENCIONALMENTE VULNERABLE. NO DESPLEGAR EN PRODUCCION. ***
"""

import sqlite3
import os

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "tienda.db")


def get_db():
    """Obtiene una conexion a la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias en la base de datos."""
    conn = get_db()
    cursor = conn.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    """)

    # Tabla de comentarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Inserta datos de ejemplo en la base de datos."""
    conn = get_db()
    cursor = conn.cursor()

    # Verificar si ya hay datos
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insertar usuarios
    usuarios = [
        ("admin", "admin123", "admin"),
        ("user1", "password1", "user"),
        ("user2", "password2", "user"),
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        usuarios
    )

    # Insertar productos
    productos = [
        ("Laptop ProMax 15", 1299.99, "Laptop de alto rendimiento con 16GB RAM y SSD de 512GB"),
        ("Mouse Ergonomico X1", 49.99, "Mouse inalambrico con diseno ergonomico y 6 botones programables"),
        ("Teclado Mecanico RGB", 89.99, "Teclado mecanico con switches Cherry MX y retroiluminacion RGB"),
        ("Monitor UltraWide 34", 599.99, "Monitor curvo de 34 pulgadas con resolucion WQHD"),
        ("Auriculares BT Pro", 129.99, "Auriculares Bluetooth con cancelacion de ruido activa"),
        ("Webcam HD 1080p", 69.99, "Camara web con microfono integrado y luz LED ajustable"),
        ("Hub USB-C 7en1", 39.99, "Hub USB-C con HDMI, USB 3.0, lector SD y carga PD"),
        ("SSD Externo 1TB", 109.99, "Disco solido externo USB 3.2 con velocidades de hasta 1050MB/s"),
        ("Soporte Monitor Dual", 79.99, "Soporte ajustable para dos monitores de hasta 27 pulgadas"),
        ("Alfombrilla XL Gaming", 24.99, "Alfombrilla de raton extendida con base antideslizante"),
    ]
    cursor.executemany(
        "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
        productos
    )

    # Insertar comentarios
    comentarios = [
        ("Carlos M.", "Excelente tienda, los productos llegaron en perfecto estado."),
        ("Ana R.", "El servicio al cliente fue muy amable y resolvieron mi duda rapidamente."),
        ("Pedro L.", "Buenos precios y envio rapido. Totalmente recomendado."),
    ]
    cursor.executemany(
        "INSERT INTO comments (author, content) VALUES (?, ?)",
        comentarios
    )

    conn.commit()
    conn.close()
    print("[*] Base de datos inicializada con datos de ejemplo.")
