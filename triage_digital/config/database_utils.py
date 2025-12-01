#!/usr/bin/env python3
"""
🔗 TRIAGE DIGITAL - DATABASE UTILITIES
=====================================
Utilidades para manejo híbrido de bases de datos (Online/Offline)
"""

import os
import socket
import time
from pathlib import Path

# Cache de estado de conexión (5 minutos)
_connection_cache = {'last_check': 0, 'is_online': False}
_CACHE_DURATION = 300  # 5 minutos en segundos

def check_internet_connection(timeout=2, use_cache=True):
    """
    Verifica si hay conexión a PostgreSQL en Render probando una conexión real.
    
    Args:
        timeout: Tiempo máximo de espera en segundos
        use_cache: Si True, usa resultado cacheado si está disponible
    
    Returns:
        bool: True si hay conexión funcional, False si no hay conexión
    """
    # Forzar modo offline si está configurado
    if os.environ.get('FORCE_OFFLINE') == '1':
        print("🔧 Modo OFFLINE forzado (FORCE_OFFLINE=1)")
        return False
    
    # Usar cache si está disponible y es reciente
    if use_cache:
        current_time = time.time()
        if current_time - _connection_cache['last_check'] < _CACHE_DURATION:
            return _connection_cache['is_online']
    
    # Primero verificar conectividad básica de red
    try:
        # Test rápido de DNS y conectividad
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            ('dpg-d4krad9r0fns738c3nd0-a.oregon-postgres.render.com', 5432)
        )
    except (socket.timeout, socket.error, OSError) as e:
        print(f"⚠️  Sin conexión de red: {type(e).__name__}")
        _connection_cache['last_check'] = time.time()
        _connection_cache['is_online'] = False
        return False
    
    # Si hay conexión de red, probar PostgreSQL
    try:
        import psycopg2
        
        # Intentar una conexión real a PostgreSQL
        conn = psycopg2.connect(
            dbname='triage_digital',
            user='triage_digital_user',
            password='hxuR3HFPIytdMIwQbGGVZ7BIo72H3Yr2',
            host='dpg-d4krad9r0fns738c3nd0-a.oregon-postgres.render.com',
            port='5432',
            sslmode='require',
            connect_timeout=timeout
        )
        conn.close()
        _connection_cache['last_check'] = time.time()
        _connection_cache['is_online'] = True
        return True
        
    except Exception as e:
        print(f"⚠️  PostgreSQL no disponible: {str(e)[:80]}")
        _connection_cache['last_check'] = time.time()
        _connection_cache['is_online'] = False
        return False

def get_database_config():
    """
    Retorna la configuración de base de datos según disponibilidad de conexión.
    
    Returns:
        dict: Configuración de base de datos para Django
    """
    # Verificar conexión
    has_internet = check_internet_connection()
    
    if has_internet:
        print("🌐 Modo ONLINE - Usando PostgreSQL en Render")
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'triage_digital',
                'USER': 'triage_digital_user',
                'PASSWORD': 'hxuR3HFPIytdMIwQbGGVZ7BIo72H3Yr2',
                'HOST': 'dpg-d4krad9r0fns738c3nd0-a.oregon-postgres.render.com',
                'PORT': '5432',
                'OPTIONS': {
                    'sslmode': 'require',
                },
                'CONN_MAX_AGE': 600,
                'CONN_HEALTH_CHECKS': True,
            }
        }
    else:
        print("💾 Modo OFFLINE - Usando SQLite local")
        
        # Crear directorio para BD local si no existe
        db_dir = Path(__file__).parent.parent / 'db'
        db_dir.mkdir(exist_ok=True)
        
        db_path = db_dir / 'triage_offline.sqlite3'
        
        return {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': str(db_path),
                'OPTIONS': {
                    'timeout': 20,
                },
            }
        }

def check_offline_database():
    """
    Verifica y configura la base de datos offline si es necesaria.
    
    Returns:
        bool: True si la BD offline está lista, False si hay problemas
    """
    try:
        db_dir = Path(__file__).parent.parent / 'db'
        db_path = db_dir / 'triage_offline.sqlite3'
        
        # Si no existe la BD offline, informar que se necesita configurar
        if not db_path.exists():
            print("📋 Base de datos offline no encontrada")
            print("💡 Se creará automáticamente con datos de demostración")
            return True
            
        print(f"✅ Base de datos offline disponible: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando BD offline: {e}")
        return False

def sync_to_offline():
    """
    Sincroniza datos desde PostgreSQL (online) hacia SQLite (offline).
    Esta función se debe ejecutar cuando hay conexión para preparar datos offline.
    """
    print("🔄 Función de sincronización offline - Para implementar en futuras versiones")
    # TODO: Implementar sincronización de datos
    pass

def sync_from_offline():
    """
    Sincroniza datos desde SQLite (offline) hacia PostgreSQL (online).
    Esta función se ejecuta cuando se recupera la conexión.
    """
    print("🔄 Función de sincronización online - Para implementar en futuras versiones") 
    # TODO: Implementar sincronización de datos
    pass