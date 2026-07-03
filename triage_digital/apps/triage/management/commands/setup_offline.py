"""
🏥 COMANDO SETUP_OFFLINE
========================
Configura la base de datos SQLite offline con datos de demostración.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from apps.triage.models import Profesional
from apps.patients.models import Paciente


class Command(BaseCommand):
    help = 'Configura la base de datos offline con usuarios de demostración'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-migrations',
            action='store_true',
            help='Omitir ejecución de migraciones',
        )

    def handle(self, *args, **options):
        self.stdout.write("🏥 Configurando base de datos OFFLINE...")
        self.stdout.write("=" * 50)

        # 1. Ejecutar migraciones
        if not options['skip_migrations']:
            self.stdout.write("📋 Ejecutando migraciones...")
            from django.core.management import call_command
            try:
                call_command('migrate', verbosity=0, interactive=False)
                self.stdout.write(self.style.SUCCESS("   ✅ Migraciones completadas"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Error en migraciones: {e}"))
                return

        # 2. Crear usuarios de demostración
        self.stdout.write("\n👥 Creando usuarios de demostración...")
        
        try:
            with transaction.atomic():
                # Usuario 1: Admin general (superusuario)
                if not User.objects.filter(username='admin').exists():
                    admin_user = User.objects.create_superuser(
                        username='admin',
                        password='admin',
                        email='admin@hospital.com',
                        first_name='Administrador',
                        last_name='Sistema'
                    )
                    self.stdout.write(self.style.SUCCESS(
                        "   ✅ Admin creado - Usuario: admin | Contraseña: admin"
                    ))
                else:
                    self.stdout.write(self.style.WARNING("   ⚠️  Usuario 'admin' ya existe"))

                # Usuario 2: Profesional con DNI 38046539
                if not User.objects.filter(username='38046539').exists():
                    prof_user = User.objects.create_user(
                        username='38046539',
                        password='38046539',
                        email='38046539@hospital.com',
                        first_name='Agustín',
                        last_name='Demo'
                    )
                    
                    # Crear perfil profesional asociado
                    if not Profesional.objects.filter(dni='38046539').exists():
                        Profesional.objects.create(
                            user=prof_user,
                            dni='38046539',
                            tipo='enfermero',
                            matricula='ENF-38046539',
                            activo=True
                        )
                    
                    self.stdout.write(self.style.SUCCESS(
                        "   ✅ Profesional creado - DNI: 38046539 | Contraseña: 38046539"
                    ))
                else:
                    self.stdout.write(self.style.WARNING("   ⚠️  Usuario DNI '38046539' ya existe"))

                # Usuario 3: Otro profesional de ejemplo
                if not User.objects.filter(username='12345678').exists():
                    otro_user = User.objects.create_user(
                        username='12345678',
                        password='12345678',
                        email='12345678@hospital.com',
                        first_name='Juan',
                        last_name='Pérez'
                    )
                    
                    if not Profesional.objects.filter(dni='12345678').exists():
                        Profesional.objects.create(
                            user=otro_user,
                            dni='12345678',
                            tipo='medico',
                            matricula='MED-12345678',
                            activo=True
                        )
                    
                    self.stdout.write(self.style.SUCCESS(
                        "   ✅ Médico demo creado - DNI: 12345678 | Contraseña: 12345678"
                    ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error creando usuarios: {e}"))
            return

        # 3. Crear pacientes de demostración
        self.stdout.write("\n🏥 Creando pacientes de demostración...")
        
        try:
            with transaction.atomic():
                pacientes_demo = [
                    {
                        'nombre': 'María',
                        'apellido': 'González',
                        'dni': '20345678',
                        'edad': 45,
                        'motivo_consulta': 'Dolor abdominal intenso',
                        'estado_atencion': 'ESPERANDO'
                    },
                    {
                        'nombre': 'Carlos',
                        'apellido': 'Rodríguez',
                        'dni': '35678901',
                        'edad': 28,
                        'motivo_consulta': 'Fiebre alta y dolor de cabeza',
                        'estado_atencion': 'ESPERANDO'
                    },
                    {
                        'nombre': 'Ana',
                        'apellido': 'Martínez',
                        'dni': '42123456',
                        'edad': 62,
                        'motivo_consulta': 'Dolor de pecho',
                        'estado_atencion': 'ESPERANDO'
                    }
                ]

                created_count = 0
                for paciente_data in pacientes_demo:
                    if not Paciente.objects.filter(dni=paciente_data['dni']).exists():
                        Paciente.objects.create(**paciente_data)
                        created_count += 1

                if created_count > 0:
                    self.stdout.write(self.style.SUCCESS(
                        f"   ✅ {created_count} pacientes de demostración creados"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        "   ⚠️  Los pacientes demo ya existen"
                    ))

        except Exception as e:
            self.stdout.write(self.style.WARNING(
                f"   ⚠️  Error creando pacientes demo: {e}"
            ))

        # 4. Resumen final
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("✅ Base de datos OFFLINE configurada\n"))
        self.stdout.write("🔑 CREDENCIALES DE ACCESO:")
        self.stdout.write("   • Admin:        usuario: admin     | contraseña: admin")
        self.stdout.write("   • Tu usuario:   DNI: 38046539      | contraseña: 38046539")
        self.stdout.write("   • Demo médico:  DNI: 12345678      | contraseña: 12345678")
        self.stdout.write("\n💡 Usa cualquiera de estos usuarios para acceder al sistema")
        self.stdout.write("=" * 50)
