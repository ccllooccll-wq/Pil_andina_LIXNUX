-- =====================================================================
-- Archivo 03: Vistas, Procedimientos, Triggers e Indices
-- =====================================================================
USE pil_andina;

-- =====================================================================
-- VISTAS (minimo 3)
-- =====================================================================

-- VISTA 1: Stock consolidado por producto y planta
CREATE OR REPLACE VIEW v_stock_por_planta AS
SELECT  pl.nombre              AS planta,
        p.codigo               AS codigo,
        p.nombre_comercial     AS producto,
        p.presentacion         AS presentacion,
        SUM(i.cantidad_actual) AS stock_total,
        p.stock_minimo         AS stock_minimo
FROM inventario i
JOIN producto p ON p.id_producto = i.id_producto
JOIN bodega   b ON b.id_bodega   = i.id_bodega
JOIN planta   pl ON pl.id_planta = b.id_planta
GROUP BY pl.nombre, p.codigo, p.nombre_comercial, p.presentacion, p.stock_minimo;

-- VISTA 2: Productos proximos a vencer (proximos 30 dias)
CREATE OR REPLACE VIEW v_proximos_vencer AS
SELECT  l.numero_lote,
        p.nombre_comercial AS producto,
        p.presentacion,
        l.fecha_vencimiento,
        DATEDIFF(l.fecha_vencimiento, CURDATE()) AS dias_restantes,
        SUM(i.cantidad_actual) AS unidades
FROM lote l
JOIN producto p   ON p.id_producto = l.id_producto
JOIN inventario i ON i.id_lote     = l.id_lote
WHERE l.fecha_vencimiento BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
GROUP BY l.numero_lote, p.nombre_comercial, p.presentacion, l.fecha_vencimiento;

-- VISTA 3: Pedidos pendientes por distribuidor con monto
CREATE OR REPLACE VIEW v_pedidos_pendientes AS
SELECT  d.razon_social     AS distribuidor,
        d.ciudad,
        ped.id_pedido,
        ped.fecha_pedido,
        ped.fecha_entrega_requerida,
        ped.estado,
        COALESCE(SUM(dp.subtotal),0) AS monto_pedido
FROM pedido ped
JOIN distribuidor d   ON d.id_distribuidor = ped.id_distribuidor
LEFT JOIN detalle_pedido dp ON dp.id_pedido = ped.id_pedido
WHERE ped.estado IN ('Pendiente','Despachado')
GROUP BY d.razon_social, d.ciudad, ped.id_pedido, ped.fecha_pedido,
         ped.fecha_entrega_requerida, ped.estado;

-- VISTA 4 (extra): Productos bajo stock minimo
CREATE OR REPLACE VIEW v_bajo_stock AS
SELECT  p.codigo, p.nombre_comercial AS producto, p.presentacion,
        SUM(i.cantidad_actual) AS stock_actual, p.stock_minimo
FROM producto p
JOIN inventario i ON i.id_producto = p.id_producto
GROUP BY p.codigo, p.nombre_comercial, p.presentacion, p.stock_minimo
HAVING SUM(i.cantidad_actual) <= p.stock_minimo;

-- =====================================================================
-- PROCEDIMIENTOS ALMACENADOS (minimo 2)
-- =====================================================================
DELIMITER //

-- PROC 1: Registrar un movimiento de inventario y actualizar stock
CREATE PROCEDURE sp_registrar_movimiento(
    IN  p_id_inventario INT,
    IN  p_tipo          VARCHAR(10),   -- 'Entrada' | 'Salida'
    IN  p_cantidad      INT,
    IN  p_motivo        VARCHAR(120),
    IN  p_id_usuario    INT
)
BEGIN
    DECLARE v_stock INT;

    -- Bloqueo de fila para evitar condiciones de carrera
    SELECT cantidad_actual INTO v_stock
    FROM inventario WHERE id_inventario = p_id_inventario FOR UPDATE;

    IF p_tipo = 'Salida' AND v_stock < p_cantidad THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente para la salida solicitada';
    END IF;

    IF p_tipo = 'Entrada' THEN
        UPDATE inventario SET cantidad_actual = cantidad_actual + p_cantidad
        WHERE id_inventario = p_id_inventario;
    ELSE
        UPDATE inventario SET cantidad_actual = cantidad_actual - p_cantidad
        WHERE id_inventario = p_id_inventario;
    END IF;

    INSERT INTO movimiento (id_inventario, tipo_movimiento, cantidad, motivo, id_usuario)
    VALUES (p_id_inventario, p_tipo, p_cantidad, p_motivo, p_id_usuario);
