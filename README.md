# 🏥 TRIAGE DIGITAL - SISTEMA HOSPITALARIO INTEGRADO

> **Sistema de clasificación médica de emergencia - TODO INTEGRADO EN UNA PANTALLA**  
> *Dashboard unificado - Sin páginas separadas - Optimizado para velocidad crítica*

---


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

# 5. Iniciar servidor
python manage.py runserver

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



*Sistema hospitalario profesional - Octubre 2025*