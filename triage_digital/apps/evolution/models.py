"""
Modelos para el seguimiento y evolución de pacientes.

Este módulo permite al personal médico registrar notas de evolución
para mantener un historial del estado del paciente.
"""

from django.db import models
from django.utils import timezone
from apps.patients.models import Paciente


class NotaEvolucion(models.Model):
    """
    Modelo para registrar notas de evolución del paciente.
    
    Permite al personal de salud documentar cambios en el estado
    del paciente durante su estancia en la guardia.
    """
    
    # Relación con el paciente
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='notas_evolucion',
        verbose_name="Paciente"
    )
    
    # Contenido de la nota
    nota = models.TextField(
        verbose_name="Nota de evolución",
        help_text="Descripción del estado actual o cambios observados en el paciente"
    )
    
    # Campos de control
    fecha_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha y Hora",
        help_text="Momento en que se registró la nota"
    )
    
    profesional = models.ForeignKey(
        'auth.User',  # Usuario Django estándar
        on_delete=models.PROTECT,
        verbose_name="Profesional",
        help_text="Profesional médico (médico/enfermero) que registró la nota de evolución"
    )
    
    # Campo para marcar si es importante
    importante = models.BooleanField(
        default=False,
        verbose_name="Nota importante",
        help_text="Marcar si la nota requiere atención especial"
    )
    
    class Meta:
        verbose_name = "Nota de Evolución"
        verbose_name_plural = "Notas de Evolución"
        ordering = ['-fecha_hora']
        
    def __str__(self):
        return f"Nota - {self.paciente.nombre_completo} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
    
    @property
    def resumen_nota(self):
        """Retorna un resumen de la nota (primeros 50 caracteres)."""
        return self.nota[:50] + '...' if len(self.nota) > 50 else self.nota
