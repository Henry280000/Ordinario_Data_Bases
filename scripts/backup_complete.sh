#!/bin/bash

# ============================================
# Script de Respaldo Completo del Sistema
# Ejecuta backups de MySQL y MongoDB
# ============================================

echo "============================================"
echo "RESPALDO COMPLETO DEL SISTEMA"
echo "Fecha: $(date)"
echo "============================================"
echo ""

# Ejecutar backup de MySQL
echo ">>> Iniciando backup de MySQL..."
bash /app/scripts/backup_mysql.sh

if [ $? -eq 0 ]; then
    echo ">>> MySQL backup completado"
else
    echo ">>> Error en MySQL backup"
fi

echo ""
echo "============================================"
echo ""

# Ejecutar backup de MongoDB
echo ">>> Iniciando backup de MongoDB..."
bash /app/scripts/backup_mongodb.sh

if [ $? -eq 0 ]; then
    echo ">>> MongoDB backup completado"
else
    echo ">>> Error en MongoDB backup"
fi

echo ""
echo "============================================"
echo "RESPALDO COMPLETO FINALIZADO"
echo "Fecha: $(date)"
echo "============================================"

# Mostrar listado de backups
echo ""
echo "Backups disponibles:"
echo ""
echo "MySQL Backups:"
ls -lh /app/scripts/backups/mysql/ | tail -n 5
echo ""
echo "MongoDB Backups:"
ls -lh /app/scripts/backups/mongodb/ | tail -n 5
