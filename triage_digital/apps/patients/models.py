"""
Modelos para la gestión de pacientes en el sistema de Triage Digital.

Este módulo contiene el modelo Paciente que almacena la información básica
de cada persona que ingresa al sistema de triaje hospitalario.
"""

from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class PacienteManager(models.Manager):
    """Manager optimizado para consultas frecuentes de pacientes."""
    
    def activos_en_espera(self):
        """Pacientes activos en espera con datos pre-cargados."""
        return self.filter(
            activo=True,
            estado_atencion='ESPERANDO'
        ).prefetch_related('signos_vitales').order_by('-fecha_ingreso')
    
    def criticos_sin_atender(self):
        """Pacientes críticos que necesitan atención inmediata."""
        return self.filter(
            activo=True,
            estado_atencion__in=['ESPERANDO', 'EN_ATENCION'],
            signos_vitales__nivel_urgencia__in=['ROJO', 'AMARILLO']
        ).select_related().prefetch_related('signos_vitales').distinct()
    
    def estadisticas_diarias(self, fecha=None):
        """Estadísticas optimizadas para un día específico."""
        if fecha is None:
            fecha = timezone.now().date()
        
        return self.filter(
            fecha_ingreso__date=fecha
        ).aggregate(
            total=models.Count('id'),
            atendidos=models.Count('id', filter=models.Q(estado_atencion='ATENDIDO')),
            en_espera=models.Count('id', filter=models.Q(estado_atencion='ESPERANDO')),
        )


class Paciente(models.Model):
    """
    Modelo para almacenar información básica del paciente.
    
    Según las especificaciones del proyecto, debe almacenar:
    - Nombre y apellido
    - DNI (único)
    - Edad
    - Motivo de consulta
    """
    
    # Validador para DNI argentino (7-8 dígitos)
    dni_validator = RegexValidator(
        regex=r'^\d{7,8}$',
        message='El DNI debe tener entre 7 y 8 dígitos.'
    )
    
    # Datos básicos del paciente (pueden estar vacíos para pacientes inconscientes)
    nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Nombre",
        help_text="Nombre del paciente (opcional para pacientes inconscientes)"
    )
    
    apellido = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Apellido", 
        help_text="Apellido del paciente (opcional para pacientes inconscientes)"
    )
    
    dni = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        validators=[dni_validator],
        verbose_name="DNI",
        help_text="Documento Nacional de Identidad (opcional para pacientes inconscientes)"
    )
    
    edad = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Edad",
        help_text="Edad del paciente en años (opcional para pacientes inconscientes)"
    )
    
    motivo_consulta = models.TextField(
        verbose_name="Motivo de consulta",
        help_text="Descripción del motivo por el cual consulta el paciente"
    )
    
    # Campos de control
    fecha_ingreso = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de ingreso",
        help_text="Fecha y hora en que el paciente ingresó al sistema"
    )
    
    # Estados de atención médica
    ESTADO_CHOICES = [
        ('ESPERANDO', '⏳ Esperando atención'),
        ('EN_ATENCION', '👩‍⚕️ En atención'),
        ('ATENDIDO', '✅ Atendido'),
        ('DERIVADO', '🏥 Derivado'),
    ]
    
    estado_atencion = models.CharField(
        max_length=12,
        choices=ESTADO_CHOICES,
        default='ESPERANDO',
        verbose_name="Estado de Atención",
        help_text="Estado actual del paciente en el proceso de atención"
    )
    
    fecha_atencion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Atención",
        help_text="Momento en que fue atendido el paciente"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el paciente está actualmente en el sistema"
    )
    
    # Manager optimizado
    objects = PacienteManager()

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-fecha_ingreso']  # Más recientes primero
        indexes = [
            # Índice para la consulta más frecuente: pacientes activos en espera
            models.Index(fields=['activo', 'estado_atencion', '-fecha_ingreso'], name='idx_pacientes_activos'),
            # Índice para búsquedas por DNI
            models.Index(fields=['dni'], name='idx_pacientes_dni'),
            # Índice para estadísticas por fecha
            models.Index(fields=['fecha_ingreso'], name='idx_pacientes_fecha'),
            # NUEVO: Índice compuesto optimizado para dashboard
            models.Index(fields=['activo', 'estado_atencion'], name='idx_estado_activo'),
            # NUEVO: Índice para búsquedas por edad en emergencias
            models.Index(fields=['edad'], name='idx_pacientes_edad'),
        ]
        
    def __str__(self):
        if self.nombre and self.apellido:
            return f"{self.apellido}, {self.nombre} (DNI: {self.dni or 'S/N'})"
        elif self.dni:
            return f"Paciente DNI: {self.dni}"
        else:
            return f"Paciente Inconsciente #{self.id}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del paciente o identificación alternativa."""
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido}"
        elif self.nombre:
            return self.nombre
        elif self.apellido:
            return self.apellido
        elif self.dni:
            return f"Paciente DNI: {self.dni}"
        else:
            return f"Paciente Inconsciente #{self.id}"
    
    @property
    def tiempo_espera(self):
        """Tiempo de espera formateado - OPTIMIZADO."""
        if self.estado_atencion == 'ATENDIDO':
            return "✅ Atendido"
        if self.estado_atencion == 'EN_ATENCION':
            return "👩‍⚕️ En atención"
            
        # Cálculo optimizado usando cache interno
        if not hasattr(self, '_tiempo_delta_cache'):
            self._tiempo_delta_cache = timezone.now() - self.fecha_ingreso
        
        delta = self._tiempo_delta_cache
        horas = delta.seconds // 3600
        minutos = (delta.seconds % 3600) // 60
        
        if delta.days > 0:
            return f"{delta.days}d {horas}h"
        elif horas > 0:
            return f"{horas}h {minutos}m"
        else:
            return f"{minutos}m"

    @property
    def tiempo_espera_minutos(self):
        """Tiempo de espera en minutos para cálculos - OPTIMIZADO."""
        if self.estado_atencion in ['ATENDIDO', 'EN_ATENCION']:
            return 0
        
        # Usar cache si existe
        if not hasattr(self, '_tiempo_delta_cache'):
            self._tiempo_delta_cache = timezone.now() - self.fecha_ingreso
            
        return int(self._tiempo_delta_cache.total_seconds() / 60)
    
    def es_critico(self):
        """Verifica si tiene triage crítico (ROJO/AMARILLO) - OPTIMIZADO."""
        # Usar select_related para evitar consulta adicional
        if hasattr(self, '_ultimo_triage_cache'):
            ultimo_triage = self._ultimo_triage_cache
        else:
            ultimo_triage = self.signos_vitales.select_related().first()
            self._ultimo_triage_cache = ultimo_triage
            
        if ultimo_triage and ultimo_triage.nivel_urgencia:
            return ultimo_triage.nivel_urgencia in ['ROJO', 'AMARILLO']
        return False
    
    def marcar_atendido(self):
        """Marca el paciente como atendido y actualiza fecha - OPTIMIZADO."""
        # Usar update() para ser más eficiente que save()
        Paciente.objects.filter(id=self.id).update(
            estado_atencion='ATENDIDO',
            fecha_atencion=timezone.now()
        )
        # Actualizar instancia actual
        self.estado_atencion = 'ATENDIDO'
        self.fecha_atencion = timezone.now()
