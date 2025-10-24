#!/bin/bash
# Script de instalación y empaquetado automático para Triage Digital
set -e

# 1. Generar el ejecutable con PyInstaller
pyinstaller --onefile --windowed start.py

# 2. Crear carpeta de distribución final
DIST_DIR="TriageApp"
rm -rf "$DIST_DIR"
mkdir "$DIST_DIR"

# 3. Copiar ejecutable, carpeta triage_digital, requirements.txt y base de datos
cp dist/start "$DIST_DIR"/
cp -r triage_digital "$DIST_DIR"/
cp requirements.txt "$DIST_DIR"/
cp triage_digital/db/triage_digital.sqlite3 "$DIST_DIR"/ 2>/dev/null || true

# 4. Copiar manual y acceso directo
cp TriageApp_ManualUsuario.txt "$DIST_DIR"/
cat > "$DIST_DIR/triage.desktop" <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=Triage Digital
Comment=Iniciar el sistema de Triage Digital
Exec=$(pwd)/$DIST_DIR/start
Icon=utilities-terminal
Terminal=true
Categories=Utility;
EOL
chmod +x "$DIST_DIR/triage.desktop"

# 5. Mensaje final
cat <<MSG

¡Listo! La carpeta $DIST_DIR contiene todo lo necesario para ejecutar Triage Digital.
Puedes copiarla a cualquier PC Linux.
Para el usuario final:
- Ejecutar ./start o hacer doble clic en triage.desktop
Para el usuario final:
- Ejecutar ./start o hacer doble clic en triage.desktop
- Si quieres el acceso directo en el escritorio, copia triage.desktop al escritorio y dale permisos de ejecución.
MSG
