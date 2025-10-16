# 🏥 Triage Digital - Sistema Hospitalario Completo

> **Sistema de clasificación hospitalaria ultra-optimizado**  
> *Filosofía: "Menos es mejor" - Máxima eficiencia, mínima complejidad*

## 🚀 Instalación Súper Rápida

```bash
git clone https://github.com/agus2894/Triage.git
cd Triage
python3 -m venv .venv
source .venv/bin/activate
cd triage_digital
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py setup_admin
python3 manage.py runserver 8003
```

**¡Listo! Sistema ejecutándose en http://127.0.0.1:8003/**

### 🔑 **Acceso Inicial**
- **Admin**: `admin` / `123456` (cambiar en producción)
- **Triage**: DNI `00000000` / `123456`

## ⚡ Características Principales

### 🔐 **Autenticación Profesional**
- Login por **DNI + Contraseña** (no username)
- Admin único: `admin` / `123456`
- Interfaz de login profesional y limpia

### 🏥 **Sistema de Triage Médico Real**
- **📋 Formulario Unificado** - Paciente + Signos Vitales + Triage en UNA pantalla
- **🚨 NEWS Score Automático** - Cálculo instantáneo con clasificación por colores
- **⏱️ Sidebar en Tiempo Real** - Lista de pacientes que se actualiza cada 30s
- **✅ Botones de Atendido** - Marcar pacientes como atendidos con un click
- **📱 Totalmente Responsive** - Funciona perfecto en tablets y móviles

### ⚡ **Ultra-Optimización 2025**
- **Código minimalista** - Eliminadas funciones redundantes
- **Caché médico** - 3min para datos críticos de triage
- **Base de datos WAL** - SQLite optimizado para concurrencia
- **Índices inteligentes** - Consultas sub-segundo
- **Menos es más** - Solo lo esencial que salva vidas

## 🎯 Clasificación por Colores

- 🔴 **ROJO**: Emergencia inmediata (NEWS ≥7)
- 🟡 **AMARILLO**: Urgencia - 30min máx (NEWS 4-6)
- 🟢 **VERDE**: No urgente - 60min máx (NEWS 0-3)

## 🛠️ Tecnologías

- **Backend**: Django 4.2.11 + SQLite con WAL mode
- **Frontend**: Bootstrap 5 CDN + AJAX
- **Cache**: Sistema multi-nivel inteligente
- **Autenticación**: DNI personalizada
- **Base de datos**: Ultra-optimizada con índices

## � **Estado Final del Sistema**

### 📊 **Funciones Esenciales (Solo 4)**
1. `dashboard_principal` - Dashboard médico con pacientes
2. `triage_completo` - Formulario unificado (GAME CHANGER)
3. `cargar_signos_vitales` - Para pacientes sin triage
4. `api_lista_pacientes` - Sidebar en tiempo real

### 🗂️ **Templates Optimizados (Solo 5)**
- `base.html` - Template base responsive
- `dashboard.html` - Dashboard principal 
- `triage_completo.html` - Formulario unificado
- `cargar_signos.html` - Signos vitales legacy
- `login.html` - Autenticación médica

## �🎯 Optimizaciones Implementadas

### 🧹 **Limpieza de Código (Octubre 2025)**
- ✅ Eliminadas **3 funciones redundantes** de views.py
- ✅ Removidos **2 templates innecesarios**
- ✅ Imports no utilizados eliminados automáticamente
- ✅ URLs simplificadas y optimizadas

### 🚀 **Optimización de Base de Datos**
- ✅ **3 índices críticos** agregados para pacientes
- ✅ Modo WAL activado para mejor concurrencia
- ✅ Cache de 64MB configurado
- ✅ Consultas optimizadas con prefetch_related

### 🛡️ **Configuración Producción**
- ✅ Variables de entorno implementadas
- ✅ Configuraciones de seguridad HTTPS
- ✅ Sesiones optimizadas para turnos hospitalarios
- ✅ Cache inteligente con limpieza automática

## 📋 Funcionalidades Completas

### ✅ **Sistema Core**
- ✅ Autenticación por DNI + contraseña
- ✅ Admin simplificado para crear profesionales
- ✅ Registro de pacientes (campos opcionales para inconscientes)
- ✅ Carga de signos vitales (6 parámetros NEWS)
- ✅ Cálculo automático NEWS Score
- ✅ Estados de atención con botón ATENDIDO
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Filtros avanzados por estado y criticidad

### 📊 **Parámetros NEWS Score**
1. **Frecuencia Respiratoria** (12-20 normal)
2. **Saturación de Oxígeno** (≥96% normal)  
3. **Tensión Arterial Sistólica** (110-219 normal)
4. **Frecuencia Cardíaca** (51-90 normal)
5. **Nivel de Conciencia** (A=Alerta, V=Verbal, P=Dolor, U=Inconsciente)
6. **Temperatura** (36.1-38.0°C normal)

## 🚀 Modos de Ejecución

### **Desarrollo** (por defecto)
```bash
./start.sh
```

### **Producción**
```bash
./start.sh prod
```

## 👥 Credenciales de Acceso

### **🔑 Administrador del Sistema**
- **Usuario**: `admin`
- **Contraseña**: `123456`
- **URL**: http://localhost:8002/admin/

### **🏥 Profesional de Prueba**
- **DNI**: `00000000`
- **Contraseña**: `123456`
- **URL**: http://localhost:8002/

## 📁 Estructura Minimalista

```
triage_digital/
├── manage.py            # Django management
├── requirements.txt     # Dependencias mínimas
├── requirements.txt     # Dependencias
├── config/             # Configuración Django
├── apps/               # Aplicaciones
│   ├── patients/       # Gestión pacientes
│   ├── triage/         # NEWS Score + Auth
│   └── evolution/      # Notas evolución
└── db/                 # Base de datos
```

## 🎯 Beneficios del Sistema

- ⚡ **Velocidad**: Ultra-optimizado para situaciones críticas
- 🎨 **Simplicidad**: Interfaz intuitiva, sin curva de aprendizaje
- 🔒 **Seguridad**: Autenticación robusta por DNI
- 📊 **Precisión**: NEWS Score automatizado y estandarizado
- 🚀 **Escalabilidad**: Listo para producción hospitalaria

---

## 🎯 **Estado del Proyecto - Octubre 2025**

✅ **Sistema 100% Funcional**  
✅ **Optimización Completa** - "Menos es más" aplicado  
✅ **Bug Crítico Solucionado** - Lista de pacientes funcionando  
✅ **Base de Datos Indexada** - Rendimiento máximo  
✅ **Código Limpio** - Sin funciones redundantes  
✅ **Listo para Producción** - Variables de entorno configuradas  

---

**💙 Desarrollado para salvar vidas - Cada segundo cuenta en emergencias**

*Sistema creado siguiendo la filosofía "menos es mejor" - Máxima eficiencia, mínima complejidad*

**🏥 Proyecto Hospitalario - 2025**