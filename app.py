"""
app.py - Punto de entrada de la aplicacion Flask.
Sistema de Gestion de Inventario y Distribucion - PIL ANDINA
"""
from flask import Flask
from config import Config
from utils.db import init_pool


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar pool de conexiones
    init_pool(app)

    # Registrar blueprints
    from routes.auth_routes import auth_bp
    from routes.main_routes import main_bp
    from routes.producto_routes import producto_bp
    from routes.gestion_routes import gestion_bp
    from routes.reporte_routes import reporte_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(gestion_bp)
    app.register_blueprint(reporte_bp)
    app.register_blueprint(admin_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
