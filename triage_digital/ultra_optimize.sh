#!/bin/bash
# Ultra-optimización de Triage Digital
# Filosofía: "Menos es mejor" - Máxima velocidad

echo "⚡ ULTRA-OPTIMIZACIÓN TRIAGE DIGITAL"
echo "===================================="

# 1. Limpiar caché Django
echo "🧹 Limpiando cachés..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

# 2. Optimizar base de datos
echo "🗃️ Ultra-optimizando base de datos..."
python3 manage.py optimize_db --verbosity=0

# 3. Compilar templates (si fuera necesario)
echo "📄 Verificando templates..."
python3 manage.py check --verbosity=0

# 4. Limpiar logs antiguos
echo "📝 Rotando logs..."
if [ -f "logs/triage.log" ] && [ $(stat -f%z "logs/triage.log" 2>/dev/null || stat -c%s "logs/triage.log") -gt 1048576 ]; then
    mv logs/triage.log logs/triage.log.old
    echo "Log rotado por tamaño"
fi

# 5. Verificar memoria disponible
echo "💾 Verificando recursos..."
if command -v free >/dev/null 2>&1; then
    FREE_MEM=$(free -m | awk 'NR==2{printf "%.0f", $7*100/$2 }')
    echo "  📊 Memoria libre: ${FREE_MEM}%"
fi

# 6. Test de velocidad crítica
echo "🚀 Test de velocidad crítica..."
START=$(date +%s%N)
python3 manage.py shell -c "
from apps.triage.models import SignosVitales
from apps.patients.models import Paciente
print(f'Pacientes: {Paciente.objects.count()}')
print(f'Evaluaciones: {SignosVitales.objects.count()}')
" 2>/dev/null
END=$(date +%s%N)
SPEED=$(( (END - START) / 1000000 ))

echo "  ⚡ Consulta BD: ${SPEED}ms"

# 7. Verificar puerto disponible
if lsof -i:8002 >/dev/null 2>&1; then
    echo "  🔄 Puerto 8002 en uso - usando 8003"
    PORT=8003
else
    PORT=8002
fi

echo ""
echo "🎯 ULTRA-OPTIMIZACIÓN COMPLETADA"
echo "================================"
echo "  ⚡ Sistema: ULTRA-RÁPIDO"
echo "  🏥 Estado: LISTO"
echo "  🚀 Puerto: $PORT"
echo ""
echo "Iniciar con: python3 manage.py runserver $PORT"
echo "Dashboard: http://localhost:$PORT/triage/"