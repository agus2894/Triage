# Configuración local para desarrollo y pruebas
from .settings import *
import os

# Base de datos SQLite para desarrollo local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'triage_local.sqlite3',
    }
}

# Configuración para desarrollo
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Cache simplificado para desarrollo
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Deshabilitar signals automáticos para pruebas locales
SIGNAL_DENYLIST = ['DISABLE_AUTO_SIGNALS']

print("🔧 Usando configuración local con SQLite")