"""
Script de Python para automatizar respaldos
Puede ser ejecutado con cron o como tarea programada
"""

import os
import subprocess
import logging
from datetime import datetime
import schedule
import time

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/scripts/backups/backup.log'),
        logging.StreamHandler()
    ]
)

def ejecutar_backup_completo():
    """Ejecuta el script de backup completo"""
    logging.info("=" * 50)
    logging.info("Iniciando respaldo automático del sistema")
    logging.info("=" * 50)
    
    try:
        # Ejecutar script de bash
        result = subprocess.run(
            ['bash', '/app/scripts/backup_complete.sh'],
            capture_output=True,
            text=True,
            check=True
        )
        
        logging.info("STDOUT:")
        logging.info(result.stdout)
        
        if result.stderr:
            logging.warning("STDERR:")
            logging.warning(result.stderr)
        
        logging.info("✓ Respaldo completado exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"✗ Error al ejecutar el backup: {e}")
        logging.error(f"STDOUT: {e.stdout}")
        logging.error(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"✗ Error inesperado: {e}")
        return False

def backup_manual():
    """Ejecutar backup manualmente"""
    print("Ejecutando backup manual...")
    ejecutar_backup_completo()

def backup_programado():
    """Configurar backup automático cada día a las 2:00 AM"""
    schedule.every().day.at("02:00").do(ejecutar_backup_completo)
    
    logging.info("Servicio de backup automático iniciado")
    logging.info("Próximo backup programado: Todos los días a las 2:00 AM")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

if __name__ == "__main__":
    import sys
    
    # Crear directorios de backup si no existen
    os.makedirs('/app/scripts/backups/mysql', exist_ok=True)
    os.makedirs('/app/scripts/backups/mongodb', exist_ok=True)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'manual':
        # Modo manual
        backup_manual()
    else:
        # Modo programado
        backup_programado()
