from django.apps import AppConfig


class TriageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.triage'
    verbose_name = 'Sistema de Triage'
    
    def ready(self):
        """Configuración automática al iniciar la aplicación."""
        # Importar signals para activar optimización automática
        from . import signals
        
        # Iniciar mantenimiento automático en background
        signals.start_auto_maintenance()
