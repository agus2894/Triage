from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Paciente.
    """
    list_display = ('apellido', 'nombre', 'dni', 'edad', 'fecha_ingreso', 'activo')
    list_filter = ('activo', 'fecha_ingreso', 'edad')
    search_fields = ('nombre', 'apellido', 'dni')
    readonly_fields = ('fecha_ingreso', 'tiempo_espera')
    list_per_page = 20
    
    fieldsets = (
        ('Datos Básicos', {
            'fields': ('nombre', 'apellido', 'dni', 'edad')
        }),
        ('Consulta', {
            'fields': ('motivo_consulta',)
        }),
        ('Control', {
            'fields': ('activo', 'fecha_ingreso', 'tiempo_espera'),
            'classes': ('collapse',)
        }),
    )
