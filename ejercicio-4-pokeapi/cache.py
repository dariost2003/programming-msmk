"""
Modulo de cache basado en SQLite para almacenar respuestas de la PokeAPI.

Evita hacer peticiones repetidas a la API, lo cual es importante para:
- No sobrecargar el servidor de PokeAPI
- Acelerar el desarrollo (las respuestas se sirven desde disco)
- Poder trabajar offline con datos ya consultados
"""

import sqlite3
import json
import time
import os


class CacheManager:
    """Administrador de cache usando SQLite como almacenamiento."""

    def __init__(self, db_path: str = "pokemon_cache.db"):
        """
        Inicializa el cache.

        Args:
            db_path: Ruta al archivo SQLite. Por defecto 'pokemon_cache.db'
                     en el directorio actual.
        """
        self.db_path = db_path
        self._hits = 0
        self._misses = 0
        self._init_db()

    def _init_db(self):
        """Crea la tabla de cache si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires_at REAL NOT NULL,
                    created_at REAL NOT NULL
                )
            """)
            conn.commit()

    def get(self, key: str):
        """
        Busca un valor en el cache.

        Args:
            key: Clave de busqueda (normalmente la URL del endpoint).

        Returns:
            El valor almacenado (dict/list) si existe y no ha expirado,
            o None si no se encuentra o ya expiro.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value, expires_at FROM cache WHERE key = ?",
                (key,)
            )
            row = cursor.fetchone()

            if row is None:
                self._misses += 1
                return None

            value, expires_at = row

            # Verificar si el cache ha expirado
            if time.time() > expires_at:
                # Eliminar entrada expirada
                conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                conn.commit()
                self._misses += 1
                return None

            self._hits += 1
            return json.loads(value)

    def set(self, key: str, value, ttl: int = 3600):
        """
        Almacena un valor en el cache.

        Args:
            key: Clave unica (normalmente la URL del endpoint).
            value: Valor a almacenar (debe ser serializable a JSON).
            ttl: Tiempo de vida en segundos. Por defecto 1 hora (3600s).
        """
        now = time.time()
        expires_at = now + ttl
        serialized = json.dumps(value, ensure_ascii=False)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache (key, value, expires_at, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (key, serialized, expires_at, now)
            )
            conn.commit()

    def clear(self):
        """Elimina todas las entradas del cache."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache")
            conn.commit()
        self._hits = 0
        self._misses = 0

    def stats(self) -> dict:
        """
        Retorna estadisticas del cache.

        Returns:
            dict con:
                - hits: Numero de consultas exitosas al cache
                - misses: Numero de consultas fallidas (no encontrado o expirado)
                - total_entries: Numero de entradas almacenadas
                - hit_rate: Porcentaje de aciertos (0.0 a 1.0)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM cache")
            total_entries = cursor.fetchone()[0]

            # Contar solo las entradas que no han expirado
            cursor = conn.execute(
                "SELECT COUNT(*) FROM cache WHERE expires_at > ?",
                (time.time(),)
            )
            valid_entries = cursor.fetchone()[0]

        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

        return {
            "hits": self._hits,
            "misses": self._misses,
            "total_entries": total_entries,
            "valid_entries": valid_entries,
            "hit_rate": round(hit_rate, 3),
        }
