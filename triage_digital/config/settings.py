"""
Triage Digital - Configuración Django optimizada.
Filosofía: "Menos es más" - Solo lo esencial para salvar vidas.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def _load_env_file():
    """Carga variables desde el archivo .env si existe (raíz o subdirectorio)."""
    candidates = [
        BASE_DIR / '.env',
        BASE_DIR.parent / '.env'
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            k = k.strip()
                            v = v.strip().strip("'\"")
                            if k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass
            break

_load_env_file()

# SECURITY: Variables de entorno con fallbacks seguros
SECRET_KEY = os.environ.get('SECRET_KEY', 'triage-digital-2025-key-CHANGE-IN-PRODUCTION')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Hosts permitidos - Configurado para red hospitalaria
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,192.168.*,10.*,172.*').split(',') if h.strip()]

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

# Middleware AUTO-OPTIMIZADO - Optimización transparente automática
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
    SECURE_SSL_REDIRECT = False  # En hospital puede no tener SSL interno

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

# Database - Configuración Híbrida Online/Offline
try:
    from .database_utils import get_database_config
    DATABASES = get_database_config()
except ImportError:
    # Fallback a SQLite local si no está disponible database_utils
    print("⚠️  Usando configuración de SQLite local (fallback)")
    db_dir = BASE_DIR / 'db'
    db_dir.mkdir(exist_ok=True)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(db_dir / 'triage_offline.sqlite3'),
            'OPTIONS': {'timeout': 20},
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

# Cache optimizado para consultas críticas de triage
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'triage-emergency-cache',
        'TIMEOUT': 300,  # 5 minutos - balance entre velocidad y actualización
        'OPTIONS': {
            'MAX_ENTRIES': 5000,  # Más entradas para hospital activo
            'CULL_FREQUENCY': 3,   # Limpiar cache más frecuentemente
        }
    },
    # Cache específico para estadísticas que pueden ser menos críticas
    'stats': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'triage-stats-cache',
        'TIMEOUT': 900,  # 15 minutos para estadísticas
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 4,
        }
    }
}

# Optimizaciones de performance
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Archivos estáticos - Solo Bootstrap CDN, sin archivos locales
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de autenticación optimizada
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/triage/'
LOGOUT_REDIRECT_URL = '/login/'

# Sesiones optimizadas para uso hospitalario intensivo
SESSION_COOKIE_AGE = 28800  # 8 horas - turno hospitalario típico
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = False  # Solo guardar cuando cambie
SESSION_CACHE_ALIAS = 'default'  # Usar cache para sesiones rápidas
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  # Cache + DB híbrido

# Configuración de logging optimizada para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',  # Solo errores importantes en producción
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'triage.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps.triage': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Crear directorio de logs si no existe
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)