#!/bin/bash
# Script de inicio optimizado para Triage Digital
# Uso: ./start_production.sh

echo "🏥 Iniciando Triage Digital - Modo Producción"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado"
    exit 1
fi

# Verificar directorio
if [ ! -f "manage.py" ]; then
    echo "❌ Ejecutar desde el directorio del proyecto"
    exit 1
fi

# Crear logs si no existe
mkdir -p logs

# Aplicar migraciones
echo "📋 Aplicando migraciones..."
python3 manage.py migrate --settings=config.settings_production

# Recopilar archivos estáticos
echo "📦 Recopilando archivos estáticos..."
python3 manage.py collectstatic --noinput --settings=config.settings_production

# Verificar configuración
echo "🔍 Verificando configuración..."
python3 manage.py check --settings=config.settings_production

# Configurar admin único
echo "👤 Configurando admin único..."
python3 manage.py setup_admin --settings=config.settings_production

echo "🚀 Iniciando servidor de producción..."
echo "📊 Panel Admin: http://localhost:8000/admin/"
echo "🏥 Sistema Triage: http://localhost:8000/"
echo "📋 Logs en: ./logs/"

# Iniciar servidor
python3 manage.py runserver 0.0.0.0:8000 --settings=config.settings_production