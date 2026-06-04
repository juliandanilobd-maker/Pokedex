"""
Este módulo inserta un Manager cache para persistencia de cache basado en SQ Lite.
Serializa las respuestas en formato JSON y maneja TTL.
"""

import json
import sqlite3
import time

from backend.app.core.config import settings


class CacheManager:
    def __init__(self):

        self.db_path = settings.CACHE_DB_PATH

        self._init_db()

    def _init_db(self):

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value TEXT,
                expires_at REAL)
            """)

            # Limpieza de registros expirados al iniciar el manager,
            # para evitar llenar la base de datos
            conn.execute("DELETE FROM cache WHERE expires_at < ?", (time.time(),))
            conn.commit()

    def get(self, key: str):

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT value, expires_at FROM cache WHERE key=?", (key,)
            ).fetchone()

            if not row:
                return None

            value, expires_at = row

            if time.time() > expires_at:
                conn.execute("DELETE FROM cache WHERE key=?", (key,))
                conn.commit()

                return None

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # Si el JSON está corrupto, lo eliminamos para hacer una nueva petición
                conn.execute("DELETE FROM cache WHERE key=?", (key,))

                conn.commit()
                return None

    def set(self, key: str, value, ttl: int | None = None):

        ttl = ttl or settings.CACHE_TTL
        expires = time.time() + ttl

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache
                VALUES (?, ?, ?)
            """,
                (key, json.dumps(value), expires),
            )
            conn.commit()
