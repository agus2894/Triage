from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Optimiza la base de datos SQLite'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Optimizando base de datos...')
        
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode=WAL;')
            cursor.execute('PRAGMA synchronous=NORMAL;')
            cursor.execute('PRAGMA cache_size=20000;')
            cursor.execute('PRAGMA temp_store=MEMORY;')
            cursor.execute('PRAGMA mmap_size=268435456;')
            cursor.execute('PRAGMA foreign_keys=ON;')
            cursor.execute('ANALYZE;')
            cursor.execute('PRAGMA optimize;')
            
        self.stdout.write('✅ Optimización completada')
