#!/bin/bash

set -e

echo "🏥 COMPILANDO TRIAGE DIGITAL - APP AUTÓNOMA"
echo "============================================"

# Activar entorno virtual
if [ -f "../venv/bin/activate" ]; then
    echo "🐍 Activando entorno virtual..."
    source ../venv/bin/activate
else
    echo "⚠️  Entorno virtual ../venv no encontrado. Creando uno..."
    python3 -m venv ../venv
    source ../venv/bin/activate
    pip install -r ../requirements.txt
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
pip install --upgrade pyinstaller pillow

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ __pycache__/

# Compilar aplicación
echo "⚙️ Compilando aplicación..."
pyinstaller TriageDigital.spec

# Copiar archivos adicionales necesarios
echo "📦 Copiando archivos adicionales..."
if [ -d "db" ]; then
    mkdir -p dist/db
    if [ -f "db/triage_offline.sqlite3" ]; then
        cp db/triage_offline.sqlite3 dist/db/
        echo "   ✅ Base de datos offline copiada"
    else
        echo "   ⚠️  Base de datos offline no encontrada (se creará al primer uso)"
    fi
fi

# Verificar resultado
if [ -f "dist/TriageDigital" ] || [ -f "dist/TriageDigital.exe" ]; then
    echo ""
    echo "✅ COMPILACIÓN EXITOSA"
    echo "======================"
    echo "📁 Archivo ejecutable en: dist/TriageDigital"
    echo "📦 Tamaño aprox: $(du -h dist/TriageDigital 2>/dev/null | cut -f1 || echo "~100MB")"
    echo ""
    echo "📋 CONTENIDO DE dist/:"
    echo "   - TriageDigital (ejecutable)"
    if [ -d "dist/db" ]; then
        echo "   - db/ (base de datos SQLite para modo offline)"
    fi
    echo ""
    echo "🖥️ Para crear acceso directo:"
    echo "   - Copiar TODA la carpeta dist/ al escritorio"
    echo "   - Renombrar carpeta a 'Triage Digital'"
    echo "   - Ejecutar dist/TriageDigital"
    echo ""
    echo "💾 Para pendrive (IMPORTANTE):"
    echo "   - Copiar TODA la carpeta dist/ al pendrive"
    echo "   - No copiar solo el ejecutable, necesita la carpeta db/"
    echo "   - Ejecutar desde allí"
    echo ""
    echo "🚀 Para probar: cd dist && ./TriageDigital"
    echo ""
else
    echo "❌ Error en la compilación"
    exit 1
fi
