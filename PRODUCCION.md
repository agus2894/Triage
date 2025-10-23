# 🏥 TRIAGE DIGITAL - CONFIGURACIÓN DE PRODUCCIÓN

## 📋 **CHECKLIST PRE-DESPLIEGUE**

### **⚙️ Configuración del Sistema**
- [ ] Python 3.8+ instalado
- [ ] Git configurado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Base de datos inicializada

### **🔐 Seguridad**
- [ ] Cambiar contraseña admin por defecto
- [ ] Crear DNIs de usuarios médicos reales
- [ ] Configurar backup automático
- [ ] Verificar permisos de archivos

### **🌐 Red y Acceso**
- [ ] Configurar IP fija para servidor
- [ ] Abrir puerto 8000 en firewall
- [ ] Probar acceso desde otras PCs
- [ ] Documentar IP para personal médico

---

## 🛠️ **COMANDOS DE MANTENIMIENTO**

### **Backup de Base de Datos**
```bash
# Crear backup
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restaurar backup
cp backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

### **Limpieza de Datos Antiguos**
```bash
# Limpiar datos de más de 30 días
python3 manage.py shell -c "
from apps.patients.models import Paciente
from django.utils import timezone
from datetime import timedelta
fecha_limite = timezone.now() - timedelta(days=30)
Paciente.objects.filter(fecha_ingreso__lt=fecha_limite).delete()
"
```

### **Crear Nuevos Usuarios Médicos**
```bash
python3 manage.py shell -c "
from django.contrib.auth.models import User
from apps.triage.models import Profesional
user = User.objects.create_user('12345678', password='nueva_password')
Profesional.objects.create(user=user, dni='12345678', tipo='medico', activo=True)
"
```

---

## 🚨 **PROCEDIMIENTOS DE EMERGENCIA**

### **Si el Sistema No Responde**
1. Verificar que el proceso esté ejecutándose
2. Reiniciar: `Ctrl+C` y luego `./start.sh`
3. Si persiste: reiniciar PC

### **Si la Base de Datos se Corrompe**
1. Parar el sistema
2. Restaurar último backup
3. Reiniciar sistema
4. Verificar funcionalidad

### **Si Hay Problemas de Red**
1. Verificar IP del servidor
2. Ping desde otras PCs
3. Revisar firewall/antivirus
4. Reiniciar router si es necesario

---

## 📊 **MONITOREO DEL SISTEMA**

### **Métricas Importantes**
- Tiempo de respuesta < 2 segundos
- Disponibilidad > 99%
- Espacio en disco > 1GB libre
- RAM disponible > 500MB

### **Logs a Revisar**
- Terminal donde corre `./start.sh`
- Errores de Python/Django
- Accesos fallidos al login

---

## 🔄 **ACTUALIZACIONES**

### **Obtener Nueva Versión**
```bash
git pull origin main
pip install -r requirements.txt
python3 manage.py migrate
./start.sh
```

### **Rollback si Hay Problemas**
```bash
git checkout HEAD~1
./start.sh
```

---

## 📞 **CONTACTOS DE SOPORTE**

### **Desarrollador Principal**
- **Email**: [email del desarrollador]
- **Teléfono**: [teléfono de emergencia]

### **IT Hospital**
- **Extension**: [extension interna]
- **Email**: [email IT hospital]

---

## 📈 **OPTIMIZACIONES RECOMENDADAS**

### **Para Mejor Rendimiento**
- Ejecutar en SSD si es posible
- Mínimo 4GB RAM
- CPU dual-core o mejor
- Conexión Ethernet estable

### **Para Mayor Seguridad**
- Cambiar puertos por defecto
- Configurar VPN para acceso remoto
- Implementar backup automático diario
- Auditorías de acceso mensuales

---

**🏥 Sistema optimizado para salvar vidas - Configuración profesional hospitalaria**

*Guía de producción - Octubre 2025*