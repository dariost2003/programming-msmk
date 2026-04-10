"""
Aplicacion web de tienda en linea - TechStore.
Permite buscar productos, dejar comentarios y gestionar usuarios.

*** ESTA APLICACION ES INTENCIONALMENTE VULNERABLE. NO DESPLEGAR EN PRODUCCION. ***
*** Solo para uso educativo en entornos locales controlados. ***
"""

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, send_file, abort
)
import os
import sqlite3

from .database import get_db

# Configuracion de la aplicacion
app = Flask(__name__)
app.secret_key = "clave_secreta_de_la_app"

# Credenciales del administrador
ADMIN_PASSWORD = "admin123"

# Directorio de archivos descargables
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")


# --- Pagina principal ---
@app.route("/")
def index():
    """Pagina de inicio con enlaces a todas las secciones."""
    return render_template("index.html")


# --- Sistema de autenticacion ---
@app.route("/login", methods=["GET", "POST"])
def login():
    """Maneja el inicio de sesion de usuarios."""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Buscar usuario en la base de datos
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash(f"Bienvenido, {user['username']}!", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contrasena incorrectos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Cierra la sesion del usuario."""
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("index"))


# --- Busqueda de productos ---
@app.route("/search")
def search():
    """Busca productos por nombre."""
    search_term = request.args.get("q", "")
    results = []
    error = None

    if search_term:
        try:
            conn = get_db()
            cursor = conn.cursor()
            # Construir consulta de busqueda
            query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            error = str(e)

    return render_template("search.html", results=results, query=search_term, error=error)


# --- Sistema de comentarios ---
@app.route("/comments", methods=["GET", "POST"])
def comments():
    """Muestra y permite agregar comentarios."""
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        author = request.form.get("author", "Anonimo")
        content = request.form.get("content", "")

        if content.strip():
            cursor.execute(
                "INSERT INTO comments (author, content) VALUES (?, ?)",
                (author, content)
            )
            conn.commit()
            flash("Comentario agregado exitosamente.", "success")
        else:
            flash("El comentario no puede estar vacio.", "error")

    # Obtener todos los comentarios
    cursor.execute("SELECT * FROM comments ORDER BY timestamp DESC")
    all_comments = cursor.fetchall()
    conn.close()

    return render_template("comments.html", comments=all_comments)


# --- Descarga de archivos ---
@app.route("/download")
def download():
    """Permite descargar archivos del servidor."""
    filename = request.args.get("file", "")

    if not filename:
        flash("No se especifico un archivo para descargar.", "error")
        return redirect(url_for("index"))

    # Construir la ruta del archivo
    filepath = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        abort(404)


# --- Panel de administracion ---
@app.route("/admin")
def admin():
    """Panel de administracion - muestra usuarios y productos."""
    if "user_id" not in session:
        flash("Debes iniciar sesion para acceder al panel.", "error")
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin.html", users=users, products=products)


# --- Manejo de errores ---
@app.errorhandler(404)
def not_found(e):
    """Pagina de error 404."""
    return render_template("base.html", error="Pagina no encontrada"), 404


@app.errorhandler(500)
def server_error(e):
    """Pagina de error 500."""
    return render_template("base.html", error="Error interno del servidor"), 500
