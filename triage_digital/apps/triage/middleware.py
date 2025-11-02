"""
Middleware para optimización automática e inteligente del sistema.
Funciona transparentemente sin intervención del usuario.
"""
import time
import logging
from django.core.cache import cache
from django.db import connection
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class AutoOptimizationMiddleware:
    """
    Middleware que optimiza automáticamente el sistema basado en uso.
    Totalmente transparente para el usuario final.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        
    def __call__(self, request):
        start_time = time.time()
        
        # Procesar request
        response = self.process_request(request)
        
        # Procesar response
        response = self.get_response(request)
        response = self.process_response(request, response, start_time)
        
        return response
    
    def process_request(self, request):
        """Optimizaciones antes de procesar la request."""
        # Incrementar contador de requests para estadísticas
        self.request_count += 1
        
        # Auto-optimización cada 500 requests
        if self.request_count % 500 == 0:
            self._auto_optimize_background()
        
        return None
    
    def process_response(self, request, response, start_time):
        """Optimizaciones después de procesar la response."""
        # Medir tiempo de respuesta
        response_time = (time.time() - start_time) * 1000  # en millisegundos
        
        # Si el response es muy lento (>2 segundos), optimizar automáticamente
        if response_time > 2000 and request.path.startswith('/triage/'):
            self._emergency_optimize()
        
        # Agregar headers de optimización (para debugging en desarrollo)
        if hasattr(request, 'user') and request.user.is_superuser:
            response['X-Triage-Response-Time'] = f'{response_time:.2f}ms'
            response['X-Triage-Optimized'] = 'auto'
        
        return response
    
    def _auto_optimize_background(self):
        """Optimización automática en background."""
        try:
            # Solo optimizar en horarios de bajo uso o si es necesario
            current_hour = timezone.now().hour
            
            # Optimización ligera siempre
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA optimize;')
                cursor.execute('PRAGMA wal_checkpoint(PASSIVE);')
            
            # Optimización más agresiva en horarios de bajo uso (2-6 AM)
            if 2 <= current_hour <= 6:
                with connection.cursor() as cursor:
                    cursor.execute('PRAGMA incremental_vacuum;')
                    cursor.execute('ANALYZE;')
            
            logger.info(f"Auto-optimización completada (requests: {self.request_count})")
            
        except Exception as e:
            logger.warning(f"Error en auto-optimización: {e}")
    
    def _emergency_optimize(self):
        """Optimización de emergencia para requests lentas."""
        try:
            # Limpiar cache que puede estar corrupto
            cache.clear()
            
            # Optimización rápida de BD
            with connection.cursor() as cursor:
                cursor.execute('PRAGMA optimize;')
            
            logger.warning("Optimización de emergencia ejecutada por response lenta")
            
        except Exception as e:
            logger.error(f"Error en optimización de emergencia: {e}")


class SmartCacheMiddleware:
    """
    Middleware para cache inteligente basado en patrones de uso.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Pre-cargar datos críticos en cache si no existen
        self._ensure_critical_cache()
        
        response = self.get_response(request)
        
        # Post-procesar para mejorar cache en próximas requests
        self._smart_preload(request)
        
        return response
    
    def _ensure_critical_cache(self):
        """Asegurar que datos críticos estén en cache."""
        # Cache de estadísticas básicas si no existe
        if not cache.get('dashboard_stats'):
            try:
                from apps.triage.models import SignosVitales
                from django.db.models import Count, Q
                from datetime import timedelta
                
                hace_24h = timezone.now() - timedelta(hours=24)
                stats = SignosVitales.objects.filter(
                    fecha_hora__gte=hace_24h,
                    paciente__activo=True
                ).aggregate(
                    total=Count('id'),
                    rojos=Count('id', filter=Q(nivel_urgencia='ROJO')),
                    amarillos=Count('id', filter=Q(nivel_urgencia='AMARILLO')),
                )
                
                cache.set('dashboard_stats_basic', stats, timeout=300)
                
            except Exception:
                pass  # Si falla, no es crítico
    
    def _smart_preload(self, request):
        """Pre-cargar datos que probablemente se necesiten."""
        # Si alguien accede al dashboard, pre-cargar lista de pacientes
        if request.path == '/triage/' and request.method == 'GET':
            if not cache.get('patients_waiting'):
                try:
                    from apps.patients.models import Paciente
                    # Pre-cargar en background (no bloquear response)
                    import threading
                    
                    def preload():
                        patients = list(Paciente.objects.activos_en_espera()[:10])
                        cache.set('patients_preload', patients, timeout=60)
                    
                    thread = threading.Thread(target=preload)
                    thread.daemon = True
                    thread.start()
                    
                except Exception:
                    pass  # Si falla, no es crítico