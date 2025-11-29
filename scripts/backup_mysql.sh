#!/bin/bash

# ============================================
# Script de Respaldo MySQL
# Sistema de Comercio Electrónico
# ============================================

# Configuración
BACKUP_DIR="/app/scripts/backups/mysql"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="mysql_backup_${TIMESTAMP}.sql"

# Variables de entorno de Docker
DB_HOST="${MYSQL_HOST:-mysql_db}"
DB_PORT="${MYSQL_PORT:-3306}"
DB_NAME="${MYSQL_DATABASE:-ecommerce_db}"
DB_USER="${MYSQL_USER:-ecommerce_user}"
DB_PASS="${MYSQL_PASSWORD:-ecommerce_pass}"

echo "============================================"
echo "Iniciando respaldo de MySQL"
echo "Fecha: $(date)"
echo "============================================"

# Crear directorio de backups si no existe
mkdir -p ${BACKUP_DIR}

# Realizar backup con mysqldump
mysqldump -h ${DB_HOST} \
          -P ${DB_PORT} \
          -u ${DB_USER} \
          -p${DB_PASS} \
          ${DB_NAME} \
          --single-transaction \
          --routines \
          --triggers \
          --events \
          > ${BACKUP_DIR}/${BACKUP_FILE}

# Verificar si el backup fue exitoso
if [ $? -eq 0 ]; then
    echo "✓ Backup de MySQL creado exitosamente: ${BACKUP_FILE}"
    
    # Comprimir el archivo
    gzip ${BACKUP_DIR}/${BACKUP_FILE}
    echo "✓ Backup comprimido: ${BACKUP_FILE}.gz"
    
    # Mostrar tamaño del archivo
    BACKUP_SIZE=$(du -h ${BACKUP_DIR}/${BACKUP_FILE}.gz | cut -f1)
    echo "✓ Tamaño del backup: ${BACKUP_SIZE}"
    
    # Limpiar backups antiguos (mantener solo los últimos 7 días)
    find ${BACKUP_DIR} -name "mysql_backup_*.sql.gz" -mtime +7 -delete
    echo "✓ Backups antiguos eliminados (>7 días)"
    
    echo "============================================"
    echo "Backup completado exitosamente"
    echo "============================================"
    exit 0
else
    echo "✗ Error al crear el backup de MySQL"
    exit 1
fi
