#!/usr/bin/env python3
"""
🏥 TRIAGE DIGITAL - LAUNCHER HÍBRIDO
====================================
Versión con soporte Online/Offline automático
"""

import os
import sys
import time
import webbrowser
import subprocess
import threading
from pathlib import Path
import socket

def main():
    print("🏥 Iniciando Triage Digital...")
    print("============================")
    
    # Configurar sys.argv PRIMERO
    if not sys.argv or len(sys.argv) == 0:
        sys.argv = ['TriageDigitalHybrid']
    
    # Configurar Django
    print("📋 Configurando sistema...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        from django.core.management import execute_from_command_line, call_command
        django.setup()
        print("✅ Sistema configurado")
        
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        input("Presiona Enter para salir...")
        return

    # Verificar modo de operación y configurar BD si es necesario
    _setup_database()
    
    # Arrancar servidor
    print("🚀 Iniciando servidor web...")

def _setup_database():
    """Configura la base de datos según el modo (online/offline)"""
    try:
        from django.conf import settings
        from django.core.management import call_command
        from pathlib import Path
        
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'postgresql' in db_engine:
            print("🌐 Modo ONLINE - PostgreSQL en Render")
            print("📊 Colaboración habilitada con tu colega")
        elif 'sqlite3' in db_engine:
            print("💾 Modo OFFLINE - SQLite local")
            print("📱 Perfecto para presentaciones sin internet")
            
            # Verificar si existe la BD offline
            db_path = Path(settings.DATABASES['default']['NAME'])
            if not db_path.exists():
                print("⚙️  Configurando BD offline por primera vez...")
                try:
                    call_command('setup_offline', verbosity=0, interactive=False)
                    print("✅ BD offline configurada con datos de demostración")
                    print("🎯 Usuario: admin / Contraseña: admin123")
                except Exception as e:
                    print(f"⚠️  Error configurando BD offline: {e}")
                    print("📋 Ejecutando migraciones básicas...")
                    call_command('migrate', verbosity=0, interactive=False)
            else:
                print("✅ BD offline disponible")
        else:
            print("⚠️  Modo de BD desconocido")
            
    except Exception as e:
        print(f"⚠️  Error verificando BD: {e}")
        print("📋 Continuando con configuración básica...")

def main():
    print("🏥 Iniciando Triage Digital...")
    print("============================")
    
    # Configurar sys.argv PRIMERO
    if not sys.argv or len(sys.argv) == 0:
        sys.argv = ['TriageDigitalHybrid']
    
    # Configurar Django
    print("📋 Configurando sistema...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        from django.core.management import execute_from_command_line, call_command
        django.setup()
        print("✅ Sistema configurado")
        
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        input("Presiona Enter para salir...")
        return

    # Verificar modo de operación y configurar BD si es necesario
    _setup_database()

    # Determinar puerto: 1) argumento --port, 2) env PORT, 3) por defecto 8000
    def _parse_port():
        # Buscar --port N en sys.argv
        for i, a in enumerate(sys.argv):
            if a.startswith('--port='):
                try:
                    return int(a.split('=', 1)[1])
                except Exception:
                    pass
            if a == '--port' and i + 1 < len(sys.argv):
                try:
                    return int(sys.argv[i+1])
                except Exception:
                    pass
        # ENV
        env_port = os.environ.get('PORT') or os.environ.get('TRIAGE_PORT')
        if env_port:
            try:
                return int(env_port)
            except Exception:
                pass
        return 8000

    def _is_port_free(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.close()
            return True
        except OSError:
            try:
                s.close()
            except Exception:
                pass
            return False

    def _find_free_port(preferred=8000, host='127.0.0.1', start=8000, end=8100):
        # Try preferred first
        if preferred and _is_port_free(host, preferred):
            return preferred
        # scan range
        for p in range(start, end + 1):
            if _is_port_free(host, p):
                return p
        # As last resort, ask OS for a free port
        s = socket.socket()
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    preferred_port = _parse_port()
    port = _find_free_port(preferred=preferred_port, start=8000, end=8100)
    url = f'http://127.0.0.1:{port}'

    def abrir_navegador():
        time.sleep(3)
        try:
            webbrowser.open(url)
            print(f"🌐 Navegador abierto automáticamente en {url}")
        except Exception:
            print(f"🌐 No se pudo abrir el navegador automáticamente. Abre: {url}")

    # Abrir navegador en hilo separado
    thread = threading.Thread(target=abrir_navegador)
    thread.daemon = True
    thread.start()

    try:
        # Ejecutar servidor Django
        print(f"📱 Accede en: {url}")
        print("⏹️  Ctrl+C para detener")
        print("-" * 40)

        # Usar call_command con noreload para evitar problemas
        from django.core.management import call_command
        call_command('runserver', f'127.0.0.1:{port}', verbosity=1, use_reloader=False)

    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"❌ Error del servidor: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == '__main__':
    main()