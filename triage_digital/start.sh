#!/bin/bash
# TRIAGE DIGITAL - EL SCRIPT DEFINITIVO
# Un solo comando para regirlos a todos

clear
echo " SISTEMA TRIAGE DIGITAL"
echo "========================="
echo "⚡ Iniciando automáticamente..."
echo ""

# Ir al directorio correcto
cd "$(dirname "$0")"

# Activar entorno virtual automáticamente
if [ -f "../.venv/bin/activate" ]; then
    source ../.venv/bin/activate
    echo "🐍 Entorno virtual activado"
fi

# Detección inteligente del entorno
if [[ "$1" == "prod" ]]; then
    MODO="PRODUCCIÓN"
    PUERTO=80
    HOST="0.0.0.0"
elif [[ "$1" == "red" ]]; then
    MODO="RED HOSPITALARIA"
    PUERTO=8001
    HOST="0.0.0.0"
elif [[ "$1" == "demo" ]]; then
    MODO="DEMO HOSPITALARIA"
    PUERTO=8001
    HOST="127.0.0.1"
else
    MODO="DESARROLLO"
    PUERTO=8001
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

# 3. OPTIMIZACIÓN AUTOMÁTICA INTEGRADA (NUEVO)
echo "⚡ Auto-optimizando sistema..."
python3 manage.py optimize_db --verbosity=0 > /dev/null 2>&1

# 4. Verificar si necesita limpieza automática
DB_SIZE=$(du -k db/triage_digital.sqlite3 2>/dev/null | cut -f1)
if [ ! -z "$DB_SIZE" ] && [ "$DB_SIZE" -gt 50000 ]; then  # >50MB
    echo "🧹 Optimizando datos antiguos..."
    python3 manage.py cleanup_old_data --days=180 > /dev/null 2>&1
fi

# 3.5. Datos demo si es modo demo
if [[ "$1" == "demo" ]]; then
    echo "🎯 Generando datos de demostración..."
    python3 manage.py demo_data --reset > /dev/null 2>&1
fi

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
echo "🔗 Admin panel: http://$HOST:$PUERTO/login/"
echo ""

# 5. Iniciar servidor
if [[ "$1" == "prod" ]]; then
    echo "🔥 Iniciando en modo PRODUCCIÓN..."
    python3 manage.py runserver $HOST:$PUERTO --settings=config.settings
elif [[ "$1" == "red" ]]; then
    echo "🏥 Iniciando en RED HOSPITALARIA..."
    echo "📱 Dispositivos pueden acceder desde la red interna"
    python3 manage.py runserver $HOST:$PUERTO
elif [[ "$1" == "demo" ]]; then
    echo "🎯 Iniciando en modo DEMO..."
    echo "💻 Perfecto para demostraciones locales"
    echo "📱 PWA instalable desde localhost"
    python3 manage.py runserver $HOST:$PUERTO
else
    echo "🧪 Iniciando en modo DESARROLLO..."  
    python3 manage.py runserver $HOST:$PUERTO
fi