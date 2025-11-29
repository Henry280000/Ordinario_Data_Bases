#!/usr/bin/env python3
"""
Script para sincronizar inventario de MongoDB a MySQL
Carga los productos de MongoDB y crea registros de inventario en MySQL
"""

import sys
import os
sys.path.append('/app')

from db_mysql import MySQLConnection
from db_mongodb import MongoDBConnection

def sync_inventory():
    """Sincroniza inventario de MongoDB a MySQL"""
    
    mysql = MySQLConnection()
    mongo = MongoDBConnection()
    
    print("=" * 60)
    print("SINCRONIZACIÓN DE INVENTARIO: MongoDB -> MySQL")
    print("=" * 60)
    
    try:
        # Obtener todos los jerseys de MongoDB
        jerseys = list(mongo.db.jerseys.find())
        print(f"\n✓ Encontrados {len(jerseys)} productos en MongoDB")
        
        # Mapeo de productos MongoDB a inventario MySQL
        inventory_mapping = {
            'jersey_rm_home_2024': [
                ('RM-HOME-2024-S', 'S', 50),
                ('RM-HOME-2024-M', 'M', 75),
                ('RM-HOME-2024-L', 'L', 100),
                ('RM-HOME-2024-XL', 'XL', 60)
            ],
            'jersey_bar_home_2024': [
                ('BAR-HOME-2024-S', 'S', 45),
                ('BAR-HOME-2024-M', 'M', 80),
                ('BAR-HOME-2024-L', 'L', 90),
                ('BAR-HOME-2024-XL', 'XL', 55)
            ],
            'jersey_man_home_2024': [
                ('MU-HOME-2024-S', 'S', 40),
                ('MU-HOME-2024-M', 'M', 70),
                ('MU-HOME-2024-L', 'L', 85),
                ('MU-HOME-2024-XL', 'XL', 50)
            ],
            'jersey_liv_home_2024': [
                ('LIV-HOME-2024-S', 'S', 55),
                ('LIV-HOME-2024-M', 'M', 85),
                ('LIV-HOME-2024-L', 'L', 95),
                ('LIV-HOME-2024-XL', 'XL', 65)
            ],
            'jersey_psg_home_2024': [
                ('PSG-HOME-2024-S', 'S', 35),
                ('PSG-HOME-2024-M', 'M', 60),
                ('PSG-HOME-2024-L', 'L', 75),
                ('PSG-HOME-2024-XL', 'XL', 45)
            ],
            'jersey_bay_home_2024': [
                ('BAY-HOME-2024-S', 'S', 42),
                ('BAY-HOME-2024-M', 'M', 68),
                ('BAY-HOME-2024-L', 'L', 82),
                ('BAY-HOME-2024-XL', 'XL', 52)
            ]
        }
        
        connection = mysql.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Limpiar inventario existente (opcional)
        print("\n⚠ Limpiando inventario existente...")
        cursor.execute("DELETE FROM Inventario WHERE id_inventario > 10")
        connection.commit()
        
        items_added = 0
        
        # Insertar inventario para cada jersey
        for jersey in jerseys:
            product_id = jersey['_id']
            product_name = jersey['nombre']
            precio = float(jersey['precio_base'])
            
            if product_id in inventory_mapping:
                print(f"\n→ Procesando: {product_name}")
                
                for sku, talla, stock in inventory_mapping[product_id]:
                    try:
                        # Verificar si ya existe
                        cursor.execute("SELECT id_inventario FROM Inventario WHERE sku = %s", (sku,))
                        existing = cursor.fetchone()
                        
                        if existing:
                            # Actualizar stock existente
                            cursor.execute("""
                                UPDATE Inventario 
                                SET cantidad_disponible = %s, precio_unitario = %s
                                WHERE sku = %s
                            """, (stock, precio, sku))
                            print(f"  ✓ Actualizado: {sku} ({talla}) - Stock: {stock}")
                        else:
                            # Insertar nuevo
                            cursor.execute("""
                                INSERT INTO Inventario 
                                (sku, producto_id, nombre_producto, talla, cantidad_disponible, precio_unitario)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (sku, product_id, product_name, talla, stock, precio))
                            print(f"  ✓ Agregado: {sku} ({talla}) - Stock: {stock}")
                        
                        items_added += 1
                        
                    except Exception as e:
                        print(f"  ✗ Error con {sku}: {e}")
                        connection.rollback()
                        continue
                
                connection.commit()
        
        # Mostrar resumen
        cursor.execute("SELECT COUNT(*) as total FROM Inventario")
        total = cursor.fetchone()['total']
        
        print("\n" + "=" * 60)
        print(f"✓ SINCRONIZACIÓN COMPLETADA")
        print(f"  Items procesados: {items_added}")
        print(f"  Total en inventario: {total}")
        print("=" * 60)
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error en sincronización: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = sync_inventory()
    sys.exit(0 if success else 1)
