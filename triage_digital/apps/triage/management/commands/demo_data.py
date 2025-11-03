"""
Comando para generar datos de demostración.
Crea pacientes ficticios para mostrar el sistema funcionando.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from apps.patients.models import Paciente
from apps.triage.models import SignosVitales, Profesional
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Genera datos de demostración para el sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina todos los pacientes existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        self.stdout.write('🎯 GENERANDO DATOS DE DEMO')
        self.stdout.write('==========================')
        
        # Eliminar datos existentes si se solicita
        if options['reset']:
            SignosVitales.objects.all().delete()
            Paciente.objects.all().delete()
            self.stdout.write('🗑️  Datos anteriores eliminados')

        # Obtener profesional admin
        try:
            admin_user = User.objects.get(username='admin')
            profesional = admin_user.profesional
        except:
            self.stdout.write(self.style.ERROR('❌ Error: Usuario admin no encontrado'))
            return

        # Datos ficticios realistas
        pacientes_demo = [
            {
                'nombre': 'María Elena', 'apellido': 'García López', 'dni': '20345678', 
                'edad': 65, 'sexo': 'F', 'motivo': 'Dolor torácico intenso',
                'signos': {'fr': 24, 'sat': 88, 'tas': 160, 'fc': 110, 'temp': 37.2, 'conciencia': 'A'}
            },
            {
                'nombre': 'Carlos', 'apellido': 'Rodríguez', 'dni': '30123456', 
                'edad': 45, 'sexo': 'M', 'motivo': 'Dificultad respiratoria',
                'signos': {'fr': 28, 'sat': 90, 'tas': 140, 'fc': 95, 'temp': 38.1, 'conciencia': 'A'}
            },
            {
                'nombre': 'Ana', 'apellido': 'Martínez', 'dni': '25987654', 
                'edad': 28, 'sexo': 'F', 'motivo': 'Cefalea severa',
                'signos': {'fr': 18, 'sat': 98, 'tas': 120, 'fc': 80, 'temp': 36.8, 'conciencia': 'A'}
            },
            {
                'nombre': 'Roberto', 'apellido': 'Fernández', 'dni': '40567890', 
                'edad': 72, 'sexo': 'M', 'motivo': 'Mareos y confusión',
                'signos': {'fr': 22, 'sat': 92, 'tas': 90, 'fc': 120, 'temp': 37.8, 'conciencia': 'V'}
            },
            {
                'nombre': 'Sofía', 'apellido': 'López', 'dni': '35246810', 
                'edad': 19, 'sexo': 'F', 'motivo': 'Dolor abdominal',
                'signos': {'fr': 16, 'sat': 99, 'tas': 110, 'fc': 75, 'temp': 36.5, 'conciencia': 'A'}
            }
        ]

        created_count = 0
        for p_data in pacientes_demo:
            # Crear paciente
            paciente = Paciente.objects.create(
                nombre=p_data['nombre'],
                apellido=p_data['apellido'],
                dni=p_data['dni'],
                edad=p_data['edad'],
                motivo_consulta=p_data['motivo']
            )

            # Crear signos vitales con tiempo aleatorio en las últimas 2 horas
            tiempo_random = timezone.now() - timedelta(minutes=random.randint(5, 120))
            
            SignosVitales.objects.create(
                paciente=paciente,
                profesional=profesional,
                frecuencia_respiratoria=p_data['signos']['fr'],
                saturacion_oxigeno=p_data['signos']['sat'],
                tension_sistolica=p_data['signos']['tas'],
                frecuencia_cardiaca=p_data['signos']['fc'],
                temperatura=p_data['signos']['temp'],
                nivel_conciencia=p_data['signos']['conciencia'],
                fecha_hora=tiempo_random
            )
            
            created_count += 1
            self.stdout.write(f'✅ {paciente.nombre} {paciente.apellido} - NEWS: {SignosVitales.objects.filter(paciente=paciente).first().news_score}')

        self.stdout.write('')
        self.stdout.write(f'🎉 {created_count} pacientes de demo creados')
        self.stdout.write('📊 Dashboard con datos realistas listo')
        self.stdout.write('')
        self.stdout.write('🎯 URL: http://127.0.0.1:8000')
        self.stdout.write('🔑 Login: DNI 00000000 / 123456')
