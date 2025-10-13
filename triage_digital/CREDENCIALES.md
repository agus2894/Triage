# 🔐 CREDENCIALES TRIAGE DIGITAL

## 🎯 UN SOLO ADMIN - FILOSOFÍA "MENOS ES MEJOR"

### 📊 **Panel de Administración**
- **URL**: http://localhost:8002/admin/
- **Usuario**: `admin`
- **Contraseña**: `123456`

### 🏥 **Sistema de Triage**
- **URL**: http://localhost:8002/login/
- **DNI**: `00000000`
- **Contraseña**: `123456`

---

## 🚀 **Inicio Rápido**
```bash
./start.sh
```

## 🛠️ **Resetear Admin**
```bash
python3 manage.py setup_admin
```

## 📋 **Flujo de Trabajo**
1. **Admin** → Crea profesionales en el panel admin
2. **Profesional** → Login con DNI → Registra pacientes → Carga signos vitales
3. **Sistema** → Calcula NEWS Score automáticamente → Asigna color de triage
4. **Profesional** → Marca pacientes como "Atendido"

---
**Sistema optimizado siguiendo "menos es mejor" - Un admin, credenciales simples, máxima eficacia** 🏥✨