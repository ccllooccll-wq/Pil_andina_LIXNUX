"""
backup.py - Gestion de backups con mysqldump/mysql.
"""
import os
import subprocess
from datetime import datetime
from flask import current_app


def _backup_dir():
    d = os.path.abspath(current_app.config["BACKUP_DIR"])
    os.makedirs(d, exist_ok=True)
    return d


def crear_backup():
    """Genera un dump .sql con marca de tiempo. Devuelve el nombre del archivo."""
    cfg = current_app.config
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"backup_{cfg['DB_NAME']}_{ts}.sql"
    fpath = os.path.join(_backup_dir(), fname)

    cmd = [
        cfg["MYSQLDUMP"],
        f"-h{cfg['DB_HOST']}",
        f"-P{cfg['DB_PORT']}",
        f"-u{cfg['DB_USER']}",
        cfg["DB_NAME"],
    ]
    if cfg["DB_PASSWORD"]:
        cmd.insert(4, f"-p{cfg['DB_PASSWORD']}")

    with open(fpath, "w", encoding="utf-8") as out:
        subprocess.run(cmd, stdout=out, check=True)
    return fname


def listar_backups():
    d = _backup_dir()
    items = []
    for f in sorted(os.listdir(d), reverse=True):
        if f.endswith(".sql"):
            full = os.path.join(d, f)
            items.append({
                "nombre": f,
                "tamano_kb": round(os.path.getsize(full) / 1024, 1),
                "fecha": datetime.fromtimestamp(os.path.getmtime(full))
                         .strftime("%Y-%m-%d %H:%M:%S"),
            })
    return items


def restaurar_backup(nombre):
    """Restaura la BD desde un archivo de backup existente."""
    cfg = current_app.config
    fpath = os.path.join(_backup_dir(), nombre)
    if not os.path.isfile(fpath):
        raise FileNotFoundError(nombre)

    cmd = [
        cfg["MYSQL_BIN"],
        f"-h{cfg['DB_HOST']}",
        f"-P{cfg['DB_PORT']}",
        f"-u{cfg['DB_USER']}",
        cfg["DB_NAME"],
    ]
    if cfg["DB_PASSWORD"]:
        cmd.insert(4, f"-p{cfg['DB_PASSWORD']}")

    with open(fpath, "r", encoding="utf-8") as inp:
        subprocess.run(cmd, stdin=inp, check=True)
