#!/usr/bin/env python3
"""
🏥 TRIAGE DIGITAL - LAUNCHER CLOUD
==================================
Versión para ejecutable con BD en Render
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
        sys.argv = ['TriageDigitalCloud']
    
    # Configurar Django
    print("📋 Configurando sistema...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        from django.core.management import execute_from_command_line
        django.setup()
        print("✅ Sistema configurado")
        
    except Exception as e:
        print(f"❌ Error de configuración: {e}")
        input("Presiona Enter para salir...")
        return
    
    # NO ejecutamos migraciones - ya están en Render
    print("📊 Base de datos en Render - Lista")
    
    # Arrancar servidor
    print("🚀 Iniciando servidor web...")

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