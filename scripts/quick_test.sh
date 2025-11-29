#!/bin/bash

# ============================================
# Script de Quick Test
# Verifica rápidamente que todo funcione
# ============================================

echo "============================================"
echo "QUICK TEST - Sistema de E-Commerce"
echo "============================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de tests
PASSED=0
FAILED=0

# Función para test
test_command() {
    local description=$1
    local command=$2
    
    echo -n "Testing: $description... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi
}

echo "1. Verificando servicios Docker..."
echo "-----------------------------------"
test_command "Docker está corriendo" "docker info"
test_command "Contenedor backend activo" "docker ps | grep backend_ecommerce"
test_command "Contenedor MySQL activo" "docker ps | grep mysql_ecommerce"
test_command "Contenedor MongoDB activo" "docker ps | grep mongodb_ecommerce"
echo ""

echo "2. Verificando conectividad..."
echo "-----------------------------------"
test_command "API Health Check" "curl -s http://localhost:5001/api/health | grep -q running"
test_command "Frontend accesible" "curl -s http://localhost:5001 | grep -q Jerseys"
echo ""

echo "3. Verificando MySQL..."
echo "-----------------------------------"
test_command "MySQL responde" "docker exec mysql_ecommerce mysqladmin -u root -prootpassword ping | grep -q alive"
test_command "Base de datos existe" "docker exec mysql_ecommerce mysql -u root -prootpassword -e 'USE ecommerce_db;'"
test_command "Tabla Usuarios existe" "docker exec mysql_ecommerce mysql -u root -prootpassword ecommerce_db -e 'SELECT COUNT(*) FROM Usuarios;' | grep -q '[0-9]'"
test_command "Tabla Inventario existe" "docker exec mysql_ecommerce mysql -u root -prootpassword ecommerce_db -e 'SELECT COUNT(*) FROM Inventario;' | grep -q '[0-9]'"
echo ""

echo "4. Verificando MongoDB..."
echo "-----------------------------------"
test_command "MongoDB responde" "docker exec mongodb_ecommerce mongosh -u admin -p adminpassword --authenticationDatabase admin --eval 'db.adminCommand({ ping: 1 })' --quiet | grep -q ok"
test_command "Base de datos existe" "docker exec mongodb_ecommerce mongosh -u admin -p adminpassword --authenticationDatabase admin --eval 'db.getName()' ecommerce_catalog --quiet | grep -q ecommerce_catalog"
test_command "Colección jerseys existe" "docker exec mongodb_ecommerce mongosh -u admin -p adminpassword --authenticationDatabase admin --eval 'db.jerseys.countDocuments()' ecommerce_catalog --quiet | grep -q '[0-9]'"
echo ""

echo "5. Verificando API Endpoints..."
echo "-----------------------------------"
test_command "GET /api/jerseys" "curl -s http://localhost:5001/api/jerseys | grep -q jerseys"
test_command "GET /api/inventario (con auth)" "curl -s -H 'Authorization: Bearer test' http://localhost:5001/api/inventario"
echo ""

echo "6. Verificando archivos de proyecto..."
echo "-----------------------------------"
test_command "Backend app.py existe" "[ -f backend/app.py ]"
test_command "Frontend index.html existe" "[ -f frontend/index.html ]"
test_command "MySQL schema existe" "[ -f database/mysql/01-schema.sql ]"
test_command "MongoDB init existe" "[ -f database/mongodb/01-init.js ]"
test_command "Scripts de backup existen" "[ -f scripts/backup_complete.sh ]"
echo ""

echo "7. Verificando datos de prueba..."
echo "-----------------------------------"
test_command "Usuarios de prueba cargados" "docker exec mysql_ecommerce mysql -u root -prootpassword ecommerce_db -e 'SELECT COUNT(*) FROM Usuarios;' | grep -E '[3-9]|[1-9][0-9]'"
test_command "Productos en inventario" "docker exec mysql_ecommerce mysql -u root -prootpassword ecommerce_db -e 'SELECT COUNT(*) FROM Inventario;' | grep -E '[1-9][0-9]'"
test_command "Jerseys en catálogo" "docker exec mongodb_ecommerce mongosh -u admin -p adminpassword --authenticationDatabase admin --eval 'db.jerseys.countDocuments()' ecommerce_catalog --quiet | grep -E '[6-9]|[1-9][0-9]'"
echo ""

echo "============================================"
echo "RESULTADOS"
echo "============================================"
echo -e "${GREEN}Tests Pasados: $PASSED${NC}"
echo -e "${RED}Tests Fallidos: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Todos los tests pasaron. Sistema listo para demo!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Algunos tests fallaron. Revisar logs:${NC}"
    echo "docker-compose logs"
    exit 1
fi
