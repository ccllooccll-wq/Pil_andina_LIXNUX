"""
routes/auth_routes.py - Login y logout.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from utils.db import query
from utils.auth import registrar_auditoria

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        password = request.form.get("password", "")

        # Consulta parametrizada (anti SQL injection)
        user = query(
            "SELECT u.id_usuario, u.nombre, u.password_hash, u.activo, r.nombre AS rol "
            "FROM usuario u JOIN rol r ON r.id_rol = u.id_rol "
            "WHERE u.correo = %s",
            (correo,), fetchone=True,
        )

        if user and user["activo"] and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id_usuario"]
            session["nombre"] = user["nombre"]
            session["rol"] = user["rol"]
            registrar_auditoria("LOGIN", "usuario", f"Inicio de sesion: {correo}")
            flash(f"Bienvenido, {user['nombre']}.", "success")
            return redirect(url_for("main.dashboard"))

        flash("Credenciales invalidas.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    if "user_id" in session:
        registrar_auditoria("LOGOUT", "usuario", "Cierre de sesion")
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))
