"""
Sistema de monitoreo en tiempo real para Triage Digital
Ejecutar: python manage.py monitor_triage
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.triage.models import SignosVitales, TriageResult
from apps.patients.models import Paciente

class Command(BaseCommand):
    help = 'Monitor de estado del sistema de triage en tiempo real'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Horas hacia atrás para el análisis (default: 24)',
        )

    def handle(self, *args, **options):
        hours = options['hours']
        desde = timezone.now() - timedelta(hours=hours)
        
        self.stdout.write(f'📊 MONITOR TRIAGE - Últimas {hours} horas')
        self.stdout.write('=' * 50)
        
        # Estadísticas generales
        total_pacientes = Paciente.objects.filter(fecha_ingreso__gte=desde).count()
        total_evaluaciones = SignosVitales.objects.filter(fecha_hora__gte=desde).count()
        
        self.stdout.write(f'👥 Pacientes ingresados: {total_pacientes}')
        self.stdout.write(f'🩺 Evaluaciones realizadas: {total_evaluaciones}')
        
        # Distribución por urgencia
        urgencias = TriageResult.objects.filter(fecha_calculo__gte=desde)
        rojos = urgencias.filter(nivel_urgencia='ROJO').count()
        amarillos = urgencias.filter(nivel_urgencia='AMARILLO').count()
        verdes = urgencias.filter(nivel_urgencia='VERDE').count()
        azules = urgencias.filter(nivel_urgencia='AZUL').count()
        
        self.stdout.write('\n🚦 Distribución por Urgencia:')
        self.stdout.write(f'  🔴 ROJO (Crítico): {rojos}')
        self.stdout.write(f'  🟡 AMARILLO (Alto): {amarillos}')
        self.stdout.write(f'  🟢 VERDE (Medio): {verdes}')
        self.stdout.write(f'  🔵 AZUL (Bajo): {azules}')
        
        # Casos críticos actuales
        criticos_actuales = TriageResult.objects.filter(
            nivel_urgencia__in=['ROJO', 'AMARILLO'],
            signos_vitales__paciente__activo=True
        ).count()
        
        self.stdout.write(f'\n⚠️  Casos críticos pendientes: {criticos_actuales}')
        
        # Performance
        if total_evaluaciones > 0:
            promedio_por_hora = total_evaluaciones / hours
            self.stdout.write(f'⚡ Promedio evaluaciones/hora: {promedio_por_hora:.1f}')
        
        # Alertas
        if rojos > 0:
            self.stdout.write(f'\n🚨 ALERTA: {rojos} casos ROJOS requieren atención inmediata')
        if criticos_actuales > 10:
            self.stdout.write('🚨 SOBRECARGA: Muchos casos críticos pendientes')
            
        self.stdout.write('\n✅ Monitor completado')