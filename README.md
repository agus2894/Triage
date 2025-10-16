# 🏥 Triage Digital - Sistema Hospitalario Completo

> **Sistema de clasificación hospitalaria ultra-optimizado**  
> *Filosofía: "Menos es mejor" - Máxima eficiencia, mínima complejidad*

## 🚀 Inicio Rápido (Un Solo Comando)

```bash
git clone https://github.com/agus2894/Triage.git
cd Triage/triage_digital
./start.sh
```

**¡Listo! El sistema estará ejecutándose en http://localhost:8002**

## ⚡ Características Principales

### 🔐 **Autenticación Profesional**
- Login por **DNI + Contraseña** (no username)
- Admin único: `admin` / `123456`
- Interfaz de login profesional y limpia

### 🏥 **Sistema de Triage Completo**
- **NEWS Score automático** - Clasificación según signos vitales
- **Estados de atención**: ESPERANDO → EN_ATENCIÓN → ATENDIDO
- **Dashboard optimizado** con filtros inteligentes
- **Gestión de pacientes** con campos opcionales para inconscientes

### ⚡ **Ultra-Optimización**
- **Caché inteligente** multi-nivel (1min crítico, 2min dashboard, 5min pacientes)
- **Índices de BD** optimizados para consultas rápidas
- **CSS minificado** para carga instantánea
- **Logging mínimo** - Solo errores críticos

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
├── start.sh              # 🚀 EL SCRIPT DEFINITIVO
├── manage.py            # Django management
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

**💙 Desarrollado para salvar vidas - Cada segundo cuenta en emergencias**

*Sistema creado siguiendo la filosofía "menos es mejor" - Máxima eficiencia, mínima complejidad*

---

**Proyecto Final - 2025**