# 🏥 Triage Digital  
Sistema web para la **clasificación y gestión de pacientes en emergencias**, diseñado para hospitales y centros de salud.  
Funciona tanto **online** (con base de datos centralizada) como **offline** (modo local), garantizando continuidad operativa incluso sin conexión.

---

## ✨ Características Principales

### 🚨 Triage Automatizado
- Registro rápido de datos del paciente  
- Medición de 6 signos vitales  
- Cálculo automático de **NEWS Score (0–20 pts)**  
- Clasificación inmediata:
  - 🔴 **Rojo – Emergencia (≥7)**
  - 🟡 **Amarillo – Urgente (3–6)**
  - 🟢 **Verde – No urgente (0–2)**

---

### 📊 Dashboard en Tiempo Real
- Listado ordenado por prioridad clínica  
- Actualización automática cada 30 segundos  
- Indicadores visuales de severidad  
- Contadores por categoría  

---

### 👥 Gestión de Pacientes
- Estados: *Esperando*, *En atención*, *Alta*  
- Historial por profesional  
- Control de flujo de pacientes  

---

### 📋 Reportes Automáticos
- Generación de PDF diario  
- Estadísticas por severidad y profesional  
- Tiempos y horarios de atención  

---

### 🔐 Control de Acceso
- Autenticación por DNI  
- Roles:
  - **Enfermería:** triage y gestión
  - **Administración:** control completo + reportes  

---

## 🌐 Modo Online
- Base de datos PostgreSQL en Render  
- Trabajo colaborativo entre múltiples profesionales  
- Conexión y sincronización en tiempo real  

## 📴 Modo Offline
- Base de datos local SQLite  
- Funcionalidad completa sin internet  
- Carga automática de datos locales  

---

## 🛠️ Tecnologías Utilizadas
- **Backend:** Django 5.2.5  
- **Base de datos:** PostgreSQL / SQLite  
- **Frontend:** HTML, CSS, JS (responsive)  
- **Reportes:** PDF automático  
- **Sincronización:** detección inteligente de conectividad  

---

## 🎯 Objetivo del Proyecto
Optimizar la atención en emergencias mediante un sistema rápido, intuitivo y confiable, diseñado para entornos hospitalarios de alta demanda.

---

## 🧑‍💻 Autor
**Gonzalo Agustín Lamas** – Técnico Universitario en Programación & Enfermero Profesional
