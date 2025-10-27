#!/bin/bash
# --------------------------------------------------------
# Lanzador de Triage Digital - versión portable
# Autor: Gonzalo Lamas
# --------------------------------------------------------

# Ir al directorio donde está el script
cd "$(dirname "$0")"

# Ejecutar el binario sin autoreload
./TriageDigitalApp runserver 0.0.0.0:8000 --noreload &

# Esperar unos segundos a que el servidor arranque
sleep 3

# Abrir el navegador automáticamente
xdg-open http://127.0.0.1:8000
