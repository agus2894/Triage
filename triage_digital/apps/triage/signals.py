"""
Signals automáticos para optimización inteligente del sistema.
Se ejecutan automáticamente sin intervención del usuario.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.db import connection
from django.utils import timezone
from datetime import timedelta
import threading
import logging

from .models import SignosVitales, Profesional
from apps.patients.models import Paciente

logger = logging.getLogger(__name__)

# Contador de operaciones para optimización automática
OPERATIONS_COUNTER = 'triage_operations_count'
LAST_OPTIMIZATION = 'triage_last_optimization'


def increment_operations():
    """Incrementa el contador de operaciones."""
    current = cache.get(OPERATIONS_COUNTER, 0)
    cache.set(OPERATIONS_COUNTER, current + 1, timeout=3600)  # 1 hora
    return current + 1


def should_optimize():
    """Determina si es necesario optimizar automáticamente."""
    operations = cache.get(OPERATIONS_COUNTER, 0)
    last_opt = cache.get(LAST_OPTIMIZATION)
    
    # Optimizar cada 100 operaciones O cada 2 horas
    if operations >= 100:
        return True
    
    if last_opt:
        time_since = timezone.now() - last_opt
        if time_since > timedelta(hours=2):
            return True
    
    return False


def auto_optimize_background():
    """Optimización automática en background thread."""
    try:
        with connection.cursor() as cursor:
            # Optimizaciones rápidas y no bloqueantes
            cursor.execute('PRAGMA optimize;')
            cursor.execute('PRAGMA wal_checkpoint(PASSIVE);')
            
        # Resetear contador y marcar última optimización
        cache.set(OPERATIONS_COUNTER, 0, timeout=3600)
        cache.set(LAST_OPTIMIZATION, timezone.now(), timeout=86400)
        
        logger.info("Auto-optimización automática completada")
        
    except Exception as e:
        logger.warning(f"Error en auto-optimización: {e}")


@receiver(post_save, sender=SignosVitales)
def optimize_after_triage(sender, instance, created, **kwargs):
    """Optimización automática después de crear triage."""
    if created:
        count = increment_operations()
        
        # Auto-optimización inteligente cada 100 triages
        if should_optimize():
            # Ejecutar en thread separado para no bloquear
            thread = threading.Thread(target=auto_optimize_background)
            thread.daemon = True
            thread.start()


@receiver(post_save, sender=Paciente)
def cache_invalidation_patient(sender, instance, **kwargs):
    """Invalidar cache automáticamente cuando cambia un paciente."""
    # Invalidar caches específicos para que el dashboard se actualice
    cache_keys = [
        'dashboard_stats',
        'patients_waiting',
        f'patient_{instance.id}',
    ]
    cache.delete_many(cache_keys)


@receiver(post_delete, sender=Paciente)
def cleanup_after_patient_delete(sender, instance, **kwargs):
    """Limpieza automática después de eliminar paciente."""
    increment_operations()
    
    # Invalidar caches relacionados
    cache.delete_many([
        'dashboard_stats',
        'patients_waiting',
        f'patient_{instance.id}',
    ])


# Signal para limpieza automática de datos antiguos
def auto_cleanup_old_data():
    """Limpieza automática de datos antiguos cada semana."""
    try:
        # Solo en horarios de bajo uso (2-6 AM)
        current_hour = timezone.now().hour
        if not (2 <= current_hour <= 6):
            return
        
        # Verificar si ya se hizo limpieza esta semana
        last_cleanup = cache.get('last_auto_cleanup')
        if last_cleanup:
            days_since = (timezone.now().date() - last_cleanup).days
            if days_since < 7:
                return
        
        # Limpieza automática de datos >6 meses
        fecha_limite = timezone.now() - timedelta(days=180)
        
        # Eliminar pacientes atendidos muy antiguos (batch pequeño)
        old_patients = Paciente.objects.filter(
            estado_atencion='ATENDIDO',
            fecha_atencion__lt=fecha_limite
        )[:50]  # Solo 50 por vez para no saturar
        
        deleted_count = 0
        for patient in old_patients:
            patient.delete()
            deleted_count += 1
        
        if deleted_count > 0:
            logger.info(f"Auto-limpieza: eliminados {deleted_count} pacientes antiguos")
            
            # Optimización post-limpieza
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA incremental_vacuum;')
        
        # Marcar última limpieza
        cache.set('last_auto_cleanup', timezone.now().date(), timeout=86400*7)
        
    except Exception as e:
        logger.warning(f"Error en auto-limpieza: {e}")


# Programar limpieza automática cada día
from django.core.management.base import BaseCommand
from django.core.management import call_command


class AutoMaintenanceThread(threading.Thread):
    """Thread para mantenimiento automático en background."""
    
    def __init__(self):
        super().__init__()
        self.daemon = True
        
    def run(self):
        import time
        while True:
            try:
                # Ejecutar cada 6 horas
                time.sleep(6 * 3600)
                auto_cleanup_old_data()
            except Exception as e:
                logger.error(f"Error en thread de mantenimiento: {e}")
                time.sleep(3600)  # Esperar 1 hora antes de reintentar


# Iniciar thread de mantenimiento automático
maintenance_thread = None

def start_auto_maintenance():
    """Inicia el mantenimiento automático."""
    global maintenance_thread
    if maintenance_thread is None or not maintenance_thread.is_alive():
        maintenance_thread = AutoMaintenanceThread()
        maintenance_thread.start()
        logger.info("Mantenimiento automático iniciado")