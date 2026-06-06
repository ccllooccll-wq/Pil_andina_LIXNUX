# Pil_andina_LIXNUX
Proyecto para la empresa Pil Andina/evaluación procesual grupal
Descripción
Repositorio desarrollado por el grupo LIXNUX para la gestión y desarrollo de proyectos académicos y de software.
Integrantes
-Sofya Grisel Zutin Castro Helguero
-Oscar Alejandro Zambrana Saavedra
-Marcelo Calle Mamani
 Instrucciones de Instalación
Requisitos previos
MySQL 8.x (o XAMPP con MySQL 8). Descargar XAMPP
Python 3.10 o superior. Descargar Python
pip actualizado: python -m pip install --upgrade pip


Paso 1  Crear la base de datos
Abre una terminal y ejecuta los scripts en orden. Si usas XAMPP, reemplaza mysql por la ruta completa (p. ej. C:\xampp\mysql\bin\mysql.exe).
bashmysql -u root -p < database/01_esquema.sql
mysql -u root -p < database/02_datos.sql
mysql -u root -p < database/03_objetos.sql
mysql -u root -p < database/04_usuarios_roles.sql
mysql -u root -p < database/05_passwords.sql
¿Sin contraseña de root? Omite el flag -p o deja el campo vacío cuando se solicite.
Verifica que todo quedó correcto:
sqlUSE pil_andina;
SHOW TABLES;         Deben aparecer 14 tablas
SHOW FULL TABLES WHERE Table_type = 'VIEW';  Deben aparecer 4 vistas
Paso 2 — Configurar el entorno Python
Desde la carpeta app/, crea un entorno virtual e instala las dependencias:
bashcd app
 Crear entorno virtual
python -m venv venv

 Activar (Linux / macOS)
source venv/bin/activate

Activar (Windows)
venv\Scripts\activate

 Instalar dependencias
pip install -r requirements.txt

Paso 3 Configurar variables de entorno
Copia el archivo de ejemplo y ajusta los valores si tu MySQL usa credenciales distintas:
bashcp .env.example .env
Contenido de .env (editar según tu instalación):
envSECRET_KEY=cambiar-esta-clave-en-produccion
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=           dejar vacío si root no tiene contraseña
DB_NAME=pil_andina
MYSQLDUMP=mysqldump    ruta completa si no está en el PATH
MYSQL_BIN=mysql

XAMPP en Windows (ejemplo):
envMYSQLDUMP=C:\xampp\mysql\bin\mysqldump.exe
MYSQL_BIN=C:\xampp\mysql\bin\mysql.exe
Paso 4 Ejecutar la aplicación
bashpython app.py
La aplicación queda disponible en: http://localhost:5000
(Opcional) Backup automático programado
Linux/macOS — cron:
bash# Ejecutar todos los días a las 02:00 AM
0 2 * * * /ruta/absoluta/pil_andina/database/backup_automatico.sh
Windows — Programador de tareas:
Apunta a backup_automatico.sh usando Git Bash como intérprete.
El script guarda el respaldo comprimido en backups/ y conserva únicamente los últimos 7 archivos.
Credenciales de Acceso 
rol: Administrador correo:admin@pilandina.bo contraseña:admin123 Permisos principales:Acceso total: CRUD, backups, monitoreo, usuarios
rol: Gerente correo:gerente@pilandina.bo contraseña:gerente123 Permisos principales:Lectura de reportes y vistas; ejecuta rotación de inventario
rol: Distribuidor correo:distri@pilandina.bo contraseña:distri123 Permisos principales:Consulta stock; crea y visualiza sus pedidos

