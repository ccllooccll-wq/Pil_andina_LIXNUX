"""
auth.py - Helpers de autenticacion, control de roles y auditoria.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request
from utils.db import execute


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Debe iniciar sesion para continuar.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


def role_required(*roles):
    """Restringe el acceso a los roles indicados (por nombre)."""
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))
            if session.get("rol") not in roles:
                flash("No tiene permisos para acceder a esta seccion.", "danger")
                return redirect(url_for("main.dashboard"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


def registrar_auditoria(accion, tabla, descripcion):
    """Inserta un registro en la tabla de auditoria."""
    uid = session.get("user_id")
    execute(
        "INSERT INTO auditoria (id_usuario, accion, tabla_afectada, descripcion) "
        "VALUES (%s, %s, %s, %s)",
        (uid, accion, tabla, descripcion),
    )
