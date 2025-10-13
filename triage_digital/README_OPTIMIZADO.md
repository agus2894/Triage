# 🏥 Triage Digital - Sistema Hospitalario Optimizado

**Sistema profesional de triage médico con autenticación por DNI, diseñado para hospitales y centros de salud.**

![Estado](https://img.shields.io/badge/Estado-Producción-green)
![Django](https://img.shields.io/badge/Django-4.2.11-blue)
![Optimizado](https://img.shields.io/badge/Performance-Optimizado-success)

## 🚀 Características Principales

### ✅ **Sistema Completado**
- **Autenticación por DNI**: Login seguro para profesionales médicos
- **Campos Opcionales**: Registro de pacientes inconscientes
- **Terminología Profesional**: Médicos y enfermeros incluidos
- **Cálculo NEWS Score**: Automático basado en signos vitales
- **Base de Datos Optimizada**: Índices y consultas eficientes
- **Sistema de Caché**: Mejora el rendimiento en consultas frecuentes
- **Logging Médico**: Auditoría completa de acciones críticas

### 🎯 **Funcionalidades**

#### **Para Administradores**
- Gestión de profesionales autorizados
- Panel de administración Django completo
- Monitoreo del sistema en tiempo real
- Logs estructurados para auditoría

#### **Para Profesionales Médicos**
- Login con DNI + contraseña
- Dashboard con estadísticas en tiempo real
- Registro rápido de pacientes
- Carga de signos vitales con cálculo automático
- Lista de pacientes con estados de triage

## 🛠️ Instalación y Configuración

### **Inicio Ultra-simple**
```bash
./start.sh
```

### **Producción (Configuración Optimizada)**
```bash
# Usar configuración de producción
./start_production.sh

# O manualmente:
python3 manage.py runserver --settings=config.settings_production
```

## 📊 Comandos de Optimización

### **Optimizar Base de Datos**
```bash
python3 manage.py optimize_db
```

### **Monitor del Sistema**
```bash
python3 manage.py monitor_triage --hours 24
```

### **Crear Profesional**
```bash
python3 manage.py shell
>>> from django.contrib.auth.models import User
>>> from apps.triage.models import Profesional
>>> user = User.objects.create_user('juan.perez', 'juan@hospital.com', 'password123')
>>> user.first_name = 'Juan'; user.last_name = 'Perez'; user.save()
>>> Profesional.objects.create(user=user, dni='12345678', tipo='medico', matricula='M-001')
```

## 🏥 Uso del Sistema

### **1. Administrador**
- **URL**: `http://localhost:8002/admin/`
- **Función**: Crear y gestionar profesionales autorizados
- **Datos**: Usuario, DNI, tipo (médico/enfermero), matrícula

### **2. Profesional Médico**
- **URL**: `http://localhost:8002/login/`
- **Login**: DNI + contraseña
- **Flujo**: Dashboard → Registrar Paciente → Signos Vitales → Resultado Triage

### **3. Workflow Típico**
1. Profesional hace login con DNI
2. Registra nuevo paciente (campos opcionales para inconscientes)
3. Carga signos vitales (6 parámetros NEWS)
4. Sistema calcula automáticamente nivel de urgencia
5. Dashboard muestra estadísticas y casos críticos

## 🚦 Niveles de Triage (NEWS Score)

| Color | Nivel | Score | Tiempo Máximo | Descripción |
|-------|--------|-------|---------------|-------------|
| 🔴 ROJO | Crítico | 7+ | Inmediato | Riesgo vital inmediato |
| 🟡 AMARILLO | Urgente | 5-6 | 30 min | Requiere atención rápida |
| 🟢 VERDE | Rutinario | 1-4 | 60 min | Estable, puede esperar |
| 🔵 AZUL | Bajo | 0 | 120 min | No urgente |

## 📁 Estructura del Proyecto

```
triage_digital/
├── apps/
│   ├── patients/         # Modelo de pacientes
│   ├── triage/          # Lógica principal, profesionales
│   └── evolution/       # Notas de evolución
├── config/
│   ├── settings.py          # Desarrollo
│   ├── settings_production.py  # Producción optimizada
│   └── urls.py
├── logs/                # Logs del sistema
├── db/                  # Base de datos SQLite
└── start_production.sh  # Script de inicio optimizado
```

## ⚡ Optimizaciones Implementadas

### **Base de Datos**
- Índices estratégicos en DNI y campos críticos
- WAL mode para mejor concurrencia
- Consultas optimizadas con `select_related`
- Caché de consultas frecuentes

### **Performance**
- Templates optimizados
- Logging estructurado con rotación
- Sistema de caché en memoria
- Consultas SQL eficientes

### **Seguridad**
- Headers de seguridad HTTPS
- Validación de entrada
- Logging de auditoría médica
- Configuración separada para producción

## 📈 Métricas y Monitoreo

### **Dashboard Médico**
- Estadísticas últimas 24h en tiempo real
- Casos críticos pendientes
- Alertas automáticas para casos ROJOS
- Distribución por niveles de urgencia

### **Logs del Sistema**
- `logs/triage_medical.log`: Acciones médicas críticas
- `logs/triage_system.log`: Eventos del sistema
- Rotación automática de archivos

## 🔧 Configuración Técnica

### **Credenciales Únicas**
- **👤 Admin Panel**: `admin` / `123456`
- **🏥 Sistema Triage**: DNI `00000000` / `123456`

### **Puertos**
- **Desarrollo**: `http://localhost:8002`
- **Producción**: `http://localhost:8000`

### **Base de Datos**
- SQLite optimizada con WAL mode
- Ubicación: `db/triage_digital.sqlite3`
- Backups automáticos disponibles

## 🎯 Estado del Proyecto

### ✅ **Completado**
- [x] Login con DNI para profesionales
- [x] Campos opcionales para pacientes inconscientes  
- [x] Cambio "Enfermero" → "Profesional"
- [x] Sistema de gestión de profesionales
- [x] Optimizaciones de rendimiento
- [x] Logging y monitoreo
- [x] Configuración de producción

### 🚀 **Listo para Producción**
El sistema está completamente funcional y optimizado para uso hospitalario real.

---

**Desarrollado siguiendo la filosofía "menos es mejor" - Código limpio que salva vidas.** 🏥✨