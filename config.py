"""
config.py - Configuracion central de la aplicacion Flask
Sistema de Inventario y Distribucion - PIL ANDINA
"""
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "pil-andina-secret-2026-cambiar-en-produccion")

    # --- Conexion MySQL ---
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "pil_andina")

    # --- Rutas de backups ---
    BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backups")

    # mysqldump / mysql ejecutables (ajustar segun instalacion: XAMPP, etc.)
    MYSQLDUMP = os.environ.get("MYSQLDUMP", "mysqldump")
    MYSQL_BIN = os.environ.get("MYSQL_BIN", "mysql")
