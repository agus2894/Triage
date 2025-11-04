#!/bin/bash

echo "🏥 COMPILANDO TRIAGE DIGITAL - APP AUTÓNOMA"
echo "============================================"

# Verificar dependencias
echo "📦 Verificando dependencias..."
pip install pyinstaller pillow

# Limpiar builds anteriores
echo "🧹 Limpiando builds anteriores..."
rm -rf build/ dist/ __pycache__/

# Compilar aplicación
echo "⚙️ Compilando aplicación..."
pyinstaller TriageDigitalApp.spec

# Verificar resultado
if [ -f "dist/TriageDigital" ] || [ -f "dist/TriageDigital.exe" ]; then
    echo ""
    echo "✅ COMPILACIÓN EXITOSA"
    echo "======================"
    echo "📁 Archivo ejecutable en: dist/"
    echo "🖥️ Para crear acceso directo:"
    echo "   - Copiar el ejecutable al escritorio"
    echo "   - Renombrar a 'Triage Digital'"
    echo ""
    echo "🚀 Para probar: cd dist && ./TriageDigital"
    echo ""
else
    echo "❌ Error en la compilación"
    exit 1
fi