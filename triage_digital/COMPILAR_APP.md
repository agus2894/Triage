# 🏥 Crear App Autónoma - Triage Digital

## 📋 Requisitos para compilar

```bash
pip install pyinstaller pillow
```

## 🚀 Compilar la aplicación

```bash
# Método automático (recomendado)
./build_app.sh

# Método manual
pyinstaller TriageDigitalApp.spec
```

## 📁 Resultado

- **Ejecutable**: `dist/TriageDigital` (Linux) o `dist/TriageDigital.exe` (Windows)
- **Tamaño**: ~80-150 MB (incluye Python + Django + dependencias)
- **Autónomo**: No requiere Python instalado en el sistema destino

## 🖥️ Crear icono en escritorio

### Linux:
```bash
# Copiar ejecutable al escritorio
cp dist/TriageDigital ~/Escritorio/

# Crear archivo .desktop
cat > ~/Escritorio/TriageDigital.desktop << EOF
[Desktop Entry]
Name=Triage Digital
Comment=Sistema Hospitalario de Triage
Exec=/home/$USER/Escritorio/TriageDigital
Icon=applications-science
Terminal=false
Type=Application
Categories=Office;Medical;
EOF

chmod +x ~/Escritorio/TriageDigital.desktop
```

### Windows:
1. Clic derecho en `TriageDigital.exe` → "Crear acceso directo"
2. Arrastar acceso directo al escritorio
3. Renombrar a "Triage Digital"

## ✅ Uso de la app

1. **Doble clic** en el icono del escritorio
2. **Esperar** ~5-10 segundos (primera vez puede tardar más)
3. **Se abre automáticamente** el navegador en http://127.0.0.1:8001
4. **Login**: admin / 123456

## 🎯 Características de la app autónoma

- ✅ **Portátil**: Un solo archivo ejecutable
- ✅ **Auto-configuración**: Base de datos y admin se crean automáticamente
- ✅ **Sin dependencias**: No necesita Python instalado
- ✅ **Icono personalizado**: Cruz médica azul
- ✅ **Navegador automático**: Se abre solo al iniciar
- ✅ **Logs incluidos**: Sistema de logging integrado

## 🔧 Solución de problemas

**Si no se abre el navegador automáticamente:**
- Ir manualmente a: http://127.0.0.1:8001

**Si hay error de puerto ocupado:**
- Cerrar otras instancias del programa
- Reiniciar la aplicación

**Primera ejecución lenta:**
- Es normal, el sistema se está configurando
- Las siguientes ejecuciones serán más rápidas