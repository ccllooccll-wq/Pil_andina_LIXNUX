"""
routes/main_routes.py - Dashboard y pagina principal.
"""
from flask import Blueprint, render_template, session
from utils.db import query
from utils.auth import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    # Tarjetas de metricas
    total_productos = query("SELECT COUNT(*) c FROM producto WHERE activo=1", fetchone=True)["c"]
    total_stock = query("SELECT COALESCE(SUM(cantidad_actual),0) s FROM inventario", fetchone=True)["s"]
    pedidos_pend = query("SELECT COUNT(*) c FROM pedido WHERE estado='Pendiente'", fetchone=True)["c"]
    por_vencer = query("SELECT COUNT(*) c FROM v_proximos_vencer", fetchone=True)["c"]

    # Datos para grafico: stock por planta
    stock_planta = query(
        "SELECT pl.nombre planta, COALESCE(SUM(i.cantidad_actual),0) total "
        "FROM planta pl LEFT JOIN bodega b ON b.id_planta=pl.id_planta "
        "LEFT JOIN inventario i ON i.id_bodega=b.id_bodega GROUP BY pl.nombre"
    )

    # Datos para grafico: pedidos por estado
    pedidos_estado = query(
        "SELECT estado, COUNT(*) total FROM pedido GROUP BY estado"
    )

    # Productos bajo stock minimo
    bajo_stock = query("SELECT * FROM v_bajo_stock")

    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        total_stock=total_stock,
        pedidos_pend=pedidos_pend,
        por_vencer=por_vencer,
        stock_planta=stock_planta,
        pedidos_estado=pedidos_estado,
        bajo_stock=bajo_stock,
    )
