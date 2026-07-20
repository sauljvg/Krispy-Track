import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "krispy_kreme.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def dict_rows(cursor):
    return [dict(row) for row in cursor.fetchall()]


def _ensure_transactions_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS store_transactions (
            tienda TEXT NOT NULL,
            mes TEXT NOT NULL,
            transacciones INTEGER NOT NULL,
            actualizado TEXT,
            PRIMARY KEY (tienda, mes)
        )
    """)
    # Migración: la tabla original solo tenía (tienda PK, transacciones), sin
    # mes. Si existe con el esquema viejo, se recrea (no había datos reales
    # todavía, solo pruebas).
    cols = {row[1] for row in conn.execute("PRAGMA table_info(store_transactions)")}
    if "mes" not in cols:
        conn.execute("DROP TABLE store_transactions")
        conn.execute("""
            CREATE TABLE store_transactions (
                tienda TEXT NOT NULL,
                mes TEXT NOT NULL,
                transacciones INTEGER NOT NULL,
                actualizado TEXT,
                PRIMARY KEY (tienda, mes)
            )
        """)
    conn.commit()
    conn.close()


def _ensure_store_meta_table():
    """Guarda el total de reseñas que Google anuncia para cada tienda (lo
    escribe el scraper al final de cada pasada), para poder marcar con un
    check cuando ya tenemos el 100% capturado."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS store_meta (
            tienda TEXT PRIMARY KEY,
            total_google INTEGER,
            actualizado TEXT
        )
    """)
    conn.commit()
    conn.close()


_ensure_transactions_table()
_ensure_store_meta_table()
