"""
Comando personalizado para optimizar la base de datos
Ejecutar: python manage.py optimize_db
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Optimiza la base de datos SQLite para mejor rendimiento'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Optimizando base de datos...')
        
        with connection.cursor() as cursor:
            # Activar WAL mode para mejor concurrencia
            cursor.execute('PRAGMA journal_mode=WAL;')
            result = cursor.fetchone()
            self.stdout.write(f'✅ WAL mode: {result[0]}')
            
            # Optimizar configuración SQLite
            cursor.execute('PRAGMA synchronous=NORMAL;')
            cursor.execute('PRAGMA cache_size=10000;')
            cursor.execute('PRAGMA temp_store=MEMORY;')
            cursor.execute('PRAGMA mmap_size=268435456;')  # 256MB
            
            # Analizar índices
            cursor.execute('ANALYZE;')
            self.stdout.write('✅ Análisis de índices completado')
            
            # Vacuum para limpiar espacio
            cursor.execute('VACUUM;')
            self.stdout.write('✅ Vacuum completado')
            
        self.stdout.write('🎯 Base de datos optimizada para triage médico')