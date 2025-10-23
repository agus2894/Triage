#!/bin/bash
# 🎯 DEMO TRIAGE DIGITAL - SÚPER FÁCIL
# Doble click y listo - Sin complicaciones

clear
echo "🎯 DEMO TRIAGE DIGITAL"
echo "====================="
echo "💻 Iniciando demo local..."
echo ""

# Ir al directorio del proyecto
cd "$(dirname "$0")/Triage/triage_digital"

# Activar entorno virtual
source ../.venv/bin/activate

# Iniciar en modo demo
./start.sh demo

echo ""
echo "❌ Demo terminado"
echo "💡 Para volver a usar: doble click en demo.sh"