from django.contrib import admin
from .models import NotaEvolucion


@admin.register(NotaEvolucion)
class NotaEvolucionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo NotaEvolucion.
    """
    list_display = ('paciente', 'resumen_nota', 'importante', 'fecha_hora', 'profesional')
    list_filter = ('importante', 'fecha_hora', 'profesional')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'paciente__dni', 'nota')
    readonly_fields = ('fecha_hora',)
    list_per_page = 20
    
    fieldsets = (
        ('Paciente y Profesional', {
            'fields': ('paciente', 'profesional', 'fecha_hora')
        }),
        ('Nota', {
            'fields': ('nota', 'importante')
        }),
    )
