"""
Triage Digital - Configuración Django optimizada.
Filosofía: "Menos es más" - Solo lo esencial para salvar vidas.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Cambiar en producción usando variables de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'triage-digital-2025-key-CHANGE-IN-PRODUCTION')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Hosts permitidos - expandir según necesidad
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.patients',
    'apps.triage',
]

# Middleware optimizado - Solo lo necesario
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuraciones de seguridad para producción
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Base de datos optimizada para triage médico
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'triage_digital.sqlite3',
        # SQLite es simple y rápido - perfecto para triage hospitalario
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

LOGIN_URL = '/login/'

# Cache optimizado para consultas críticas de triage
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'triage-emergency-cache',
        'TIMEOUT': 180,  # 3 minutos - datos críticos, cache corto
        'OPTIONS': {
            'MAX_ENTRIES': 2000,  # Más entradas para hospital activo
            'CULL_FREQUENCY': 3,   # Limpiar cache más frecuentemente
        }
    }
}

# Optimizaciones de performance
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging minimalista - Solo errores críticos
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'triage.log',
        },
    },
    'loggers': {
        'apps.triage': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}

# Archivos estáticos - Solo Bootstrap CDN, sin archivos locales
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (no necesarios para este proyecto)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de autenticación optimizada
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/triage/'
LOGOUT_REDIRECT_URL = '/login/'

# Sesiones optimizadas para uso hospitalario
SESSION_COOKIE_AGE = 28800  # 8 horas - turno hospitalario típico
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False  # Solo guardar cuando cambie