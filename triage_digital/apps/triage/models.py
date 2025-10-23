"""Modelos para Triage Digital y cálculo NEWS Score."""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.patients.models import Paciente


class Profesional(models.Model):
    """Profesional médico (médico o enfermero) autorizado para usar el sistema."""
    
    TIPO_CHOICES = [
        ('medico', 'Médico'),
        ('enfermero', 'Enfermero'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario"
    )
    
    dni = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="DNI",
        help_text="Documento Nacional de Identidad (sin puntos)"
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Profesional"
    )
    
    matricula = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Matrícula Profesional",
        help_text="Número de matrícula profesional"
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si el profesional puede acceder al sistema"
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    
    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"
        ordering = ['user__last_name', 'user__first_name']
        indexes = [
            models.Index(fields=['dni'], name='idx_profesional_dni'),
            models.Index(fields=['activo', 'tipo'], name='idx_profesional_activo_tipo'),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - DNI: {self.dni} ({self.get_tipo_display()})"


class SignosVitales(models.Model):
    """Signos vitales para cálculo NEWS Score (6 parámetros) + Resultado de Triage."""
    
    # Escala AVPU para nivel de conciencia
    CONCIENCIA_CHOICES = [
        ('A', 'Alerta y orientado'),
        ('V', 'Responde a estímulos verbales'), 
        ('P', 'Responde solo a estímulos dolorosos'),
        ('U', 'No responde (inconsciente)')
    ]
    
    # Niveles de urgencia según NEWS Score (Sistema Argentino)
    NIVEL_URGENCIA_CHOICES = [
        ('VERDE', 'Verde - Sin riesgo vital (atención dentro de 60 minutos)'),
        ('AMARILLO', 'Amarillo - Riesgo moderado (atención dentro de 30 minutos)'),
        ('ROJO', 'Rojo - Riesgo vital inmediato (atención inmediata)'),
    ]
    
    COLOR_CODES = {
        'VERDE': '#28a745',
        'AMARILLO': '#ffc107', 
        'ROJO': '#dc3545'
    }
    
    # Relaciones
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='signos_vitales',
        verbose_name="Paciente"
    )
    
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name='signos_registrados',
        verbose_name="Profesional que registra"
    )
    
    # Fecha y hora del registro
    fecha_hora = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha y hora del registro"
    )
    
    # Parámetros vitales del NEWS Score
    frecuencia_respiratoria = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(60)],
        verbose_name="Frecuencia Respiratoria",
        help_text="Respiraciones por minuto (1-60)"
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(100)],
        verbose_name="Saturación de Oxígeno",
        help_text="Porcentaje de saturación de O2 (50-100%)"
    )
    
    tension_sistolica = models.PositiveIntegerField(
        validators=[MinValueValidator(50), MaxValueValidator(300)],
        verbose_name="Tensión Arterial Sistólica",
        help_text="Tensión sistólica en mmHg (50-300)"
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(200)],
        verbose_name="Frecuencia Cardíaca",
        help_text="Latidos por minuto (20-200)"
    )
    
    nivel_conciencia = models.CharField(
        max_length=1,
        choices=CONCIENCIA_CHOICES,
        verbose_name="Nivel de Conciencia",
        help_text="Escala AVPU"
    )
    
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(30.0), MaxValueValidator(45.0)],
        verbose_name="Temperatura Corporal",
        help_text="Temperatura en grados Celsius (30.0-45.0)"
    )
    
    # Resultado del triage (campos consolidados)
    news_score = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Puntaje NEWS",
        help_text="Puntaje calculado del National Early Warning Score"
    )
    
    nivel_urgencia = models.CharField(
        max_length=8,
        choices=NIVEL_URGENCIA_CHOICES,
        null=True, blank=True,
        verbose_name="Nivel de Urgencia"
    )
    
    tiempo_atencion_max = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Tiempo máximo de atención",
        help_text="Tiempo máximo de espera en minutos"
    )
    
    class Meta:
        verbose_name = "Signos Vitales"
        verbose_name_plural = "Signos Vitales"
        ordering = ['-fecha_hora']
        # Índices optimizados para consultas médicas críticas
        indexes = [
            models.Index(fields=['-fecha_hora'], name='idx_signos_fecha'),
            models.Index(fields=['paciente', '-fecha_hora'], name='idx_paciente_fecha'),
            models.Index(fields=['profesional', '-fecha_hora'], name='idx_profesional_fecha'),
            models.Index(fields=['nivel_urgencia', '-fecha_hora'], name='idx_urgencia_fecha'),
        ]
        
    def __str__(self):
        return f"Signos vitales - {self.paciente.nombre_completo} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
    
    @property
    def color_hex(self):
        """Retorna el código de color hexadecimal para el nivel de urgencia."""
        return self.COLOR_CODES.get(self.nivel_urgencia, '#6c757d')
    
    def calcular_puntaje_news(self):
        """
        Calcula el puntaje NEWS basado en los signos vitales.
        
        Returns:
            dict: Resultado del cálculo NEWS
        """
        from .utils import CalculadoraNEWS  # Import lazy para evitar circular imports
        
        datos_signos_vitales = {
            'frecuencia_respiratoria': self.frecuencia_respiratoria,
            'saturacion_oxigeno': self.saturacion_oxigeno,
            'tension_sistolica': self.tension_sistolica,
            'frecuencia_cardiaca': self.frecuencia_cardiaca,
            'nivel_conciencia': self.nivel_conciencia,
            'temperatura': self.temperatura,
        }
        
        return CalculadoraNEWS.calcular_puntaje_total(datos_signos_vitales)
    
    def save(self, *args, **kwargs):
        """
        OPTIMIZADO: Cálculo crítico de triage médico.
        Minimiza consultas DB para velocidad en emergencias.
        """
        # Cálculo optimizado del triage
        resultado_news = self.calcular_puntaje_news()
        
        # Asignar valores calculados
        self.news_score = resultado_news['puntaje_total']
        self.nivel_urgencia = resultado_news['clasificacion']
        self.tiempo_atencion_max = resultado_news['tiempo_atencion_maximo']
        
        # Guardar con triage calculado
        super().save(*args, **kwargs)
