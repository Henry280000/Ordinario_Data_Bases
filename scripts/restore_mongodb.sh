#!/bin/bash

# ============================================
# Script de Restauración de MongoDB
# Sistema de Comercio Electrónico
# ============================================

if [ $# -eq 0 ]; then
    echo "Uso: ./restore_mongodb.sh <archivo_backup.tar.gz>"
    echo ""
    echo "Backups disponibles:"
    ls -lh /app/scripts/backups/mongodb/
    exit 1
fi

BACKUP_FILE=$1

# Verificar que el archivo existe
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: El archivo ${BACKUP_FILE} no existe"
    exit 1
fi

# Variables de entorno
DB_HOST="${MONGODB_HOST:-mongodb_db}"
DB_PORT="${MONGODB_PORT:-27017}"
DB_NAME="${MONGODB_DATABASE:-ecommerce_catalog}"
DB_USER="${MONGODB_USER:-admin}"
DB_PASS="${MONGODB_PASSWORD:-adminpassword}"

TEMP_DIR="/tmp/mongodb_restore_$$"

echo "============================================"
echo "Restaurando backup de MongoDB"
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

# Crear directorio temporal
mkdir -p ${TEMP_DIR}

# Descomprimir
tar -xzf ${BACKUP_FILE} -C ${TEMP_DIR}

# Encontrar el directorio de la base de datos
RESTORE_DIR=$(find ${TEMP_DIR} -type d -name ${DB_NAME})

if [ -z "${RESTORE_DIR}" ]; then
    echo "Error: No se encontró el directorio de la base de datos en el backup"
    rm -rf ${TEMP_DIR}
    exit 1
fi

# Restaurar con mongorestore
mongorestore --host ${DB_HOST} \
             --port ${DB_PORT} \
             --username ${DB_USER} \
             --password ${DB_PASS} \
             --authenticationDatabase admin \
             --db ${DB_NAME} \
             --drop \
             ${RESTORE_DIR}

if [ $? -eq 0 ]; then
    echo "✓ Base de datos restaurada exitosamente"
    rm -rf ${TEMP_DIR}
    exit 0
else
    echo "✗ Error al restaurar la base de datos"
    rm -rf ${TEMP_DIR}
    exit 1
fi
