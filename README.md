# 🏥 TRIAGE DIGITAL - SISTEMA HOSPITALARIO INTEGRADO

> **Sistema de clasificación médica de emergencia - TODO INTEGRADO EN UNA PANTALLA**  
> *Dashboard unificado - Sin páginas separadas - Optimizado para velocidad crítica*

---

## ✨ **CARACTERÍSTICAS PRINCIPALES**

🎯 **DISEÑO UNIFICADO**: Todo en una sola pantalla - formulario, estadísticas y pacientes  
⚡ **ULTRA RÁPIDO**: Auto-refresh cada 30 segundos, cache inteligente  
📱 **PWA COMPLETA**: Instalable como app móvil/escritorio  
🔄 **TIEMPO REAL**: Actualizaciones automáticas sin recargar página  
🏥 **LISTO PARA HOSPITAL**: Base de datos optimizada, sistema de turnos integrado

---

## 🚀 **INSTALACIÓN EN MÁQUINA DE COLEGA**

### **📋 Requisitos Previos**
- Python 3.8+ instalado
- Git instalado
- Acceso a terminal/command prompt

### **⚡ Instalación Súper Rápida**

```bash
# 1. Clonar proyecto
git clone [URL_DEL_REPOSITORIO]
cd Triage

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# O en Windows: venv\Scripts\activate

# 3. Instalar dependencias (solo 2 esenciales!)
cd triage_digital
pip install -r requirements.txt

# 4. Configurar sistema automáticamente
python manage.py migrate
python manage.py setup_admin
python manage.py demo_data

# 5. Iniciar servidor
python manage.py runserver

# ¡LISTO! Sistema funcionando en http://127.0.0.1:8000/triage/
```

---

## 🔑 **CREDENCIALES DE ACCESO**

### **�‍⚕️ ENFERMERO TRIAJERO** (Solo triage)
- **URL**: http://127.0.0.1:8000/triage/
- **DNI**: `38046539`
- **Contraseña**: `123456`
- **Permisos**: Realizar triage, ver pacientes en espera

### **🔧 ADMINISTRADOR** (Todos los permisos + Reportes PDF)
- **URL**: http://127.0.0.1:8000/triage/
- **DNI**: `00000000` (8 ceros)
- **Contraseña**: `123456`
- **Permisos**: Triage + Descargar reportes PDF + Gestión

### **🔧 Panel Admin Django:**
- **URL**: http://127.0.0.1:8000/admin/
- **Usuario**: `admin`
- **Contraseña**: `123456`

> ⚠️ **IMPORTANTE**: Cambiar contraseñas en producción real

---

## 🏥 **CÓMO USAR EL SISTEMA**

### **1️⃣ Triage de Paciente (Proceso Completo)**
1. **Login** con DNI médico
2. **Click "Nuevo Triage"** → Formulario unificado
3. **Llenar datos** del paciente (nombre, edad, etc.)
4. **Ingresar signos vitales** (6 parámetros médicos)
5. **¡Resultado automático!** - NEWS Score y color (Rojo/Amarillo/Verde)

### **2️⃣ Dashboard en Tiempo Real**
- **Vista general** de todos los casos
- **Pacientes críticos** destacados en rojo
- **Lista lateral** se actualiza cada 30 segundos
- **Botón "Atendido"** para marcar completado

### **3️⃣ Reportes Diarios**
- **PDF automático** con estadísticas del día
- **Descarga inmediata** desde el dashboard

---

## 📱 **CARACTERÍSTICAS DESTACADAS**

### **⚡ Ultra-Optimizado AUTOMÁTICAMENTE**
- **AUTO-OPTIMIZACIÓN** - El sistema se optimiza solo, sin configuración
- **CACHE INTELIGENTE** - Datos críticos siempre disponibles al instante  
- **BASE DE DATOS AUTO-TUNEADA** - Configuración perfecta desde el primer uso
- **LIMPIEZA AUTOMÁTICA** - Mantiene el rendimiento sin intervención manual
- **ADAPTACIÓN INTELIGENTE** - Se adapta automáticamente al dispositivo y uso

---

## 🏗️ **ARQUITECTURA FINAL - TODO INTEGRADO**

### **📱 PANTALLA PRINCIPAL UNIFICADA**
```
┌─────────────────────────────────────────────────────┐
│ 🏥 TRIAGE DIGITAL - Dashboard Integrado             │
├─────────────────┬───────────────────────────────────┤
│ 📊 ESTADÍSTICAS │ 📝 FORMULARIO DE TRIAGE           │
│ 🔴 Críticos: 2  │ Nombre: [____________]            │
│ 🟡 Moderados: 5 │ DNI: [____________]               │
│ 🟢 Leves: 3     │ Frecuencia Cardíaca: [____]      │
│ 📈 Total: 10    │ Saturación O2: [____]            │
├─────────────────┤ Temperatura: [____]              │
│ 👥 PACIENTES EN │ [CREAR TRIAGE] ← TODO EN UNO      │
│    ESPERA       ├───────────────────────────────────┤
│ • Juan P. [🔴]  │ 📋 PACIENTES RECIENTES            │
│ • Ana L. [🟡]   │ ✅ Pedro M. - Atendido 10:30      │
│ • Luis R. [🟢]  │ ✅ María J. - Atendida 11:15      │
│ [Atender] [✓]   │ ✅ Carlos S. - Atendido 11:45     │
└─────────────────┴───────────────────────────────────┘
```

