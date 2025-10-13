#!/bin/bash
# Script súper simple para iniciar Triage Digital
# Un solo comando, un solo admin

echo "🏥 TRIAGE DIGITAL - INICIO RÁPIDO"
echo "================================"

# Ir al directorio correcto
cd "$(dirname "$0")"

# Configurar admin único
echo "👤 Configurando admin..."
python3 manage.py setup_admin

# Aplicar migraciones si es necesario
echo "📋 Verificando base de datos..."
python3 manage.py migrate --verbosity=0

# Ultra-optimizar
echo "⚡ Ultra-optimizando..."
python3 manage.py optimize_db --verbosity=0

echo ""
echo "🚀 SISTEMA LISTO"
echo "==============="
echo "🌐 Abrir: http://localhost:8002"
echo "👤 Admin: admin / 123456"
echo "🏥 Triage: DNI 00000000 / 123456"
echo ""

# Iniciar servidor
python3 manage.py runserver 8002