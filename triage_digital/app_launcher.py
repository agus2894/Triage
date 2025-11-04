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
    
    def abrir_navegador():
        time.sleep(3)
        webbrowser.open('http://127.0.0.1:8000')
        print("🌐 Navegador abierto automáticamente")
    
    # Abrir navegador en hilo separado
    thread = threading.Thread(target=abrir_navegador)
    thread.daemon = True
    thread.start()
    
    try:
        # Ejecutar servidor Django
        print("📱 Accede en: http://127.0.0.1:8000")
        print("⏹️  Ctrl+C para detener")
        print("-" * 40)
        
        # Usar call_command con noreload para evitar problemas
        from django.core.management import call_command
        call_command('runserver', '127.0.0.1:8000', verbosity=1, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"❌ Error del servidor: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para salir...")

if __name__ == '__main__':
    main()