#!/bin/bash
# TRIAGE DIGITAL - EL SCRIPT DEFINITIVO
# Un solo comando para regirlos a todos 🎯

clear
echo "🏥 SISTEMA TRIAGE DIGITAL"
echo "========================="
echo "⚡ Iniciando automáticamente..."
echo ""

# Ir al directorio correcto
cd "$(dirname "$0")"

# Detección inteligente del entorno
if [[ "$1" == "prod" ]]; then
    MODO="PRODUCCIÓN"
    PUERTO=80
    HOST="0.0.0.0"
else
    MODO="DESARROLLO"
    PUERTO=8002
    HOST="127.0.0.1"
fi

echo "🔧 Modo: $MODO"
echo "📡 Puerto: $PUERTO"
echo ""

# 1. Migraciones (silencioso)
echo "📋 Configurando base de datos..."
python3 manage.py migrate --verbosity=0 > /dev/null 2>&1

# 2. Admin automático (silencioso)
echo "👤 Configurando administrador..."
python3 manage.py setup_admin > /dev/null 2>&1

# 3. Optimización (silencioso)  
echo "⚡ Optimizando sistema..."
python3 manage.py optimize_db --verbosity=0 > /dev/null 2>&1

# 4. Colectar archivos estáticos si es producción
if [[ "$1" == "prod" ]]; then
    echo "📁 Preparando archivos estáticos..."
    python3 manage.py collectstatic --noinput --verbosity=0 > /dev/null 2>&1
fi

echo ""
echo "🚀 SISTEMA LISTO PARA SALVAR VIDAS"
echo "=================================="
echo "🌐 URL: http://$HOST:$PUERTO"
echo "👤 Admin: admin / 123456"
echo "🏥 Login: DNI + contraseña"
echo ""
echo "💡 Ctrl+C para detener"
echo "🔗 Admin panel: http://$HOST:$PUERTO/admin/"
echo ""

# 5. Iniciar servidor
if [[ "$1" == "prod" ]]; then
    echo "🔥 Iniciando en modo PRODUCCIÓN..."
    python3 manage.py runserver $HOST:$PUERTO --settings=config.settings
else
    echo "🧪 Iniciando en modo DESARROLLO..."  
    python3 manage.py runserver $HOST:$PUERTO
fi