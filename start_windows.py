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
        subprocess.check_call(['pip', 'install', '-r', req_path], shell=True)
        print('Dependencias instaladas. Reinicia el programa.')
        sys.exit(0)

ensure_requirements()

# Detecta si se ejecuta como ejecutable PyInstaller
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta a triage_digital
django_dir = os.path.join(base_dir, 'triage_digital')
os.chdir(django_dir)

# Inicia el servidor Django y muestra la salida y errores en pantalla
server = subprocess.Popen(
    ['python', 'manage.py', 'runserver', '0.0.0.0:8000'],
    stdout=None,
    stderr=None
)

print('Iniciando servidor Django...')
time.sleep(3)

webbrowser.open('http://127.0.0.1:8000/')

try:
    server.wait()
except KeyboardInterrupt:
    print('Cerrando servidor...')
    server.terminate()
