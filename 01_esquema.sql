-- =====================================================================
-- Archivo 02: Datos de prueba (DML)
-- Mínimo 10 registros por tabla principal
-- =====================================================================
USE pil_andina;

-- ---------------------- ROLES ----------------------
INSERT INTO rol (nombre, descripcion) VALUES
('Administrador','Acceso total al sistema'),
('Gerente','Reportes, dashboard y consultas gerenciales'),
('Distribuidor','Consulta de stock y gestion de sus pedidos');

-- ---------------------- USUARIOS ----------------------
-- NOTA: el hash corresponde a la contrasena 'admin123', 'gerente123', etc.
-- Generados con werkzeug.security.generate_password_hash (pbkdf2:sha256)
-- En produccion se generan desde la app. Aqui se incluyen ya hasheados.
INSERT INTO usuario (nombre, correo, password_hash, id_rol) VALUES
('Admin General','admin@pilandina.bo','pbkdf2:sha256:600000$seed01$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1),
('Maria Gerente','gerente@pilandina.bo','pbkdf2:sha256:600000$seed02$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',2),
('Carlos Distribuidor','distri@pilandina.bo','pbkdf2:sha256:600000$seed03$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',3),
('Ana Lopez','ana@pilandina.bo','pbkdf2:sha256:600000$seed04$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',2),
('Jorge Ramirez','jorge@pilandina.bo','pbkdf2:sha256:600000$seed05$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',3),
('Lucia Vargas','lucia@pilandina.bo','pbkdf2:sha256:600000$seed06$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',2),
('Pedro Soto','pedro@pilandina.bo','pbkdf2:sha256:600000$seed07$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',3),
('Sofia Mendez','sofia@pilandina.bo','pbkdf2:sha256:600000$seed08$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',2),
('Raul Flores','raul@pilandina.bo','pbkdf2:sha256:600000$seed09$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',3),
('Elena Quispe','elena@pilandina.bo','pbkdf2:sha256:600000$seed10$8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',1);

-- ---------------------- PRODUCTOS ----------------------
INSERT INTO producto (codigo, nombre_comercial, tipo, presentacion, graduacion_alcoholica, precio_actual, stock_minimo, stock_maximo) VALUES
('PAC355','Pacena','Lager','355ml',5.00,7.50,500,50000),
('PAC620','Pacena','Lager','620ml',5.00,12.00,400,40000),
('TAQ620','Taquina','Pilsener','620ml',4.80,11.50,300,30000),
('HUA620','Huari','Lager','620ml',5.20,13.00,300,30000),
('BOC355','Bock','Negra','355ml',6.00,9.00,200,20000),
('REA620','Real','Pilsener','620ml',5.00,10.50,250,25000),
('IMP620','Imperial','Lager','620ml',4.90,10.00,250,25000),
('POT620','Potosina','Pilsener','620ml',4.70,9.50,200,20000),
('COP1L','Copacabana','Malta','1L',0.50,8.00,150,15000),
('MAL355','Maltin','Malta','355ml',0.00,5.50,150,15000);

-- ---------------------- PLANTAS ----------------------
INSERT INTO planta (nombre, ciudad, ubicacion) VALUES
('Planta La Paz','La Paz','Mecapaca'),
('Planta Cochabamba','Cochabamba','Sacaba'),
('Planta Santa Cruz','Santa Cruz','Palmasola');

-- ---------------------- BODEGAS ----------------------
INSERT INTO bodega (id_planta, nombre, tipo, ubicacion_fisica, capacidad_maxima, temperatura_almacenamiento) VALUES
(1,'Bodega PT La Paz','Producto Terminado','Galpon A',100000,18.0),
(1,'Bodega Refrig La Paz','Refrigerado','Camara 1',30000,4.0),
(1,'Bodega Insumos La Paz','Insumos','Galpon B',50000,20.0),
(2,'Bodega PT Cbba','Producto Terminado','Galpon A',90000,18.0),
(2,'Bodega Refrig Cbba','Refrigerado','Camara 1',25000,4.0),
(2,'Bodega Insumos Cbba','Insumos','Galpon B',40000,20.0),
(3,'Bodega PT Santa Cruz','Producto Terminado','Galpon A',120000,18.0),
(3,'Bodega Refrig SC','Refrigerado','Camara 1',35000,4.0),
(3,'Bodega Insumos SC','Insumos','Galpon B',60000,20.0),
(1,'Bodega Despacho La Paz','Producto Terminado','Anden 1',20000,18.0);

-- ---------------------- LOTES ----------------------
INSERT INTO lote (numero_lote, id_producto, id_planta, fecha_produccion, fecha_vencimiento, cantidad_producida) VALUES
('L-PAC355-001',1,1,'2026-01-10','2026-07-10',20000),
('L-PAC620-001',2,1,'2026-01-12','2026-07-12',15000),
('L-TAQ620-001',3,2,'2026-02-01','2026-08-01',12000),
('L-HUA620-001',4,2,'2026-02-05','2026-08-05',10000),
('L-BOC355-001',5,1,'2026-02-10','2026-06-15',8000),
('L-REA620-001',6,3,'2026-03-01','2026-09-01',9000),
('L-IMP620-001',7,3,'2026-03-03','2026-09-03',9500),
('L-POT620-001',8,2,'2026-03-10','2026-06-20',7000),
('L-COP1L-001',9,1,'2026-03-15','2026-09-15',6000),
('L-MAL355-001',10,3,'2026-03-20','2026-06-10',5000);

-- ---------------------- CONTROL DE CALIDAD ----------------------
INSERT INTO control_calidad (id_lote, resultado, tecnico_responsable, observaciones, fecha_control) VALUES
(1,'Aprobado','Ing. Mamani','Parametros normales','2026-01-11'),
(2,'Aprobado','Ing. Mamani','OK','2026-01-13'),
(3,'Aprobado','Ing. Choque','OK','2026-02-02'),
(4,'Aprobado','Ing. Choque','OK','2026-02-06'),
(5,'Rechazado','Ing. Mamani','Exceso de espuma','2026-02-11'),
(6,'Aprobado','Ing. Rojas','OK','2026-03-02'),
(7,'Aprobado','Ing. Rojas','OK','2026-03-04'),
(8,'Aprobado','Ing. Choque','OK','2026-03-11'),
(9,'Aprobado','Ing. Mamani','OK','2026-03-16'),
(10,'Aprobado','Ing. Rojas','OK','2026-03-21');

-- ---------------------- INVENTARIO ----------------------
INSERT INTO inventario (id_producto, id_lote, id_bodega, cantidad_actual) VALUES
(1,1,1,18000),
(2,2,1,14000),
(3,3,4,11000),
(4,4,4,9500),
(5,5,1,300),     -- bajo stock minimo (200) -> casi al limite
(6,6,7,8500),
(7,7,7,9000),
(8,8,4,150),     -- por debajo del minimo (200)
(9,9,1,5800),
(10,10,7,4800);

-- ---------------------- DISTRIBUIDORES ----------------------
INSERT INTO distribuidor (nit, razon_social, direccion, ciudad, zona, contacto, telefono, correo) VALUES
('1023456789','Distribuidora Andina SRL','Av. 6 de Agosto 234','La Paz','Sur','Luis Perez','77712345','andina@dist.bo'),
('1023456790','Bebidas del Valle','Av. America 1200','Cochabamba','Norte','Marta Rios','77723456','valle@dist.bo'),
('1023456791','Comercial Oriente','Av. Banzer 3000','Santa Cruz','Este','Juan Vaca','77734567','oriente@dist.bo'),
('1023456792','El Alto Bebidas','Av. 6 de Marzo 500','El Alto','Ceja','Rosa Mamani','77745678','elalto@dist.bo'),
('1023456793','Distribuidora Sur','Calle Sucre 88','Tarija','Centro','Carlos Gil','77756789','sur@dist.bo'),
('1023456794','Mayorista Potosi','Av. Universitaria 10','Potosi','Centro','Ana Soto','77767890','potosi@dist.bo'),
('1023456795','Bebidas Oruro','Calle Bolivar 45','Oruro','Centro','Pedro Lima','77778901','oruro@dist.bo'),
('1023456796','Distribuidora Beni','Av. 9 de Abril 77','Trinidad','Centro','Sara Roca','77789012','beni@dist.bo'),
('1023456797','Comercial Chuquisaca','Calle Junin 23','Sucre','Centro','Mario Paz','77790123','sucre@dist.bo'),
('1023456798','Pando Bebidas','Av. Internacional 5','Cobija','Centro','Lia Suarez','77701234','pando@dist.bo');

-- ---------------------- PEDIDOS ----------------------
INSERT INTO pedido (id_distribuidor, fecha_pedido, fecha_entrega_requerida, estado) VALUES
(1,'2026-05-01','2026-05-05','Entregado'),
(2,'2026-05-03','2026-05-08','Despachado'),
(3,'2026-05-05','2026-05-10','Pendiente'),
(4,'2026-05-06','2026-05-11','Pendiente'),
(5,'2026-05-07','2026-05-12','Cancelado'),
(6,'2026-05-08','2026-05-13','Entregado'),
(7,'2026-05-09','2026-05-14','Despachado'),
(8,'2026-05-10','2026-05-15','Pendiente'),
(9,'2026-05-11','2026-05-16','Pendiente'),
(10,'2026-05-12','2026-05-17','Entregado');

-- ---------------------- DETALLE DE PEDIDO ----------------------
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario) VALUES
(1,1,500,7.50),
(1,2,300,12.00),
(2,3,400,11.50),
(3,4,200,13.00),
(4,5,150,9.00),
(5,6,250,10.50),
(6,7,300,10.00),
(7,8,200,9.50),
(8,9,150,8.00),
(9,10,150,5.50),
(10,1,600,7.50);

