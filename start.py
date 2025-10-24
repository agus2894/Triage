
import subprocess
import webbrowser
import time
import os
import sys

def ensure_requirements():
    try:
        import django  # noqa: F401
    except ImportError:
        req_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)), 'requirements.txt')
        print('Instalando dependencias desde requirements.txt...')
        subprocess.check_call(['pip', 'install', '-r', req_path])
        print('Dependencias instaladas. Reinicia el programa.')
        sys.exit(0)

ensure_requirements()

# Detecta si se ejecuta como ejecutable PyInstaller

# Detecta si se ejecuta como ejecutable PyInstaller
if getattr(sys, 'frozen', False):
    # Siempre busca triage_digital en la misma carpeta que el ejecutable
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta a triage_digital
django_dir = os.path.join(base_dir, 'triage_digital')
os.chdir(django_dir)


# Inicia el servidor Django y muestra la salida y errores en pantalla
server = subprocess.Popen(
    ['python3', 'manage.py', 'runserver', '0.0.0.0:8000'],
    stdout=None,  # Hereda la salida estándar
    stderr=None   # Hereda los errores estándar
)

# Espera unos segundos para que el servidor arranque
print('Iniciando servidor Django...')
time.sleep(3)

# Abre el navegador en la página principal
webbrowser.open('http://127.0.0.1:8000/')

# Espera a que el servidor termine
try:
    server.wait()
except KeyboardInterrupt:
    print('Cerrando servidor...')
    server.terminate()
