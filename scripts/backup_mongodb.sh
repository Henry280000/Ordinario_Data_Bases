#!/bin/bash

# ============================================
# Script de Respaldo MongoDB
# Sistema de Comercio Electrónico
# ============================================

# Configuración
BACKUP_DIR="/app/scripts/backups/mongodb"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="mongodb_backup_${TIMESTAMP}"

# Variables de entorno de Docker
DB_HOST="${MONGODB_HOST:-mongodb_db}"
DB_PORT="${MONGODB_PORT:-27017}"
DB_NAME="${MONGODB_DATABASE:-ecommerce_catalog}"
DB_USER="${MONGODB_USER:-admin}"
DB_PASS="${MONGODB_PASSWORD:-adminpassword}"

echo "============================================"
echo "Iniciando respaldo de MongoDB"
echo "Fecha: $(date)"
echo "============================================"

# Crear directorio de backups si no existe
mkdir -p ${BACKUP_DIR}

# Realizar backup con mongodump
mongodump --host ${DB_HOST} \
          --port ${DB_PORT} \
          --username ${DB_USER} \
          --password ${DB_PASS} \
          --authenticationDatabase admin \
          --db ${DB_NAME} \
          --out ${BACKUP_DIR}/${BACKUP_NAME}

# Verificar si el backup fue exitoso
if [ $? -eq 0 ]; then
    echo "✓ Backup de MongoDB creado exitosamente: ${BACKUP_NAME}"
    
    # Comprimir el directorio
    cd ${BACKUP_DIR}
    tar -czf ${BACKUP_NAME}.tar.gz ${BACKUP_NAME}
    
    # Eliminar directorio sin comprimir
    rm -rf ${BACKUP_NAME}
    
    echo "✓ Backup comprimido: ${BACKUP_NAME}.tar.gz"
    
    # Mostrar tamaño del archivo
    BACKUP_SIZE=$(du -h ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz | cut -f1)
    echo "✓ Tamaño del backup: ${BACKUP_SIZE}"
    
    # Limpiar backups antiguos (mantener solo los últimos 7 días)
    find ${BACKUP_DIR} -name "mongodb_backup_*.tar.gz" -mtime +7 -delete
    echo "✓ Backups antiguos eliminados (>7 días)"
    
    echo "============================================"
    echo "Backup completado exitosamente"
    echo "============================================"
    exit 0
else
    echo "✗ Error al crear el backup de MongoDB"
    exit 1
fi
