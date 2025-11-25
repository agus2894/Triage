# 🏥 TRIAGE DIGITAL#
Sistema hospitalario para clasificación médica de emergencias con funcionalidad online y offline.

## EJECUCIÓN##
- **Con internet**: Colaboración en tiempo real (PostgreSQL)-


## ⚕️ FUNCIONES PRINCIPALES## 

### 🚨 **TRIAGE DE PACIENTES**###
- Registro de datos básicos del paciente-
- Medición de 6 signos vitales críticos-

- **Cálculo automático NEWS Score** (0-20 puntos)- 
- **Clasificación por colores**:
  - 🔴 **ROJO**: Emergencia (NEWS ≥ 7)  
  - 🟡 **AMARILLO**: Urgente (NEWS 3-6) 
  - 🟢 **VERDE**: No urgente (NEWS 0-2) 

### 📊 **DASHBOARD EN TIEMPO REAL**### 

- Lista de pacientes ordenada por prioridad-
- Actualización automática cada 30 segundos-
- Vista rápida del estado de cada paciente-
- Contadores de casos por categoría-

### 👥 **GESTIÓN DE PACIENTES**###

- Estados de atención (Esperando, En atención, Alta, etc.)-
- Marcado de pacientes como atendidos- Marcado de pacientes como atendidos


### 📋 **REPORTES MÉDICOS**###

- **PDF diario** con estadísticas completas-

- Información por profesional médico.
- Distribución de casos por severidad.
- Horarios y tiempos de atención.


### 🔒 **CONTROL DE ACCESO**###

- Sistema de autenticación por DNI-

- **Enfermeros**: Triage y gestión básica-
- **Administradores**: Acceso completo + reportes-


### **ONLINE** (Con Internet)###
- Base de datos compartida en Render-
- Colaboración en tiempo real entre profesionales-
- Sincronización automática de datos-
- Ideal para uso hospitalario diario-

### **OFFLINE** (Sin Internet)### 
- Base de datos local SQLite-
- Todos los usuarios funcionan igual-
- Datos de demostración incluidos-
- Perfecto para presentaciones y capacitaciones-


## 🔧 CARACTERÍSTICAS TÉCNICAS##
- **Framework**: Django 5.2.5-
- **Base de datos**: PostgreSQL (online) / SQLite (offline)-
- **Compatibilidad**: Detección automática de conectividad-
- **Interfaz**: Web responsiva, acceso desde cualquier navegador-

*Sistema desarrollado para optimizar la atención médica de emergencias**Sistema desarrollado para optimizar la atención médica de emergencias*