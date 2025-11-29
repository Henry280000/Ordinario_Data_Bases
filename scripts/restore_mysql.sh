#!/bin/bash

# ============================================
# Script de Restauración de MySQL
# Sistema de Comercio Electrónico
# ============================================

if [ $# -eq 0 ]; then
    echo "Uso: ./restore_mysql.sh <archivo_backup.sql.gz>"
    echo ""
    echo "Backups disponibles:"
    ls -lh /app/scripts/backups/mysql/
    exit 1
fi

BACKUP_FILE=$1

# Verificar que el archivo existe
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: El archivo ${BACKUP_FILE} no existe"
    exit 1
fi

# Variables de entorno
DB_HOST="${MYSQL_HOST:-mysql_db}"
DB_PORT="${MYSQL_PORT:-3306}"
DB_NAME="${MYSQL_DATABASE:-ecommerce_db}"
DB_USER="${MYSQL_USER:-ecommerce_user}"
DB_PASS="${MYSQL_PASSWORD:-ecommerce_pass}"

echo "============================================"
echo "Restaurando backup de MySQL"
echo "Archivo: ${BACKUP_FILE}"
echo "Base de datos: ${DB_NAME}"
echo "============================================"

# Advertencia
read -p "¿Está seguro de que desea restaurar este backup? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Restauración cancelada"
    exit 0
fi

# Descomprimir y restaurar
gunzip < ${BACKUP_FILE} | mysql -h ${DB_HOST} \
                                 -P ${DB_PORT} \
                                 -u ${DB_USER} \
                                 -p${DB_PASS} \
                                 ${DB_NAME}

if [ $? -eq 0 ]; then
    echo "✓ Base de datos restaurada exitosamente"
    exit 0
else
    echo "✗ Error al restaurar la base de datos"
    exit 1
fi
