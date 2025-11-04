#!/usr/bin/env python3
"""
Triage Digital - Aplicación Autónoma
Punto de entrada principal para la app compilada
"""
import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def main():
    """Función principal que inicia el servidor Django y abre el navegador"""
    try:
        # Configurar el directorio de trabajo
        if getattr(sys, 'frozen', False):
            # Si estamos en una app compilada
            base_dir = Path(sys.executable).parent
        else:
            # Si estamos en desarrollo
            base_dir = Path(__file__).parent
            
        os.chdir(base_dir)
        
        # Verificar que existe manage.py
        if not Path('manage.py').exists():
            print("❌ Error: No se encontró manage.py")
            input("Presiona Enter para salir...")
            return
            
        print("🏥 Iniciando Triage Digital...")
        print("============================")
        
        # Configurar base de datos si es necesario
        print("📋 Configurando sistema...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                      capture_output=True, check=False)
        
        print("👤 Configurando administrador...")
        subprocess.run([sys.executable, 'manage.py', 'setup_admin'], 
                      capture_output=True, check=False)
        
        print("🚀 Iniciando servidor...")
        print("💻 El sistema se abrirá automáticamente en tu navegador")
        print("🔗 URL: http://127.0.0.1:8001")
        print("👤 Usuario: admin | Contraseña: 123456")
        print("")
        print("💡 Presiona Ctrl+C para detener")
        
        # Función para abrir el navegador después de un delay
        def abrir_navegador():
            time.sleep(3)  # Esperar a que el servidor esté listo
            try:
                webbrowser.open('http://127.0.0.1:8001')
            except:
                pass
        
        # Abrir navegador en thread separado
        threading.Thread(target=abrir_navegador, daemon=True).start()
        
        # Iniciar servidor Django
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8001'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == '__main__':
    main()