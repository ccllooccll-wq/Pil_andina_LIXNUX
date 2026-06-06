"""
routes/producto_routes.py - CRUD de productos + busqueda avanzada con filtros.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.db import query, execute
from utils.auth import login_required, role_required, registrar_auditoria

producto_bp = Blueprint("producto", __name__, url_prefix="/productos")


@producto_bp.route("/")
@login_required
def listar():
    # Busqueda avanzada con filtros multiples (todo parametrizado)
    nombre = request.args.get("nombre", "").strip()
    tipo = request.args.get("tipo", "").strip()
    presentacion = request.args.get("presentacion", "").strip()

    sql = "SELECT * FROM producto WHERE 1=1"
    params = []
    if nombre:
        sql += " AND nombre_comercial LIKE %s"
        params.append(f"%{nombre}%")
    if tipo:
        sql += " AND tipo = %s"
        params.append(tipo)
    if presentacion:
        sql += " AND presentacion = %s"
        params.append(presentacion)
    sql += " ORDER BY nombre_comercial"

    productos = query(sql, tuple(params))
    return render_template("productos/listar.html", productos=productos,
                           f_nombre=nombre, f_tipo=tipo, f_pres=presentacion)


@producto_bp.route("/nuevo", methods=["GET", "POST"])
@role_required("Administrador")
def nuevo():
    if request.method == "POST":
        datos = (
            request.form["codigo"], request.form["nombre_comercial"],
            request.form["tipo"], request.form["presentacion"],
            request.form["graduacion_alcoholica"], request.form["precio_actual"],
            request.form["stock_minimo"], request.form["stock_maximo"],
        )
        execute(
            "INSERT INTO producto (codigo, nombre_comercial, tipo, presentacion, "
            "graduacion_alcoholica, precio_actual, stock_minimo, stock_maximo) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", datos,
        )
        registrar_auditoria("INSERT", "producto", f"Alta producto {datos[0]}")
        flash("Producto creado correctamente.", "success")
        return redirect(url_for("producto.listar"))
    return render_template("productos/form.html", producto=None)


@producto_bp.route("/editar/<int:pid>", methods=["GET", "POST"])
@role_required("Administrador")
def editar(pid):
    producto = query("SELECT * FROM producto WHERE id_producto=%s", (pid,), fetchone=True)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("producto.listar"))

    if request.method == "POST":
        execute(
            "UPDATE producto SET nombre_comercial=%s, tipo=%s, presentacion=%s, "
            "graduacion_alcoholica=%s, precio_actual=%s, stock_minimo=%s, "
            "stock_maximo=%s WHERE id_producto=%s",
            (request.form["nombre_comercial"], request.form["tipo"],
             request.form["presentacion"], request.form["graduacion_alcoholica"],
             request.form["precio_actual"], request.form["stock_minimo"],
             request.form["stock_maximo"], pid),
        )
        registrar_auditoria("UPDATE", "producto", f"Edicion producto id {pid}")
        flash("Producto actualizado.", "success")
        return redirect(url_for("producto.listar"))
    return render_template("productos/form.html", producto=producto)


@producto_bp.route("/eliminar/<int:pid>", methods=["POST"])
@role_required("Administrador")
def eliminar(pid):
    # Baja logica para preservar integridad referencial
    execute("UPDATE producto SET activo=0 WHERE id_producto=%s", (pid,))
    registrar_auditoria("DELETE", "producto", f"Baja logica producto id {pid}")
    flash("Producto dado de baja.", "info")
    return redirect(url_for("producto.listar"))
