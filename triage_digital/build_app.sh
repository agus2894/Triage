#!/bin/bash

echo "🏥 COMPILANDO TRIAGE DIGITAL - APP AUTÓNOMA"
echo "============================================"

# Activar entorno virtual
echo "🐍 Activando entorno virtual..."
source ../.venv/bin/activate

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
    echo "� Tamaño aprox: $(du -h dist/TriageDigital 2>/dev/null | cut -f1 || echo "~100MB")"
    echo ""
    echo "�🖥️ Para crear acceso directo:"
    echo "   - Copiar dist/TriageDigital al escritorio"
    echo "   - Renombrar a 'Triage Digital'"
    echo ""
    echo "💾 Para pendrive:"
    echo "   - Copiar toda la carpeta dist/ al pendrive"
    echo "   - Ejecutar desde allí"
    echo ""
    echo "🚀 Para probar: cd dist && ./TriageDigital"
    echo ""
else
    echo "❌ Error en la compilación"
    exit 1
fi