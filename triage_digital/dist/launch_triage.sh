#!/bin/bash
# --------------------------------------------------------
# Lanzador de Triage Digital - versión portable
# Autor: Gonzalo Lamas
# --------------------------------------------------------

# Obtener el directorio del script
APP_DIR="$(dirname "$(realpath "$0")")"

# Ejecutar el binario
"$APP_DIR/TriageDigitalApp" &

# Esperar unos segundos a que el servidor arranque
sleep 3

# Abrir el navegador automáticamente
xdg-open http://127.0.0.1:8000
