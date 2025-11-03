"""
Comando para actualizar roles de profesionales existentes al nuevo sistema.
Convierte usuarios existentes a roles diferenciados.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.triage.models import Profesional


class Command(BaseCommand):
    help = '🔒 Actualiza roles de profesionales al nuevo sistema de permisos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Asignar roles automáticamente basado en nombres de usuario',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔒 ACTUALIZANDO SISTEMA DE ROLES...')
        )
        
        # Contar profesionales por tipo actual
        total_profesionales = Profesional.objects.count()
        
        if total_profesionales == 0:
            self.stdout.write(
                self.style.WARNING('⚠️  No hay profesionales en el sistema.')
            )
            return
        
        if options['auto']:
            self._asignar_roles_automatico()
        else:
            self._asignar_roles_interactivo()
            
        self.stdout.write(
            self.style.SUCCESS('✅ Roles actualizados correctamente')
        )

    def _asignar_roles_automatico(self):
        """Asigna roles automáticamente basado en nombres de usuario."""
        
        for profesional in Profesional.objects.all():
            username = profesional.user.username.lower()
            
            # Detectar administradores
            if any(word in username for word in ['admin', 'administrador', 'jefe', 'director']):
                profesional.tipo = 'administrador'
                self.stdout.write(f'👤 {profesional.user.username} → ADMINISTRADOR')
                
            # Detectar médicos
            elif any(word in username for word in ['medico', 'doctor', 'dr']):
                profesional.tipo = 'medico'
                self.stdout.write(f'👨‍⚕️ {profesional.user.username} → MÉDICO')
                
            # Por defecto: enfermero
            else:
                profesional.tipo = 'enfermero'
                self.stdout.write(f'👩‍⚕️ {profesional.user.username} → ENFERMERO')
            
            profesional.save()

    def _asignar_roles_interactivo(self):
        """Permite asignar roles manualmente para cada profesional."""
        
        self.stdout.write('\n🔒 ASIGNACIÓN INTERACTIVA DE ROLES\n')
        
        roles_choices = {
            '1': ('enfermero', '👩‍⚕️ Enfermero Triajero'),
            '2': ('medico', '👨‍⚕️ Médico'),
            '3': ('administrador', '🔧 Administrador'),
        }
        
        for profesional in Profesional.objects.all():
            self.stdout.write(f'\n📋 Profesional: {profesional.user.get_full_name()} ({profesional.user.username})')
            self.stdout.write(f'   DNI: {profesional.dni}')
            self.stdout.write(f'   Tipo actual: {profesional.get_tipo_display()}')
            
            self.stdout.write('\nSeleccione nuevo rol:')
            for key, (value, display) in roles_choices.items():
                self.stdout.write(f'  {key}. {display}')
            
            while True:
                choice = input('\nOpción (1-3, Enter para mantener actual): ').strip()
                
                if choice == '':
                    self.stdout.write(f'✅ Manteniendo rol actual: {profesional.get_tipo_display()}')
                    break
                elif choice in roles_choices:
                    nuevo_tipo, display = roles_choices[choice]
                    profesional.tipo = nuevo_tipo
                    profesional.save()
                    self.stdout.write(f'✅ Rol actualizado: {display}')
                    break
                else:
                    self.stdout.write('❌ Opción inválida. Intente nuevamente.')