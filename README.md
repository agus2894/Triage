# 🏥 TRIAGE DIGITAL - SISTEMA HOSPITALARIO

> **Sistema completo de clasificación médica de emergencia y gestión hospitalaria**  
> *Aplicación web desarrollada en Django con interfaz moderna y funcionalidades médicas especializadas*

## 📋 DESCRIPCIÓN DEL PROYECTO

Triage Digital es un sistema hospitalario completo que permite:

- **🚨 Clasificación de Emergencias**: Sistema de triage según protocolos médicos
- **👥 Gestión de Pacientes**: Registro completo de datos médicos y personales  
- **👨‍⚕️ Gestión de Profesionales**: Control de personal médico y sus especialidades
- **📊 Reportes**: Generación de informes en PDF con estadísticas médicas
- **🔒 Seguridad**: Sistema de autenticación y control de acceso por roles

## ⚡ INSTALACIÓN RÁPIDA

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd Triage

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# En Windows: venv\Scripts\activate

# 3. Instalar dependencias
cd triage_digital
pip install -r ../requirements.txt

# 4. Configurar la base de datos
python manage.py migrate

# 5. Crear usuario administrador
python manage.py setup_admin

# 6. Iniciar servidor
python manage.py runserver

## 🔑 **CREDENCIALES DE ACCESO**

> **⚠️ IMPORTANTE**: Después de clonar el proyecto, **SIEMPRE** ejecutar `python manage.py setup_admin` para crear los usuarios del sistema.

### **📋 SETUP PARA NUEVOS DESARROLLADORES**

```bash
# Después de instalar dependencias y migrar:
python manage.py setup_admin

# ✅ Este comando crea automáticamente:
# - Usuario admin para Django Admin
# - Usuario administrador del sistema hospitalario  
# - Perfil profesional asociado
```

### **👨‍⚕️ ENFERMERO TRIAJERO** (Solo triage)
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

---

## 🗄️ **CONFIGURACIÓN DE BASE DE DATOS**

### **📂 Base de Datos Local**
- **Archivo**: `triage_digital/db/triage_digital.sqlite3`
- **Estado**: ❌ **NO está en Git** (buena práctica)
- **Cada desarrollador**: Tiene su propia BD local
- **Datos**: Se crean con `migrate` y `setup_admin`

### **🔄 Flujo para Nuevos Colegas**
```bash
git clone [repo]          # Solo código fuente
python manage.py migrate  # Crea tu BD local
python manage.py setup_admin  # Crea usuarios
# ¡Listo para trabajar!
```

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