### **⚡ FLUJO OPTIMIZADO**
1. **UNA SOLA PANTALLA** - Todo visible simultáneamente
2. **FORMULARIO INTEGRADO** - Crear triage sin cambiar página
3. **ESTADÍSTICAS EN VIVO** - Actualizadas cada 30 segundos
4. **LISTA PACIENTES** - Sidebar con botones de acción directa
5. **HISTORIAL RECIENTE** - Ver atenciones del día

### **🔒 SISTEMA DE ROLES Y PERMISOS**

#### **👩‍⚕️ ENFERMERO TRIAJERO**
- ✅ Realizar triage de pacientes
- ✅ Ver pacientes en espera con priorización automática
- ✅ Marcar pacientes como atendidos
- ❌ **NO puede descargar reportes PDF**
- 🎯 **Interfaz limpia** sin opciones administrativas

#### **🔧 ADMINISTRADOR**
- ✅ Todos los permisos del enfermero +
- ✅ **Descargar reportes PDF diarios**
- ✅ Gestión de usuarios y sistema
- 📊 **Botón "Reporte PDF"** visible en dashboard

### **📋 REPORTE PDF PARA ADMINISTRADORES**
El reporte incluye información detallada para supervisión:
- 👩‍⚕️ **Qué enfermero atendió** cada paciente
- 📊 **NEWS Score obtenido** por cada caso
- ⏰ **Horarios exactos** de atención
- 📈 **Estadísticas por profesional** (rendimiento diario)
- 🏥 **Resumen general** del turno

### **🚨 PRIORIZACIÓN INTELIGENTE DE CÓDIGOS ROJOS**
Cuando hay múltiples pacientes críticos, el sistema ordena automáticamente por:
1. **NEWS Score más alto** (mayor criticidad médica)
2. **Tiempo de espera** (>30 min = mayor prioridad)
3. **Edad avanzada** (+65 años)
4. **Signos vitales ultra-críticos** (saturación <85%, etc.)

### **🎯 ELIMINACIÓN DE REDUNDANCIAS**
- ❌ **Eliminado**: Página separada "Triage Completo"
- ❌ **Eliminado**: Navegación entre páginas múltiples
- ❌ **Eliminado**: Print statements de debugging
- ❌ **Eliminado**: Código comentado innecesario
- ❌ **Eliminado**: Console.log excesivos

---

## 🏥 **FUNCIONALIDADES MÉDICAS**

### **🏥 Diseño Hospitalario**
- **Interfaz médica** intuitiva y limpia
- **Colores estándar** (Rojo/Amarillo/Verde)
- **Dashboard único** sin distracciones
- **Mobile-first** para tablets/celulares

### **🔒 Seguridad Médica**
- **Autenticación por DNI** profesional
- **Datos en SQLite** local (privacidad TOTAL)
- **Sin conexión externa** requerida
- **Cache inteligente** para velocidad crítica

---

## 🎯 **CLASIFICACIÓN MÉDICA**

### **🔴 ROJO (NEWS ≥7)**
- **Emergencia crítica**
- **Atención inmediata**
- **Riesgo vital**

### **🟡 AMARILLO (NEWS 5-6)**
- **Urgencia moderada** 
- **Atención en 30 minutos**
- **Monitoreo frecuente**

### **🟢 VERDE (NEWS 0-4)**
- **Sin riesgo inmediato**
- **Atención en 60 minutos**
- **Rutinario**

---

## 🛠️ **COMANDOS DE MANTENIMIENTO**

### **🚀 Iniciar Sistema**
```bash
# Desarrollo local
python manage.py runserver

# Con datos de ejemplo
python manage.py demo_data

# Optimizar base de datos
python manage.py optimize_db
```

### **👨‍⚕️ Gestión de Usuarios**
```bash
# Crear administrador
python manage.py setup_admin

# Limpiar datos antiguos
python manage.py cleanup_old_data
```

### **🔧 Mantenimiento**
```bash
# Reset completo
python manage.py flush
python manage.py migrate
python manage.py setup_admin

# Performance check
python manage.py performance_check
```

---

## 🏥 **DESPLIEGUE EN HOSPITAL**

### **Para PC Local (Demo/Testing)**
- Usar `./start.sh demo`
- Acceso: http://127.0.0.1:8000

### **Para Red Hospitalaria**
- Usar `./start.sh red` 
- Acceso: http://[IP-DEL-SERVIDOR]:8000
- Configurar IP fija en router

### **Para Producción**
- Cambiar contraseñas por defecto
- Configurar backup de base de datos
- Documentar procedimientos médicos

---

## 📞 **SOPORTE TÉCNICO**

### **Problemas Comunes**
- **Puerto ocupado**: Cambiar puerto en `start.sh`
- **Sin Python**: Instalar Python 3.8+
- **Permisos**: Ejecutar como administrador

### **Logs del Sistema**
- Ver terminal donde se ejecuta `./start.sh`
- Errores aparecen automáticamente

---

## 📈 **ESTADO DEL PROYECTO**

✅ **Sistema 100% Funcional**  
✅ **Optimizado para Hospitales**  
✅ **Sin Bugs Conocidos**  
✅ **Listo para Producción**  
✅ **Documentación Completa**

---

**💙 Desarrollado para salvar vidas - Cada segundo cuenta en emergencias**

*Sistema hospitalario profesional - Octubre 2025*