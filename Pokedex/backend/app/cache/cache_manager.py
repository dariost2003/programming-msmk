import sqlite3
import json
import time

from app.core.config import Settings

class CacheManager:

    def __init__(self):

        self.db_path = Settings.CACHE_DB_PATH

        self._init_db()

    def _init_db(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at REAL)
            """)
    
    def get(self, key: str):

        with sqlite3.connect(self.db_path) as conn:

            row = conn.execute(
                'SELECT value, expires_at FROM cache WHERE key=?',
                (key,)
            ).fetchone()

            if not row:
                return None
            
            value, expires_at = row

            if time.time() > expires_at:

                conn.execute(
                    'DELETE FROM cache WHERE key=?',
                    (key,)
                )

                return None
            
            return json.loads(value)


    def set(self, key: str, value, ttl=3600):

        expires = time.time() + ttl

        with sqlite3.connect(self.db_path) as conn:

            conn.execute("""
                        INSERT OR REPLACE INTO cache
                        VALUES (? ? ?)
                        """, (
                            key,
                            json.dumps(value),
                            expires
                        ))    

    
 