"""
Comando personalizado para optimizar la base de datos
Ejecutar: python manage.py optimize_db
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Optimiza la base de datos SQLite para mejor rendimiento'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Optimizando base de datos para triage médico...')
        
        with connection.cursor() as cursor:
            # 1. Activar WAL mode para mejor concurrencia (múltiples lecturas simultáneas)
            cursor.execute('PRAGMA journal_mode=WAL;')
            result = cursor.fetchone()
            self.stdout.write(f'✅ WAL mode: {result[0]}')
            
            # 2. Configuraciones críticas para rendimiento hospitalario
            optimizations = [
                ('PRAGMA synchronous=NORMAL;', 'Sincronización optimizada'),
                ('PRAGMA cache_size=20000;', 'Cache aumentado a 20MB'),  # Aumentado para más pacientes
                ('PRAGMA temp_store=MEMORY;', 'Tablas temporales en RAM'),
                ('PRAGMA mmap_size=268435456;', 'Memory mapping 256MB'),
                ('PRAGMA page_size=4096;', 'Tamaño de página optimizado'),
                ('PRAGMA auto_vacuum=INCREMENTAL;', 'Auto-vacuum incremental'),
                ('PRAGMA wal_autocheckpoint=1000;', 'Checkpoint WAL optimizado'),
                ('PRAGMA query_only=OFF;', 'Modo escritura habilitado'),
                ('PRAGMA foreign_keys=ON;', 'Claves foráneas activas'),
                ('PRAGMA secure_delete=OFF;', 'Borrado rápido para logs'),
            ]
            
            for pragma, description in optimizations:
                cursor.execute(pragma)
                self.stdout.write(f'✅ {description}')
            
            # 3. Analizar y optimizar índices críticos
            cursor.execute('ANALYZE;')
            self.stdout.write('✅ Análisis de índices completado')
            
            # 4. Vacuum incremental para limpiar sin bloquear
            cursor.execute('PRAGMA incremental_vacuum;')
            self.stdout.write('✅ Vacuum incremental completado')
            
            # 5. Verificar integridad (crítico en ambiente médico)
            cursor.execute('PRAGMA integrity_check;')
            result = cursor.fetchone()
            if result[0] == 'ok':
                self.stdout.write('✅ Integridad de base de datos verificada')
            else:
                self.stdout.write(self.style.ERROR(f'⚠️ Problema de integridad: {result[0]}'))
                
        self.stdout.write(
            self.style.SUCCESS('🎯 Base de datos optimizada para emergencias médicas')
        )
