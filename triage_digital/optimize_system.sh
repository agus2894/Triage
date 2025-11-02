#!/bin/bash

# Script de optimización completa para Triage Digital
# Ejecutar: ./optimize_system.sh

echo "🚀 OPTIMIZACIÓN COMPLETA DEL SISTEMA TRIAGE DIGITAL"
echo "====================================================="

# Verificar si está en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Ejecutar desde el directorio triage_digital/"
    exit 1
fi

# 1. Crear migraciones para nuevos índices
echo "📋 1. Creando migraciones para nuevos índices..."
python3 manage.py makemigrations --verbosity=1

# 2. Aplicar migraciones
echo "📋 2. Aplicando migraciones..."
python3 manage.py migrate --verbosity=1

# 3. Optimizar base de datos
echo "⚡ 3. Optimizando base de datos..."
python3 manage.py optimize_db

# 4. Verificar rendimiento
echo "🔍 4. Verificando rendimiento..."
python3 manage.py performance_check

# 5. Crear directorio de logs si no existe
echo "📁 5. Configurando logging..."
mkdir -p logs
touch logs/triage.log
echo "✅ Directorio de logs creado"

# 6. Verificar permisos
echo "🔐 6. Verificando permisos..."
chmod 644 db/triage_digital.sqlite3 2>/dev/null || echo "Base de datos no encontrada (primera ejecución)"
chmod 755 logs 2>/dev/null
chmod 644 logs/triage.log 2>/dev/null

echo ""
echo "✅ OPTIMIZACIÓN COMPLETADA"
echo "=========================="
echo ""
echo "📊 COMANDOS ÚTILES PARA MANTENIMIENTO:"
echo "  python3 manage.py performance_check         # Análisis de rendimiento"
echo "  python3 manage.py optimize_db               # Optimizar base de datos"
echo "  python3 manage.py cleanup_old_data --days=365  # Limpiar datos antiguos"
echo "  python3 manage.py performance_check --detailed # Análisis detallado"
echo ""
echo "🎯 El sistema está ahora ultra-optimizado para emergencias médicas."