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

## 🚀 OPCIONES DE INSTALACIÓN

### 💻 **OPCIÓN 1: EJECUTABLE (Recomendado para usuarios finales)**

**📥 Descarga directa - Sin instalación**

1. **Descargar el ejecutable:**
   - Solicita el archivo `TriageDigital` al desarrollador
   - O compílalo siguiendo las instrucciones de desarrollo

2. **Ejecutar:**
   ```bash
   ./TriageDigital  # Linux/Mac
   # TriageDigital.exe  # Windows
   ```

3. **Acceder al sistema:**
   - El navegador se abrirá automáticamente en: `http://127.0.0.1:8001`
   - **Usuario:** `admin`
   - **Contraseña:** `123456`

**✅ Ventajas:** Sin dependencias, funciona inmediatamente, incluye todo lo necesario

---

### 🛠️ **OPCIÓN 2: INSTALACIÓN DESDE CÓDIGO FUENTE**

**📋 Requisitos previos:**
- Python 3.8 o superior
- Git
- 50MB de espacio libre

**⚡ Instalación paso a paso:**

```bash
# 1. Clonar el repositorio
git clone https://github.com/agus2894/Triage.git
cd Triage

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar la base de datos
cd triage_digital
python manage.py migrate
python manage.py setup_admin

# 5. Iniciar servidor
python manage.py runserver 127.0.0.1:8001
```

**🌐 Acceder al sistema:**
- URL: `http://127.0.0.1:8001`
- **Usuario:** `admin`
- **Contraseña:** `123456`

---

### 🔨 **OPCIÓN 3: COMPILAR TU PROPIO EJECUTABLE**

**Para desarrolladores que quieren crear el ejecutable:**

```bash
# 1. Seguir pasos de la Opción 2 hasta el paso 4

# 2. Instalar PyInstaller
pip install pyinstaller

# 3. Compilar ejecutable
pyinstaller app_launcher.py --onefile --name TriageDigital

# 4. El ejecutable estará en: dist/TriageDigital
```

## 🔑 **CREDENCIALES DE ACCESO**

### **👤 Usuario Administrador:**
- **Usuario:** `admin`
- **Contraseña:** `123456`
- **Permisos:** Acceso completo al sistema

### **🏥 Usuario Triage:**
- **DNI:** `00000000`
- **Contraseña:** `123456`  
- **Permisos:** Registro y clasificación de pacientes

> **⚠️ IMPORTANTE:** Cambiar las contraseñas por defecto en entorno de producción

## ❓ **SOLUCIÓN DE PROBLEMAS**

### **🐛 Problemas comunes:**

**Error: "No module named 'django'"**
```bash
# Asegúrate de activar el entorno virtual
source venv/bin/activate
pip install -r requirements.txt
```

**Error: "Port is already in use"**
```bash
# Usar otro puerto
python manage.py runserver 127.0.0.1:8002
```

**Error de base de datos**
```bash
# Recrear la base de datos
rm db/triage_digital.sqlite3
python manage.py migrate
python manage.py setup_admin
```

**El ejecutable no inicia**
```bash
# Verificar permisos (Linux/Mac)
chmod +x TriageDigital
./TriageDigital
```

### **� Soporte:**
- Reportar problemas en: [GitHub Issues](https://github.com/agus2894/Triage/issues)
- Desarrollador: agus2894

## 🏗️ **TECNOLOGÍAS UTILIZADAS**

- **Backend:** Django 5.2.5
- **Base de datos:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap
- **PDF:** ReportLab
- **Autenticación:** Django Auth System
- **Empaquetado:** PyInstaller

## 📁 **ESTRUCTURA DEL PROYECTO**

```
Triage/
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias Python
├── .gitignore               # Archivos ignorados por Git
└── triage_digital/          # Aplicación principal
    ├── manage.py            # Gestor de Django
    ├── app_launcher.py      # Launcher para ejecutable
    ├── db/                  # Base de datos SQLite
    ├── config/              # Configuración Django
    ├── apps/                # Aplicaciones del proyecto
    │   ├── triage/          # App principal de triage
    │   └── patients/        # App de gestión de pacientes
    └── logs/                # Archivos de log
```

## � **ESTADÍSTICAS DEL PROYECTO**

- **Líneas de código:** ~3,000
- **Archivos Python:** 25+
- **Modelos de BD:** 5 principales
- **Templates HTML:** 10+
- **Funcionalidades:** 15+ características médicas

---

## 📄 **LICENCIA**

Este proyecto es de código abierto y está disponible para uso educativo y profesional.

**Desarrollado con ❤️ para mejorar la atención hospitalaria** 🏥

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