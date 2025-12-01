"""
🔄 COMANDO SYNC_OFFLINE
=======================
Sincroniza datos entre SQLite (offline) y PostgreSQL (online).
"""

from django.core.management.base import BaseCommand
from django.db import transaction, connections
from django.contrib.auth.models import User
from apps.triage.models import Profesional, SignosVitales
from apps.patients.models import Paciente
import sqlite3
import os


class Command(BaseCommand):
    help = 'Sincroniza datos entre base de datos offline (SQLite) y online (PostgreSQL)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--direction',
            type=str,
            choices=['to-online', 'from-online'],
            default='to-online',
            help='Dirección de sincronización: to-online (SQLite→PostgreSQL) o from-online (PostgreSQL→SQLite)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simular sin hacer cambios reales',
        )

    def handle(self, *args, **options):
        direction = options['direction']
        dry_run = options['dry_run']

        self.stdout.write("🔄 Sincronización de Datos")
        self.stdout.write("=" * 50)
        
        if dry_run:
            self.stdout.write(self.style.WARNING("⚠️  MODO DRY-RUN (simulación)"))
        
        if direction == 'to-online':
            self.stdout.write("📤 Sincronizando: SQLite → PostgreSQL (online)")
            self._sync_to_online(dry_run)
        else:
            self.stdout.write("📥 Sincronizando: PostgreSQL → SQLite (offline)")
            self._sync_from_online(dry_run)

    def _sync_to_online(self, dry_run):
        """Sincroniza datos locales (SQLite) hacia PostgreSQL."""
        
        self.stdout.write("\n🔍 Verificando datos nuevos en SQLite...")
        
        # TODO: Implementar lógica de sincronización
        # 1. Detectar registros nuevos/modificados en SQLite
        # 2. Copiarlos a PostgreSQL evitando duplicados
        # 3. Manejar conflictos (por timestamps, última modificación gana)
        
        self.stdout.write(self.style.WARNING(
            "⚠️  Sincronización to-online aún no implementada"
        ))
        self.stdout.write("\n💡 Para futuras versiones:")
        self.stdout.write("   • Detectar pacientes/triages nuevos en SQLite")
        self.stdout.write("   • Copiarlos a PostgreSQL con resolución de conflictos")
        self.stdout.write("   • Marcar como sincronizados")

    def _sync_from_online(self, dry_run):
        """Sincroniza datos desde PostgreSQL hacia SQLite local."""
        
        self.stdout.write("\n🔍 Verificando datos en PostgreSQL...")
        
        # TODO: Implementar lógica de sincronización
        # 1. Obtener datos recientes de PostgreSQL
        # 2. Copiarlos a SQLite offline para tener backup
        
        self.stdout.write(self.style.WARNING(
            "⚠️  Sincronización from-online aún no implementada"
        ))
        self.stdout.write("\n💡 Para futuras versiones:")
        self.stdout.write("   • Descargar datos recientes de PostgreSQL")
        self.stdout.write("   • Actualizar SQLite para modo offline")
        self.stdout.write("   • Mantener consistencia entre ambas BDs")
