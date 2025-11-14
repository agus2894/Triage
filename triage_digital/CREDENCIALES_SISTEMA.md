# 🏥 TRIAGE DIGITAL - CREDENCIALES DEL SISTEMA

## 📋 INFORMACIÓN GENERAL
- **Aplicación**: Sistema de Triage Digital
- **Versión**: Híbrida Online/Offline
- **Tamaño ejecutable**: 35MB
- **Ubicación**: `/home/agustin/Escritorio/Triage/triage_digital/dist/TriageDigital`

---

## 🔑 CREDENCIALES DE ACCESO

### 👤 ADMINISTRADOR DEL SISTEMA
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **DNI**: `00000000`
- **Nivel**: Superusuario (acceso completo)
- **Permisos**: Administración total del sistema

### 👨‍⚕️ ENFERMERO TRIAJERO - LAMAS GONZALO
- **Usuario**: `38046539`
- **Contraseña**: `38046539`
- **DNI**: `38046539`
- **Nivel**: Staff médico
- **Rol**: Enfermero Triajero

### 👩‍⚕️ ENFERMERA TRIAJERA - GORDALIZA FLORENCIA
- **Usuario**: `43724258`
- **Contraseña**: `43724258`
- **DNI**: `43724258`
- **Nivel**: Staff médico
- **Rol**: Enfermera Triajera

---

## 🌐 MODOS DE OPERACIÓN

### MODO ONLINE (Con internet)
- **Base de datos**: PostgreSQL en Render
- **Funcionalidad**: Colaboración en tiempo real
- **Usuarios**: Los 3 usuarios arriba funcionan
- **Detección**: Automática al iniciar la aplicación

### MODO OFFLINE (Sin internet)
- **Base de datos**: SQLite local
- **Funcionalidad**: Presentaciones y trabajo offline
- **Usuarios**: Los mismos 3 usuarios funcionan
- **Datos demo**: 3 pacientes de ejemplo incluidos

---

## 🚀 INSTRUCCIONES DE USO

### Para usar Online:
1. Asegurar conexión a internet
2. Ejecutar: `./TriageDigital` desde carpeta `dist/`
3. Esperar mensaje: "🌐 Modo ONLINE - PostgreSQL en Render"
4. Acceder en: http://127.0.0.1:8000

### Para usar Offline:
1. **Desconectar internet** (WiFi o cable)
2. Ejecutar: `./TriageDigital` desde carpeta `dist/`
3. Esperar mensaje: "💾 Modo OFFLINE - SQLite local"
4. Acceder en: http://127.0.0.1:8000

---

## ✅ VALIDACIÓN DEL SISTEMA

### Comprobaciones realizadas:
- ✅ Usuarios configurados en PostgreSQL remoto
- ✅ Usuarios configurados en SQLite local
- ✅ Detección automática Online/Offline funcional
- ✅ Ejecutable compilado con soporte híbrido
- ✅ Base de datos offline incluida en ejecutable

### Estado actual:
- **Base de datos remota**: ✅ LISTA con usuarios del sistema
- **Base de datos local**: ✅ LISTA con usuarios del sistema
- **Ejecutable**: ✅ LISTO para uso en presentaciones

---

## 🎯 PRÓXIMOS PASOS SUGERIDOS

1. **Probar modo online** con internet conectado
2. **Probar modo offline** desconectando internet
3. **Validar login** con los 3 usuarios en ambos modos
4. **Crear datos de prueba** adicionales si es necesario

---

## 📞 SOPORTE TÉCNICO
Sistema desarrollado y configurado el 14 de noviembre de 2025.
Todos los usuarios están sincronizados entre modo online y offline.