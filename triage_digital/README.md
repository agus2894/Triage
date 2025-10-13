# Triage Digital - Sistema de clasificación hospitalaria

**Integrantes:** Gordaliza Florencia - Lamas Gonzalo

## Descripción del Proyecto

Triage Digital es una aplicación web multiplataforma (Windows y Linux) diseñada para apoyar al personal de salud en el proceso de triaje en guardias hospitalarias. El sistema permite clasificar de manera rápida y estandarizada a los pacientes que ingresan, basándose en parámetros clínicos objetivos y utilizando la escala NEWS (National Early Warning Score).

## Objetivo Principal

Optimizar la toma de decisiones en el ámbito de la guardia hospitalaria, asegurando que los pacientes sean atendidos según su nivel real de urgencia. Con Triage Digital, el enfermero puede registrar datos del paciente, ingresar sus signos vitales y recibir automáticamente una clasificación por color:

- 🔴 **Rojo**: Emergencia inmediata
- 🟡 **Amarillo**: Urgencia (atención en menos de 30 minutos)
- 🟢 **Verde**: No urgente (atención en menos de 60 minutos)

## Estructura del Proyecto

```
triage_digital/
├── manage.py
├── config/                 # Configuración Django
├── apps/                   # Aplicaciones Django
│   ├── authentication/     # Sistema de login enfermeros
│   ├── patients/          # Gestión de pacientes
│   ├── triage/            # Lógica NEWS Score
│   ├── dashboard/         # Panel estadístico
│   └── evolution/         # Notas de evolución
├── templates/             # Templates HTML
├── static/               # CSS, JS, imágenes
└── db/                   # Base de datos SQLite
```

## Funcionalidades Implementadas

### ✅ Core del Sistema
- [ ] Autenticación de enfermeros
- [ ] Registro de pacientes (nombre, apellido, DNI, edad, motivo)
- [ ] Carga de signos vitales (6 parámetros NEWS)
- [ ] Cálculo automático del NEWS Score
- [ ] Clasificación visual por colores
- [ ] Notas de evolución
- [ ] Dashboard con estadísticas en tiempo real

### 📊 Parámetros del NEWS Score
1. **Frecuencia Respiratoria** (respiraciones/min)
2. **Saturación de Oxígeno** (%)
3. **Tensión Arterial Sistólica** (mmHg)
4. **Frecuencia Cardíaca** (latidos/min)
5. **Nivel de Conciencia** (AVPU)
6. **Temperatura** (°C)

## Instalación y Uso

1. **Clonar el repositorio**
2. **Crear entorno virtual**
3. **Instalar dependencias**
4. **Ejecutar migraciones**
5. **Crear superusuario**
6. **Iniciar servidor**

## Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite
- **Multiplataforma**: Windows/Linux

## Beneficios Esperados

- Agilizar el trabajo de enfermería en el primer contacto
- Estandarizar criterios de clasificación
- Facilitar gestión de demanda mediante panel visual
- Mejorar seguridad del paciente priorizando casos críticos

---

**Proyecto Final - 2025**