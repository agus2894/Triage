# 📦 INSTRUCCIONES PARA PENDRIVE - TRIAGE DIGITAL

## 🎯 Qué tienes ahora:

✅ **Archivo ejecutable**: `dist/TriageDigital` (~30MB)
✅ **Completamente autónomo**: No necesita Python, Django, ni nada instalado
✅ **Portable**: Funciona desde cualquier ubicación (pendrive, escritorio, etc.)

## 💾 USAR EN PENDRIVE (Recomendado para el docente):

### 1. Preparar pendrive:
```bash
# Copiar el ejecutable al pendrive
cp dist/TriageDigital /media/tu_usuario/TU_PENDRIVE/
# O simplemente arrastrarlo con el explorador de archivos
```

### 2. En cualquier PC Linux:
1. **Conectar pendrive**
2. **Doble clic** en `TriageDigital`
3. **Esperar 5-10 segundos** (se configura automáticamente)
4. **Se abre el navegador** automáticamente en http://127.0.0.1:8001
5. **Login**: admin / 123456

## 🖥️ CREAR ICONO EN ESCRITORIO (Para demostración):

```bash
# Opción 1: Copiar directamente
cp dist/TriageDigital ~/Escritorio/

# Opción 2: Crear acceso directo elegante
cat > ~/Escritorio/TriageDigital.desktop << EOF
[Desktop Entry]
Name=Triage Digital
Comment=Sistema Hospitalario de Triage
Exec=$PWD/dist/TriageDigital
Icon=applications-science
Terminal=false
Type=Application
Categories=Office;Medical;
EOF

chmod +x ~/Escritorio/TriageDigital.desktop
```

## ✅ VENTAJAS de esta solución:

- 🎯 **Un solo archivo** de 30MB
- 🚀 **Auto-abre navegador** al ejecutar
- 🏥 **Auto-configura BD y admin** (admin/123456)
- 💾 **Funciona desde pendrive** sin instalación
- 🖥️ **Compatible** con cualquier Linux moderno
- 📱 **Interfaz PWA** instalable como app nativa

## 🎓 PARA EL DOCENTE:

1. **Entregar**: Pendrive con `TriageDigital` 
2. **Instrucción**: "Doble clic y esperar"
3. **Resultado**: Sistema funcionando en navegador
4. **Login**: admin / 123456

## 🧪 PROBAR AHORA:

```bash
cd dist
./TriageDigital
```

¡Debería abrirse automáticamente el navegador! 🚀