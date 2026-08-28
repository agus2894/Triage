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
        ).select_related(
            'profesional_atencion__user'
        ).prefetch_related(
            'signos_vitales__profesional__user'
        ).only(
            'id', 'nombre', 'apellido', 'dni', 'edad', 'motivo_consulta',
            'fecha_ingreso', 'estado_atencion', 'fecha_atencion', 'activo',
            'profesional_atencion__user__first_name', 'profesional_atencion__user__last_name'
        ).order_by('-fecha_ingreso')
    
    def criticos_sin_atender(self):
        """Pacientes críticos que necesitan atención inmediata."""
        return self.filter(
            activo=True,
            estado_atencion__in=['ESPERANDO', 'EN_ATENCION'],
            signos_vitales__nivel_urgencia__in=['ROJO', 'AMARILLO']
        ).select_related(
            'profesional_atencion__user'
        ).prefetch_related(
            'signos_vitales__profesional__user'
        ).distinct()
    
    def estadisticas_diarias(self, fecha=None):
        """Estadísticas optimizadas para un día específico."""
        if fecha is None:
            fecha = timezone.now().date()
        
        return self.filter(
            fecha_ingreso__date=fecha
        ).aggregate(
            total=models.Count('id'),
            atendidos=models.Count('id', filter=models.Q(estado_atencion__in=['PASE_A_SALA', 'ALTA', 'PASE_A_UTI'])),
            en_espera=models.Count('id', filter=models.Q(estado_atencion='ESPERANDO')),
            pase_a_sala=models.Count('id', filter=models.Q(estado_atencion='PASE_A_SALA')),
            altas=models.Count('id', filter=models.Q(estado_atencion='ALTA')),
            pase_a_uti=models.Count('id', filter=models.Q(estado_atencion='PASE_A_UTI')),
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
        ('PASE_A_SALA', '🏥 Pase a Sala'),
        ('ALTA', '✅ Alta'),
        ('PASE_A_UTI', '🚨 Pase a UTI'),
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
    
    profesional_atencion = models.ForeignKey(
        'triage.Profesional',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pacientes_atendidos',
        verbose_name="Profesional que Atendió",
        help_text="Profesional que marcó al paciente como atendido"
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
        if self.estado_atencion in ['PASE_A_SALA', 'ALTA', 'PASE_A_UTI']:
            estado_emojis = {
                'PASE_A_SALA': '🏥 Pase a Sala',
                'ALTA': '✅ Alta',
                'PASE_A_UTI': '🚨 Pase a UTI'
            }
            return estado_emojis.get(self.estado_atencion, "✅ Atendido")
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
        if self.estado_atencion in ['PASE_A_SALA', 'ALTA', 'PASE_A_UTI', 'EN_ATENCION']:
            return 0
        
        # Usar cache si existe
        if not hasattr(self, '_tiempo_delta_cache'):
            self._tiempo_delta_cache = timezone.now() - self.fecha_ingreso
            
        return int(self._tiempo_delta_cache.total_seconds() / 60)
    
    def es_critico(self):
        """Verifica si tiene triage crítico (ROJO/AMARILLO) - OPTIMIZADO."""
        # Usar prefetch si está disponible para evitar consulta adicional
        if hasattr(self, '_prefetched_objects_cache') and 'signos_vitales' in self._prefetched_objects_cache:
            signos = list(self.signos_vitales.all())
            if signos:
                ultimo_triage = signos[0]
            else:
                return False
        elif hasattr(self, '_ultimo_triage_cache'):
            ultimo_triage = self._ultimo_triage_cache
        else:
            ultimo_triage = self.signos_vitales.only('nivel_urgencia').first()
            self._ultimo_triage_cache = ultimo_triage
            
        if ultimo_triage and ultimo_triage.nivel_urgencia:
            return ultimo_triage.nivel_urgencia in ['ROJO', 'AMARILLO']
        return False
    
    def obtener_ultimo_triage(self):
        """
        Obtiene el último triage del paciente de forma optimizada.
        Usa cache si está disponible para evitar queries repetidas.
        
        Returns:
            SignosVitales o None
        """
        # Usar prefetch si está disponible
        if hasattr(self, '_prefetched_objects_cache') and 'signos_vitales' in self._prefetched_objects_cache:
            signos = list(self.signos_vitales.all())
            return signos[0] if signos else None
        
        # Usar cache interno si existe
        if hasattr(self, '_ultimo_triage_cache'):
            return self._ultimo_triage_cache
        
        # Query optimizada con only()
        ultimo_triage = self.signos_vitales.select_related('profesional__user').only(
            'id', 'nivel_urgencia', 'news_score', 'fecha_hora',
            'frecuencia_respiratoria', 'saturacion_oxigeno', 
            'tension_sistolica', 'frecuencia_cardiaca',
            'nivel_conciencia', 'temperatura',
            'profesional__user__first_name', 'profesional__user__last_name'
        ).first()
        
        self._ultimo_triage_cache = ultimo_triage
        return ultimo_triage
    
    def marcar_atendido(self, destino='ALTA', profesional=None):
        """
        Marca el paciente con destino o estado específico.
        Usa update() para optimizar la escritura en BD.
        
        Args:
            destino: Estado del paciente ('ALTA', 'PASE_A_SALA', etc.)
            profesional: Profesional que realiza la acción
        """
        destinos_validos = ['ESPERANDO', 'EN_ATENCION', 'PASE_A_SALA', 'ALTA', 'PASE_A_UTI', 'DERIVADO']
        if destino not in destinos_validos:
            destino = 'ALTA'
            
        update_data = {
            'estado_atencion': destino,
        }
        
        ahora = timezone.now()
        if destino != 'ESPERANDO':
            update_data['fecha_atencion'] = ahora
        else:
            update_data['fecha_atencion'] = None
            
        if profesional:
            update_data['profesional_atencion'] = profesional
            
        # Usar update() para una sola query SQL en lugar de save()
        Paciente.objects.filter(id=self.id).update(**update_data)
        
        # Actualizar instancia actual para mantener coherencia
        self.estado_atencion = destino
        self.fecha_atencion = update_data.get('fecha_atencion')
        if profesional:
            self.profesional_atencion = profesional
