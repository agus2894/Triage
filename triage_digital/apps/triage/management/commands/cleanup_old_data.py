"""
Comando para limpieza automática de datos antiguos del sistema de triage.
Ejecutar: python manage.py cleanup_old_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from apps.patients.models import Paciente
from apps.triage.models import SignosVitales


class Command(BaseCommand):
    help = 'Limpia datos antiguos para mantener el rendimiento del sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Días de antigüedad para considerar datos como viejos (default: 365)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la limpieza sin realizar cambios',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        self.stdout.write(f'🧹 Iniciando limpieza de datos antiguos (>{days} días)')
        
        if dry_run:
            self.stdout.write('🔍 MODO SIMULACIÓN - No se realizarán cambios')
        
        # Fecha límite
        fecha_limite = timezone.now() - timedelta(days=days)
        
        with transaction.atomic():
            # 1. Pacientes atendidos antiguos
            self._limpiar_pacientes_antiguos(fecha_limite, dry_run)
            
            # 2. Signos vitales antiguos
            self._limpiar_signos_antiguos(fecha_limite, dry_run)
            
            # 3. Optimizar base de datos después de limpieza
            if not dry_run:
                self._optimizar_post_limpieza()
        
        self.stdout.write(self.style.SUCCESS('✅ Limpieza completada'))

    def _limpiar_pacientes_antiguos(self, fecha_limite, dry_run):
        """Limpia pacientes atendidos que son muy antiguos."""
        self.stdout.write('\n👥 Analizando pacientes antiguos...')
        
        # Solo pacientes ya atendidos y muy antiguos
        pacientes_antiguos = Paciente.objects.filter(
            estado_atencion='ATENDIDO',
            fecha_atencion__lt=fecha_limite
        )
        
        count = pacientes_antiguos.count()
        self.stdout.write(f'Encontrados {count} pacientes antiguos atendidos')
        
        if count > 0:
            if dry_run:
                self.stdout.write(f'[SIMULACIÓN] Se eliminarían {count} pacientes')
            else:
                # Eliminar en lotes para evitar problemas de memoria
                deleted_count = 0
                batch_size = 100
                
                while True:
                    batch = list(pacientes_antiguos[:batch_size])
                    if not batch:
                        break
                        
                    for paciente in batch:
                        paciente.delete()
                        deleted_count += 1
                        
                    if deleted_count % 100 == 0:
                        self.stdout.write(f'Eliminados {deleted_count} pacientes...')
                
                self.stdout.write(f'✅ Eliminados {deleted_count} pacientes antiguos')

    def _limpiar_signos_antiguos(self, fecha_limite, dry_run):
        """Limpia signos vitales muy antiguos."""
        self.stdout.write('\n📊 Analizando signos vitales antiguos...')
        
        signos_antiguos = SignosVitales.objects.filter(
            fecha_hora__lt=fecha_limite,
            paciente__estado_atencion='ATENDIDO'  # Solo de pacientes ya atendidos
        )
        
        count = signos_antiguos.count()
        self.stdout.write(f'Encontrados {count} signos vitales antiguos')
        
        if count > 0:
            if dry_run:
                self.stdout.write(f'[SIMULACIÓN] Se eliminarían {count} signos vitales')
            else:
                deleted_count = signos_antiguos.delete()[0]
                self.stdout.write(f'✅ Eliminados {deleted_count} signos vitales antiguos')

    def _optimizar_post_limpieza(self):
        """Optimiza la base de datos después de la limpieza."""
        self.stdout.write('\n⚡ Optimizando base de datos post-limpieza...')
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            # Vacuum completo después de eliminar datos
            cursor.execute('VACUUM;')
            
            # Re-analizar estadísticas
            cursor.execute('ANALYZE;')
            
            # Verificar integridad
            cursor.execute('PRAGMA integrity_check;')
            result = cursor.fetchone()
            
            if result[0] == 'ok':
                self.stdout.write('✅ Base de datos optimizada correctamente')
            else:
                self.stdout.write(f'⚠️ Advertencia en integridad: {result[0]}')