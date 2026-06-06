"""
routes/reporte_routes.py - Reportes gerenciales exportables a CSV.
"""
import csv
import io
from flask import Blueprint, render_template, request, Response
from utils.db import query, call_proc
from utils.auth import login_required, role_required

reporte_bp = Blueprint("reporte", __name__, url_prefix="/reportes")


def _csv_response(rows, headers, filename):
    """Genera una respuesta CSV descargable."""
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(headers)
    for r in rows:
        writer.writerow([r.get(h) for h in headers])
    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@reporte_bp.route("/")
@login_required
def index():
    return render_template("reportes/index.html")


@reporte_bp.route("/stock")
@login_required
def stock():
    data = query("SELECT * FROM v_stock_por_planta ORDER BY planta, producto")
    if request.args.get("export") == "csv":
        return _csv_response(
            data, ["planta", "codigo", "producto", "presentacion", "stock_total", "stock_minimo"],
            "stock_por_planta.csv")
    return render_template("reportes/tabla.html", titulo="Stock por Planta",
                           data=data, endpoint="reporte.stock")


@reporte_bp.route("/vencimientos")
@login_required
def vencimientos():
    data = query("SELECT * FROM v_proximos_vencer ORDER BY dias_restantes")
    if request.args.get("export") == "csv":
        return _csv_response(
            data, ["numero_lote", "producto", "presentacion", "fecha_vencimiento",
                   "dias_restantes", "unidades"], "proximos_vencer.csv")
    return render_template("reportes/tabla.html", titulo="Productos Proximos a Vencer",
                           data=data, endpoint="reporte.vencimientos")


@reporte_bp.route("/pendientes")
@login_required
def pendientes():
    data = query("SELECT * FROM v_pedidos_pendientes ORDER BY fecha_pedido")
    if request.args.get("export") == "csv":
        return _csv_response(
            data, ["distribuidor", "ciudad", "id_pedido", "fecha_pedido",
                   "fecha_entrega_requerida", "estado", "monto_pedido"],
            "pedidos_pendientes.csv")
    return render_template("reportes/tabla.html", titulo="Pedidos Pendientes",
                           data=data, endpoint="reporte.pendientes")


@reporte_bp.route("/rotacion")
@role_required("Administrador", "Gerente")
def rotacion():
    anio = int(request.args.get("anio", 2026))
    mes = int(request.args.get("mes", 5))
    data = call_proc("sp_rotacion_producto", (anio, mes))
    if request.args.get("export") == "csv":
        return _csv_response(
            data, ["producto", "presentacion", "salidas_mes_actual", "salidas_mes_anterior"],
            "rotacion.csv")
    return render_template("reportes/tabla.html",
                           titulo=f"Rotacion de Inventario {mes}/{anio}",
                           data=data, endpoint="reporte.rotacion")