-- ---------------------- FACTURAS ----------------------
INSERT INTO factura (id_pedido, monto_total, estado_pago, fecha_emision) VALUES
(1,7350.00,'Pagado','2026-05-05'),
(2,4600.00,'Pagado','2026-05-08'),
(3,2600.00,'Pendiente','2026-05-10'),
(4,1350.00,'Pendiente','2026-05-11'),
(6,3000.00,'Pagado','2026-05-13'),
(7,1900.00,'Pendiente','2026-05-14'),
(8,1200.00,'Pendiente','2026-05-15'),
(9,825.00,'Pendiente','2026-05-16'),
(10,4500.00,'Pagado','2026-05-17'),
(5,2625.00,'Pendiente','2026-05-12');

-- ---------------------- AUDITORIA (registros iniciales) ----------------------
INSERT INTO auditoria (id_usuario, accion, tabla_afectada, descripcion) VALUES
(1,'LOGIN','usuario','Inicio de sesion admin'),
(2,'LOGIN','usuario','Inicio de sesion gerente'),
(1,'INSERT','producto','Alta producto PAC355'),
(1,'INSERT','lote','Alta lote L-PAC355-001'),
(2,'SELECT','inventario','Consulta de stock'),
(3,'LOGIN','usuario','Inicio de sesion distribuidor'),
(1,'UPDATE','producto','Cambio de precio'),
(2,'SELECT','pedido','Consulta de pedidos pendientes'),
(1,'INSERT','distribuidor','Alta distribuidor Andina'),
(1,'DELETE','detalle_pedido','Eliminacion linea de pedido');
