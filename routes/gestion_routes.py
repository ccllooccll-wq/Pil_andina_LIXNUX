"""
routes/gestion_routes.py - CRUD de inventario, lotes y distribuidores.
Cubre 4 tablas principales con operaciones de gestion.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db import query, execute, call_proc
from utils.auth import login_required, role_required, registrar_auditoria

gestion_bp = Blueprint("gestion", __name__)

# ----------------------- INVENTARIO -----------------------
@gestion_bp.route("/inventario")
@login_required
def inventario():
    bodega = request.args.get("bodega", "").strip()
    sql = (
        "SELECT i.id_inventario, p.nombre_comercial, p.presentacion, "
        "l.numero_lote, b.nombre AS bodega, i.cantidad_actual, l.fecha_vencimiento "
        "FROM inventario i "
        "JOIN producto p ON p.id_producto=i.id_producto "
        "JOIN lote l ON l.id_lote=i.id_lote "
        "JOIN bodega b ON b.id_bodega=i.id_bodega WHERE 1=1"
    )
    params = []
    if bodega:
        sql += " AND b.nombre LIKE %s"
        params.append(f"%{bodega}%")
    sql += " ORDER BY p.nombre_comercial"
    items = query(sql, tuple(params))
    return render_template("inventario/listar.html", items=items, f_bodega=bodega)


@gestion_bp.route("/inventario/movimiento/<int:iid>", methods=["POST"])
@role_required("Administrador", "Gerente")
def movimiento(iid):
    from flask import session
    tipo = request.form["tipo"]
    cantidad = int(request.form["cantidad"])
    motivo = request.form.get("motivo", "")
    try:
        call_proc("sp_registrar_movimiento",
                  (iid, tipo, cantidad, motivo, session["user_id"]))
        registrar_auditoria("UPDATE", "inventario",
                            f"Movimiento {tipo} de {cantidad} en inv {iid}")
        flash(f"Movimiento {tipo} registrado.", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
    return redirect(url_for("gestion.inventario"))


# ----------------------- LOTES -----------------------
@gestion_bp.route("/lotes")
@login_required
def lotes():
    items = query(
        "SELECT l.*, p.nombre_comercial, pl.nombre AS planta, "
        "cc.resultado AS calidad "
        "FROM lote l JOIN producto p ON p.id_producto=l.id_producto "
        "JOIN planta pl ON pl.id_planta=l.id_planta "
        "LEFT JOIN control_calidad cc ON cc.id_lote=l.id_lote "
        "ORDER BY l.fecha_produccion DESC"
    )
    return render_template("lotes/listar.html", items=items)


@gestion_bp.route("/lotes/nuevo", methods=["GET", "POST"])
@role_required("Administrador")
def lote_nuevo():
    if request.method == "POST":
        execute(
            "INSERT INTO lote (numero_lote, id_producto, id_planta, "
            "fecha_produccion, fecha_vencimiento, cantidad_producida) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (request.form["numero_lote"], request.form["id_producto"],
             request.form["id_planta"], request.form["fecha_produccion"],
             request.form["fecha_vencimiento"], request.form["cantidad_producida"]),
        )
        registrar_auditoria("INSERT", "lote", f"Alta lote {request.form['numero_lote']}")
        flash("Lote registrado.", "success")
        return redirect(url_for("gestion.lotes"))
    productos = query("SELECT id_producto, codigo, nombre_comercial, presentacion FROM producto WHERE activo=1")
    plantas = query("SELECT id_planta, nombre FROM planta")
    return render_template("lotes/form.html", productos=productos, plantas=plantas)


# ----------------------- DISTRIBUIDORES -----------------------
@gestion_bp.route("/distribuidores")
@login_required
def distribuidores():
    ciudad = request.args.get("ciudad", "").strip()
    sql = "SELECT * FROM distribuidor WHERE 1=1"
    params = []
    if ciudad:
        sql += " AND ciudad LIKE %s"
        params.append(f"%{ciudad}%")
    sql += " ORDER BY razon_social"
    items = query(sql, tuple(params))
    return render_template("distribuidores/listar.html", items=items, f_ciudad=ciudad)


@gestion_bp.route("/distribuidores/nuevo", methods=["GET", "POST"])
@role_required("Administrador")
def dist_nuevo():
    if request.method == "POST":
        execute(
            "INSERT INTO distribuidor (nit, razon_social, direccion, ciudad, "
            "zona, contacto, telefono, correo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (request.form["nit"], request.form["razon_social"],
             request.form["direccion"], request.form["ciudad"],
             request.form["zona"], request.form["contacto"],
             request.form["telefono"], request.form["correo"]),
        )
        registrar_auditoria("INSERT", "distribuidor", f"Alta distribuidor {request.form['nit']}")
        flash("Distribuidor creado.", "success")
        return redirect(url_for("gestion.distribuidores"))
    return render_template("distribuidores/form.html", dist=None)


@gestion_bp.route("/distribuidores/editar/<int:did>", methods=["GET", "POST"])
@role_required("Administrador")
def dist_editar(did):
    dist = query("SELECT * FROM distribuidor WHERE id_distribuidor=%s", (did,), fetchone=True)
    if request.method == "POST":
        execute(
            "UPDATE distribuidor SET razon_social=%s, direccion=%s, ciudad=%s, "
            "zona=%s, contacto=%s, telefono=%s, correo=%s WHERE id_distribuidor=%s",
            (request.form["razon_social"], request.form["direccion"],
             request.form["ciudad"], request.form["zona"], request.form["contacto"],
             request.form["telefono"], request.form["correo"], did),
        )
        registrar_auditoria("UPDATE", "distribuidor", f"Edicion distribuidor id {did}")
        flash("Distribuidor actualizado.", "success")
        return redirect(url_for("gestion.distribuidores"))
    return render_template("distribuidores/form.html", dist=dist)
