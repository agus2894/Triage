import osimport osimport os

from django.core.management.base import BaseCommand

from django.db import connectionfrom django.core.management.base import BaseCommandfrom django.core.management.base import BaseCommand

from django.conf import settings

from apps.patients.models import Pacientefrom django.db import connectionfrom django.db import connection

from apps.triage.models import SignosVitales

from django.conf import settingsfrom django.conf import settings



class Command(BaseCommand):from apps.patients.models import Pacientefrom apps.patients.models import Paciente

    help = 'Análisis básico del sistema'

from apps.triage.models import SignosVitalesfrom apps.triage.models import SignosVitales

    def handle(self, *args, **options):

        self.stdout.write('🔍 Análisis del sistema...\n')

        

        # Base de datos

        with connection.cursor() as cursor:

            cursor.execute("SELECT sqlite_version();")class Command(BaseCommand):class Command(BaseCommand):

            version = cursor.fetchone()[0]

            self.stdout.write(f'SQLite: {version}')    help = 'Análisis básico del sistema'    help = 'Análisis básico del sistema'

            

            db_path = settings.DATABASES['default']['NAME']

            if os.path.exists(db_path):

                size_mb = os.path.getsize(db_path) / (1024 * 1024)    def handle(self, *args, **options):    def handle(self, *args, **options):

                self.stdout.write(f'BD: {size_mb:.1f} MB')

                self.stdout.write('🔍 Análisis del sistema...\n')        self.stdout.write('🔍 Análisis del sistema...\n')

        # Datos

        pacientes = Paciente.objects.count()                

        signos = SignosVitales.objects.count()

        self.stdout.write(f'Pacientes: {pacientes}')        # Base de datos        # Base de datos

        self.stdout.write(f'Signos vitales: {signos}')

                with connection.cursor() as cursor:        with connection.cursor() as cursor:

        self.stdout.write('\n✅ Análisis completado')
            cursor.execute("SELECT sqlite_version();")            cursor.execute("SELECT sqlite_version();")

            version = cursor.fetchone()[0]            version = cursor.fetchone()[0]

            self.stdout.write(f'SQLite: {version}')            self.stdout.write(f'SQLite: {version}')

                        

            db_path = settings.DATABASES['default']['NAME']            db_path = settings.DATABASES['default']['NAME']

            if os.path.exists(db_path):            if os.path.exists(db_path):

                size_mb = os.path.getsize(db_path) / (1024 * 1024)                size_mb = os.path.getsize(db_path) / (1024 * 1024)

                self.stdout.write(f'BD: {size_mb:.1f} MB')                self.stdout.write(f'BD: {size_mb:.1f} MB')

                

        # Datos        # Datos

        pacientes = Paciente.objects.count()        pacientes = Paciente.objects.count()

        signos = SignosVitales.objects.count()        signos = SignosVitales.objects.count()

        self.stdout.write(f'Pacientes: {pacientes}')        self.stdout.write(f'Pacientes: {pacientes}')

        self.stdout.write(f'Signos vitales: {signos}')        self.stdout.write(f'Signos vitales: {signos}')

                

        self.stdout.write('\n✅ Análisis completado')        self.stdout.write('\n✅ Análisis completado')
        
        with connection.cursor() as cursor:
            # Información de SQLite
            cursor.execute("SELECT sqlite_version();")
            version = cursor.fetchone()[0]
            self.stdout.write(f'SQLite versión: {version}')
            
            # Tamaño de la base de datos
            db_path = settings.DATABASES['default']['NAME']
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                size_mb = size_bytes / (1024 * 1024)
                self.stdout.write(f'Tamaño BD: {size_mb:.2f} MB')
            
            # Configuraciones críticas
            pragmas = [
                'journal_mode', 'synchronous', 'cache_size', 
                'temp_store', 'mmap_size', 'foreign_keys'
            ]
            
            for pragma in pragmas:
                cursor.execute(f'PRAGMA {pragma};')
                result = cursor.fetchone()
                self.stdout.write(f'{pragma}: {result[0] if result else "N/A"}')
            
            # Conteos de registros
            pacientes = Paciente.objects.count()
            signos = SignosVitales.objects.count()
            profesionales = Profesional.objects.count()
            
            self.stdout.write(f'\nRegistros:')
            self.stdout.write(f'  Pacientes: {pacientes}')
            self.stdout.write(f'  Signos vitales: {signos}')
            self.stdout.write(f'  Profesionales: {profesionales}')

    def _analizar_memoria(self):
        """Analiza el uso de memoria del proceso."""
        self.stdout.write('\n🧠 ANÁLISIS DE MEMORIA')
        self.stdout.write('=' * 40)
        
        try:
            import psutil
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            rss_mb = memory_info.rss / (1024 * 1024)
            vms_mb = memory_info.vms / (1024 * 1024)
            
            self.stdout.write(f'Memoria RSS: {rss_mb:.2f} MB')
            self.stdout.write(f'Memoria VMS: {vms_mb:.2f} MB')
            self.stdout.write(f'CPU percent: {process.cpu_percent():.1f}%')
            
        except ImportError:
            self.stdout.write('psutil no disponible, usando info básica')
            
        # Información de Python
        self.stdout.write(f'Objetos en memoria: {len(gc.get_objects())}')
        self.stdout.write(f'Recolecciones GC: {gc.get_count()}')

    def _analizar_cache(self):
        """Analiza el estado del cache."""
        self.stdout.write('\n💾 ANÁLISIS DE CACHE')
        self.stdout.write('=' * 40)
        
        try:
            # Probar cache
            cache.set('test_key', 'test_value', 60)
            test_result = cache.get('test_key')
            cache.delete('test_key')
            
            if test_result == 'test_value':
                self.stdout.write('✅ Cache funcionando correctamente')
            else:
                self.stdout.write('❌ Problema con el cache')
                
            # Información de configuración
            cache_backend = settings.CACHES['default']['BACKEND']
            self.stdout.write(f'Backend: {cache_backend}')
            
            if 'locmem' in cache_backend:
                self.stdout.write('Tipo: Memoria local (recomendado para triage)')
            
        except Exception as e:
            self.stdout.write(f'❌ Error en cache: {e}')

    def _analizar_consultas_detalladas(self):
        """Análisis detallado de consultas más comunes."""
        self.stdout.write('\n🔍 ANÁLISIS DETALLADO DE CONSULTAS')
        self.stdout.write('=' * 40)
        
        from django.db import connection
        from django.test.utils import override_settings
        
        # Habilitar logging de consultas temporalmente
        with override_settings(LOGGING_CONFIG=None):
            from django.db import reset_queries
            reset_queries()
            
            # Simular consultas típicas del dashboard
            self.stdout.write('Simulando consultas del dashboard...')
            
            # Query 1: Estadísticas
            stats = SignosVitales.objects.filter(
                nivel_urgencia__isnull=False
            ).aggregate(
                total=connection.ops.count('id'),
            )
            
            # Query 2: Pacientes críticos
            criticos = list(SignosVitales.objects.filter(
                nivel_urgencia__in=['ROJO', 'AMARILLO']
            ).select_related('paciente', 'profesional__user')[:5])
            
            # Query 3: Lista de pacientes
            pacientes = list(Paciente.objects.activos_en_espera()[:10])
            
            # Mostrar número de consultas
            queries_count = len(connection.queries)
            self.stdout.write(f'Consultas ejecutadas: {queries_count}')
            
            if queries_count > 10:
                self.stdout.write('⚠️ Muchas consultas, revisar optimizaciones')
            else:
                self.stdout.write('✅ Número de consultas aceptable')

    def _mostrar_recomendaciones(self):
        """Muestra recomendaciones basadas en el análisis."""
        self.stdout.write('\n💡 RECOMENDACIONES')
        self.stdout.write('=' * 40)
        
        recomendaciones = [
            "✅ Ejecutar 'python manage.py optimize_db' semanalmente",
            "✅ Monitorear tamaño de BD, considerar limpieza si >100MB",
            "✅ Verificar logs en /logs/ periódicamente",
            "✅ En producción, usar un servidor web como Gunicorn",
            "✅ Considerar backup automático de BD crítica",
            "✅ Monitorear memoria si supera 500MB consistentemente",
        ]
        
        for rec in recomendaciones:
            self.stdout.write(rec)
        
        # Recomendaciones específicas basadas en el estado
        total_pacientes = Paciente.objects.count()
        if total_pacientes > 1000:
            self.stdout.write("⚠️ Considerar archivado de pacientes antiguos")
        
        total_signos = SignosVitales.objects.count()
        if total_signos > 5000:
            self.stdout.write("⚠️ Considerar limpieza de signos vitales antiguos")