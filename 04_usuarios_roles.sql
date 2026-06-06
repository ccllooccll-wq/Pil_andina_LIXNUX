#!/bin/bash
# ============================================================
# Backup automatico programado de la BD pil_andina
# Uso en Linux (cron):   0 2 * * *  /ruta/backup_automatico.sh
# Uso en Windows: programar con el Programador de tareas (Git Bash)
# ============================================================
DB_NAME="pil_andina"
DB_USER="pil_admin"
DB_PASS="AdminPil2026*"
DEST="$(dirname "$0")/../backups"
mkdir -p "$DEST"
STAMP=$(date +%Y%m%d_%H%M%S)
FILE="$DEST/backup_${DB_NAME}_${STAMP}.sql"

mysqldump -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$FILE"

# Comprimir y conservar solo los ultimos 7 backups
gzip "$FILE"
ls -t "$DEST"/*.sql.gz 2>/dev/null | tail -n +8 | xargs -r rm
echo "Backup creado: ${FILE}.gz"
