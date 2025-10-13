# Triage Digital - Sistema de clasificación hospitalaria

**Integrantes:** Gordaliza Florencia - Lamas Gonzalo

Sistema de clasificación hospitalaria asistido por software utilizando la escala NEWS (National Early Warning Score).

## Estructura del Proyecto

```
Triage/
├── triage_digital/          # Aplicación Django principal
├── .venv/                   # Entorno virtual Python
├── .git/                    # Repositorio Git
└── Triage Digital.docx      # Documentación del proyecto
```

## Inicio Rápido

```bash
cd triage_digital/
source ../.venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Funcionalidades

- 🔐 Autenticación de enfermeros
- 👥 Registro de pacientes
- 📊 Cálculo automático NEWS Score
- 🚨 Clasificación por colores (Rojo/Amarillo/Verde)
- 📈 Dashboard en tiempo real
- 📝 Notas de evolución

---
**Proyecto Final - 2025**