END //

-- PROC 2: Rotacion de inventario por producto (comparativa de salidas entre meses)
CREATE PROCEDURE sp_rotacion_producto(
    IN p_anio INT,
    IN p_mes  INT
)
BEGIN
    SELECT  p.nombre_comercial AS producto,
            p.presentacion,
            SUM(CASE WHEN m.tipo_movimiento='Salida'
                     AND YEAR(m.fecha_movimiento)=p_anio
                     AND MONTH(m.fecha_movimiento)=p_mes
                     THEN m.cantidad ELSE 0 END) AS salidas_mes_actual,
            SUM(CASE WHEN m.tipo_movimiento='Salida'
                     AND ( (p_mes=1 AND YEAR(m.fecha_movimiento)=p_anio-1 AND MONTH(m.fecha_movimiento)=12)
                        OR (p_mes>1 AND YEAR(m.fecha_movimiento)=p_anio AND MONTH(m.fecha_movimiento)=p_mes-1) )
                     THEN m.cantidad ELSE 0 END) AS salidas_mes_anterior
    FROM producto p
    JOIN inventario i ON i.id_producto = p.id_producto
    JOIN movimiento m ON m.id_inventario = i.id_inventario
    GROUP BY p.nombre_comercial, p.presentacion;
END //

DELIMITER ;

-- =====================================================================
-- TRIGGERS (minimo 2)
-- =====================================================================
DELIMITER //

-- TRIGGER 1: Auditoria automatica de cambios de precio en producto
CREATE TRIGGER trg_audit_precio
AFTER UPDATE ON producto
FOR EACH ROW
BEGIN
    IF OLD.precio_actual <> NEW.precio_actual THEN
        INSERT INTO auditoria (id_usuario, accion, tabla_afectada, descripcion)
        VALUES (NULL, 'UPDATE', 'producto',
                CONCAT('Producto ', NEW.codigo, ': precio ', OLD.precio_actual,
                       ' -> ', NEW.precio_actual));
    END IF;
END //

-- TRIGGER 2: Control de stock - evita cantidades negativas en inventario
CREATE TRIGGER trg_control_stock
BEFORE UPDATE ON inventario
FOR EACH ROW
BEGIN
    IF NEW.cantidad_actual < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La cantidad en inventario no puede ser negativa';
    END IF;
END //

-- TRIGGER 3 (extra): Registrar en auditoria cada nuevo lote
CREATE TRIGGER trg_audit_lote
AFTER INSERT ON lote
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (id_usuario, accion, tabla_afectada, descripcion)
    VALUES (NULL, 'INSERT', 'lote',
            CONCAT('Nuevo lote ', NEW.numero_lote));
END //

DELIMITER ;

-- =====================================================================
-- INDICES ESTRATEGICOS (minimo 3 - justificados en el documento)
-- =====================================================================

-- IDX 1: Busqueda y reportes de lotes por fecha de vencimiento (alertas)
CREATE INDEX idx_lote_vencimiento ON lote (fecha_vencimiento);

-- IDX 2: Filtrado de movimientos por fecha (kardex y rotacion)
CREATE INDEX idx_mov_fecha ON movimiento (fecha_movimiento);

-- IDX 3: Busqueda de productos por nombre comercial (busquedas avanzadas)
CREATE INDEX idx_producto_nombre ON producto (nombre_comercial);

-- IDX 4 (extra): pedidos por estado (reporte de pendientes)
CREATE INDEX idx_pedido_estado ON pedido (estado);
