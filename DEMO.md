# 🎯 TRIAGE DIGITAL - DEMO LOCAL

> **Demo del Sistema Hospitalario en PC Local**  
> *Sin necesidad de red - Perfecto para demostraciones*

## 🚀 **INICIO RÁPIDO**

```bash
cd triage_digital
./start.sh demo
```

**¡Y listo!** El sistema estará funcionando en: **http://127.0.0.1:8000**

## 📱 **DEMO PWA (Progressive Web App)**

### **Instalar como App Desktop:**
1. Abrir Chrome → `http://127.0.0.1:8000`
2. Click en el ícono "+" de la barra de direcciones
3. "Instalar Triage Digital"
4. ¡Ya tienes la app en el escritorio!

### **Funciona Offline:**
- Desconecta internet
- La app sigue funcionando
- Ideal para emergencias

## 🏥 **CREDENCIALES DEMO**

### **Login Profesional:**
- **DNI**: `00000000`
- **Contraseña**: `123456`
- **URL**: http://127.0.0.1:8000

### **Administrador:**
- **Usuario**: `admin`
- **Contraseña**: `123456`
- **URL**: http://127.0.0.1:8000/admin/

## 🎭 **DATOS DE DEMOSTRACIÓN**

El sistema incluye **5 pacientes ficticios** con diferentes niveles de urgencia:

- 🔴 **María Elena García** - NEWS 8 (ROJO) - Dolor torácico
- 🟡 **Carlos Rodríguez** - NEWS 5 (AMARILLO) - Dificultad respiratoria  
- 🟡 **Roberto Fernández** - NEWS 6 (AMARILLO) - Mareos y confusión
- 🟢 **Ana Martínez** - NEWS 2 (VERDE) - Cefalea
- 🟢 **Sofía López** - NEWS 0 (VERDE) - Dolor abdominal

## ⚡ **FUNCIONALIDADES DEMO**

### **📊 Dashboard en Tiempo Real**
- Lista de pacientes actualizada cada 30 segundos
- Clasificación por colores (Rojo/Amarillo/Verde)
- Botones "ATENDIDO" funcionales

### **📋 Triage Completo**
- Formulario unificado: Paciente + Signos + Triage
- Cálculo automático NEWS Score
- Resultado instantáneo con colores

### **📱 Mobile-First**
- Interfaz optimizada para tablets
- Funciona perfecto en pantallas táctiles
- PWA instalable

## 🔧 **COMANDOS ÚTILES**

```bash
# Iniciar demo con datos frescos
./start.sh demo

# Solo desarrollo (sin datos demo)
./start.sh

# Regenerar datos demo
python3 manage.py demo_data --reset

# Parar servidor
Ctrl+C
```

## 🎯 **PERFECTA PARA:**

- ✅ **Demostraciones** a directivos hospitalarios
- ✅ **Capacitación** de personal médico
- ✅ **Testing** de funcionalidades
- ✅ **Validación** del flujo de trabajo
- ✅ **Presentaciones** comerciales

## 📈 **PRÓXIMOS PASOS**

1. **Validar** funcionalidades con el equipo médico
2. **Personalizar** según necesidades del hospital
3. **Desplegar** en red hospitalaria real
4. **Capacitar** al personal médico

---

**🏥 Sistema listo para salvar vidas - Cada segundo cuenta**

*Demo creada el 22 de Octubre de 2025*