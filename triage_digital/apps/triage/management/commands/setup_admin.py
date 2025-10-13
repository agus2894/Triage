"""
Comando para crear/resetear el admin único del sistema.
Ejecutar: python manage.py setup_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.triage.models import Profesional

class Command(BaseCommand):
    help = 'Crea o resetea el admin único del sistema (admin/123456)'

    def handle(self, *args, **options):
        self.stdout.write('🏥 CONFIGURANDO ADMIN ÚNICO')
        self.stdout.write('=' * 30)
        
        # Verificar si ya existe el admin
        try:
            admin = User.objects.get(username='admin')
            self.stdout.write('⚠️  Admin existente - Actualizando credenciales')
            admin.set_password('123456')
            admin.email = 'admin@hospital.com'
            admin.first_name = 'Administrador'
            admin.last_name = 'Sistema'
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
        except User.DoesNotExist:
            # Crear el admin único
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@hospital.com',
                password='123456',
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write('✅ Admin creado')

        # Verificar/crear perfil de profesional
        try:
            profesional = admin.profesional
            self.stdout.write('⚠️  Perfil profesional ya existe')
        except Profesional.DoesNotExist:
            profesional = Profesional.objects.create(
                user=admin,
                dni='00000000',
                tipo='medico',
                matricula='ADMIN-001',
                activo=True
            )
            self.stdout.write('✅ Perfil profesional creado')

        self.stdout.write('')
        self.stdout.write('🎯 CREDENCIALES ÚNICAS:')
        self.stdout.write('=====================')
        self.stdout.write('📊 Admin: admin / 123456')
        self.stdout.write('🏥 Triage: DNI 00000000 / 123456')
        self.stdout.write('')
        self.stdout.write('✅ Sistema listo para usar')