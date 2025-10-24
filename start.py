import subprocess
import webbrowser
import time
import os
import sys

# Detecta si se ejecuta como ejecutable PyInstaller

# Detecta si se ejecuta como ejecutable PyInstaller
if getattr(sys, 'frozen', False):
    # Si el ejecutable está en dist/, sube un nivel para encontrar triage_digital
    exe_dir = os.path.dirname(sys.executable)
    project_root = os.path.abspath(os.path.join(exe_dir, '..'))
else:
    project_root = os.path.dirname(os.path.abspath(__file__))

# Ruta absoluta a triage_digital
django_dir = os.path.join(project_root, 'triage_digital')
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
