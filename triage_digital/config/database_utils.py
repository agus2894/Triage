#!/usr/bin/env python3
"""
🔗 TRIAGE DIGITAL - DATABASE UTILITIES
=====================================
Utilidades para manejo híbrido de bases de datos (Online/Offline)
"""

import os
import sys
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
    db_host = os.environ.get('DB_HOST', '')
    db_port = int(os.environ.get('DB_PORT', '5432'))
    
    # Si no hay configuración de DB, asumir offline
    if not db_host:
        if use_cache:
            _connection_cache['last_check'] = time.time()
            _connection_cache['is_online'] = False
        return False
    
    db_name = os.environ.get('DB_NAME', '')
    db_user = os.environ.get('DB_USER', '')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_sslmode = os.environ.get('DB_SSLMODE', 'require')

    try:
        # Test rápido de DNS y conectividad
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            (db_host, db_port)
        )
    except (socket.timeout, socket.error, OSError) as e:
        print(f"⚠️  Sin conexión de red a {db_host}:{db_port}: {type(e).__name__}")
        _connection_cache['last_check'] = time.time()
        _connection_cache['is_online'] = False
        return False
    
    # Si hay conexión de red, probar PostgreSQL
    try:
        import psycopg2
        
        # Intentar una conexión real a PostgreSQL
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            sslmode=db_sslmode,
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
        
        # Validar que todas las credenciales estén presentes
        required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            print(f"⚠️ Faltan variables de entorno: {', '.join(missing_vars)}")
            print("💾 Cayendo a modo OFFLINE - Usando SQLite local")
            has_internet = False
        else:
            return {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': os.environ.get('DB_NAME'),
                    'USER': os.environ.get('DB_USER'),
                    'PASSWORD': os.environ.get('DB_PASSWORD'),
                    'HOST': os.environ.get('DB_HOST'),
                    'PORT': os.environ.get('DB_PORT', '5432'),
                    'OPTIONS': {
                        'sslmode': os.environ.get('DB_SSLMODE', 'require'),
                        'connect_timeout': 10,
                    },
                    'CONN_MAX_AGE': 600,
                    'CONN_HEALTH_CHECKS': True,
                }
            }
    
    # Modo offline si no hay conexión
    if not has_internet:
        print("💾 Modo OFFLINE - Usando SQLite local")
        
        # Detectar si estamos ejecutando desde PyInstaller
        if getattr(sys, 'frozen', False):
            # Ejecutable de PyInstaller: usar directorio del ejecutable
            base_path = Path(sys.executable).parent
            print(f"🔧 Ejecutable PyInstaller detectado")
        else:
            # Desarrollo: usar directorio del proyecto
            base_path = Path(__file__).parent.parent
            print(f"🔧 Modo desarrollo detectado")
        
        # Crear directorio para BD local si no existe
        db_dir = base_path / 'db'
        db_dir.mkdir(exist_ok=True)
        
        db_path = db_dir / 'triage_offline.sqlite3'
        
        # LOGGING: mostrar ruta exacta de BD
        print(f"🗄️  base_path = {base_path}")
        print(f"🗄️  db_dir = {db_dir}")
        print(f"🗄️  db_path = {db_path}")
        print(f"🗄️  db_path.exists() = {db_path.exists()}")
        if db_path.exists():
            import os
            print(f"🗄️  Tamaño BD: {os.path.getsize(db_path)} bytes")
        
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