-- =====================================================================
-- Archivo 04: Usuarios de BD, Roles y Privilegios minimos
-- =====================================================================
USE pil_andina;

-- ---------------------------------------------------------------------
-- ROL 1: ADMINISTRADOR  (control total sobre la BD)
-- ---------------------------------------------------------------------
DROP USER IF EXISTS 'pil_admin'@'localhost';
CREATE USER 'pil_admin'@'localhost' IDENTIFIED BY 'AdminPil2026*';
GRANT ALL PRIVILEGES ON pil_andina.* TO 'pil_admin'@'localhost';

-- ---------------------------------------------------------------------
-- ROL 2: GERENTE  (solo lectura sobre tablas y vistas de reportes,
--                  mas ejecucion de procedimientos de reporte)
-- ---------------------------------------------------------------------
DROP USER IF EXISTS 'pil_gerente'@'localhost';
CREATE USER 'pil_gerente'@'localhost' IDENTIFIED BY 'GerentePil2026*';
GRANT SELECT ON pil_andina.v_stock_por_planta   TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.v_proximos_vencer    TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.v_pedidos_pendientes TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.v_bajo_stock         TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.producto             TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.inventario           TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.lote                 TO 'pil_gerente'@'localhost';
GRANT SELECT ON pil_andina.pedido               TO 'pil_gerente'@'localhost';
GRANT EXECUTE ON PROCEDURE pil_andina.sp_rotacion_producto TO 'pil_gerente'@'localhost';

-- ---------------------------------------------------------------------
-- ROL 3: DISTRIBUIDOR  (lectura de stock disponible y de sus pedidos;
--                       insercion de pedidos)
-- ---------------------------------------------------------------------
DROP USER IF EXISTS 'pil_distri'@'localhost';
CREATE USER 'pil_distri'@'localhost' IDENTIFIED BY 'DistriPil2026*';
GRANT SELECT ON pil_andina.v_stock_por_planta TO 'pil_distri'@'localhost';
GRANT SELECT ON pil_andina.producto           TO 'pil_distri'@'localhost';
GRANT SELECT, INSERT ON pil_andina.pedido         TO 'pil_distri'@'localhost';
GRANT SELECT, INSERT ON pil_andina.detalle_pedido TO 'pil_distri'@'localhost';

FLUSH PRIVILEGES;

-- ---------------------------------------------------------------------
-- Verificacion de privilegios
-- ---------------------------------------------------------------------
-- SHOW GRANTS FOR 'pil_admin'@'localhost';
-- SHOW GRANTS FOR 'pil_gerente'@'localhost';
-- SHOW GRANTS FOR 'pil_distri'@'localhost';
