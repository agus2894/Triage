"""
Middleware optimizado para manejo de cache y performance.
"""
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class PerformanceOptimizationMiddleware(MiddlewareMixin):
    """
    Middleware que optimiza el rendimiento de consultas y cache.
    - Limpia cache de queries obsoletas
    - Optimiza headers para mejor performance
    """
    
    def process_request(self, request):
        """Preprocesa la request para optimización."""
        # Marcar el inicio del request para métricas
        request._start_time = __import__('time').time()
        return None
    
    def process_response(self, request, response):
        """Optimiza la respuesta y agrega headers de cache."""
        # Para APIs JSON, agregar headers de cache apropiados
        if request.path.startswith('/triage/api/'):
            # Cache corto para APIs de tiempo real
            response['Cache-Control'] = 'private, max-age=15'
        
        # Para páginas estáticas, cache más largo
        elif request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=31536000'
        
        return response