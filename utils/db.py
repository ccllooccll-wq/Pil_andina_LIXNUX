"""
db.py - Capa de acceso a datos.
Usa mysql-connector-python con consultas parametrizadas (placeholders %s)
para prevenir inyeccion SQL. NUNCA se concatenan valores en las consultas.
"""
import mysql.connector
from mysql.connector import pooling
from flask import current_app

_pool = None


def init_pool(app):
    """Inicializa el pool de conexiones al arrancar la app."""
    global _pool
    _pool = pooling.MySQLConnectionPool(
        pool_name="pil_pool",
        pool_size=5,
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"],
        charset="utf8mb4",
        autocommit=False,
    )


def get_conn():
    return _pool.get_connection()


def query(sql, params=None, fetchone=False):
    """SELECT parametrizado. Devuelve lista de dicts (o un dict si fetchone)."""
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        data = cur.fetchone() if fetchone else cur.fetchall()
        return data
    finally:
        cur.close()
        conn.close()


def execute(sql, params=None):
    """INSERT/UPDATE/DELETE parametrizado. Devuelve lastrowid / filas afectadas."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid or cur.rowcount
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def call_proc(name, args):
    """Ejecuta un procedimiento almacenado y devuelve los resultados."""
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.callproc(name, args)
        results = []
        for res in cur.stored_results():
            results.extend(res.fetchall())
        conn.commit()
        return results
    finally:
        cur.close()
        conn.close()
