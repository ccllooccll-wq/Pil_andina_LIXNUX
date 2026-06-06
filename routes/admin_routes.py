"""
routes/admin_routes.py - Panel de administracion:
gestion de usuarios/roles, backups y monitoreo.
Acceso restringido al rol Administrador.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from utils.db import query, execute
from utils.auth import role_required, registrar_auditoria
from utils.backup import crear_backup, listar_backups, restaurar_backup

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ----------------------- USUARIOS Y ROLES -----------------------
@admin_bp.route("/usuarios")
@role_required("Administrador")
def usuarios():
    items = query(
        "SELECT u.id_usuario, u.nombre, u.correo, u.activo, r.nombre AS rol "
        "FROM usuario u JOIN rol r ON r.id_rol=u.id_rol ORDER BY u.nombre"
    )
    roles = query("SELECT * FROM rol")
    return render_template("admin/usuarios.html", items=items, roles=roles)


@admin_bp.route("/usuarios/nuevo", methods=["POST"])
@role_required("Administrador")
def usuario_nuevo():
    pwd_hash = generate_password_hash(request.form["password"])
    execute(
        "INSERT INTO usuario (nombre, correo, password_hash, id_rol) "
        "VALUES (%s,%s,%s,%s)",
        (request.form["nombre"], request.form["correo"], pwd_hash,
         request.form["id_rol"]),
    )
    registrar_auditoria("INSERT", "usuario", f"Alta usuario {request.form['correo']}")
    flash("Usuario creado.", "success")
    return redirect(url_for("admin.usuarios"))


@admin_bp.route("/usuarios/estado/<int:uid>", methods=["POST"])
@role_required("Administrador")
def usuario_estado(uid):
    execute("UPDATE usuario SET activo = NOT activo WHERE id_usuario=%s", (uid,))
    registrar_auditoria("UPDATE", "usuario", f"Cambio de estado usuario id {uid}")
    flash("Estado del usuario actualizado.", "info")
    return redirect(url_for("admin.usuarios"))


# ----------------------- BACKUPS -----------------------
@admin_bp.route("/backups")
@role_required("Administrador")
def backups():
    return render_template("admin/backups.html", items=listar_backups())


@admin_bp.route("/backups/crear", methods=["POST"])
@role_required("Administrador")
def backup_crear():
    try:
        fname = crear_backup()
        registrar_auditoria("BACKUP", "sistema", f"Backup creado: {fname}")
        flash(f"Backup creado: {fname}", "success")
    except Exception as e:
        flash(f"Error al crear backup: {e}", "danger")
    return redirect(url_for("admin.backups"))


@admin_bp.route("/backups/restaurar", methods=["POST"])
@role_required("Administrador")
def backup_restaurar():
    nombre = request.form["nombre"]
    try:
        restaurar_backup(nombre)
        registrar_auditoria("RESTORE", "sistema", f"Restauracion: {nombre}")
        flash(f"Backup restaurado: {nombre}", "success")
    except Exception as e:
        flash(f"Error al restaurar: {e}", "danger")
    return redirect(url_for("admin.backups"))


# ----------------------- MONITOREO -----------------------
@admin_bp.route("/monitoreo")
@role_required("Administrador")
def monitoreo():
    # Conexiones / procesos activos en MySQL
    try:
        procesos = query("SHOW PROCESSLIST")
    except Exception:
        procesos = []
    # Estado del servidor (conexiones)
    try:
        conexiones = query("SHOW STATUS LIKE 'Threads_connected'", fetchone=True)
    except Exception:
        conexiones = {"Value": "N/D"}
    # Ultimos registros de auditoria (logs)
    logs = query(
        "SELECT a.fecha_hora, u.nombre AS usuario, a.accion, a.tabla_afectada, "
        "a.descripcion FROM auditoria a LEFT JOIN usuario u ON u.id_usuario=a.id_usuario "
        "ORDER BY a.fecha_hora DESC LIMIT 50"
    )
    return render_template("admin/monitoreo.html", procesos=procesos,
                           conexiones=conexiones, logs=logs)
