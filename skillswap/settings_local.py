"""
Local development settings for SkillSwap
"""
from .settings import *
import os

# Override database for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable Redis for local development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Disable Celery for local development
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Channel layers for local development
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Remove OAuth2 provider from installed apps for local development
INSTALLED_APPS = [app for app in INSTALLED_APPS if 'oauth2_provider' not in app]

# Remove OAuth2 middleware
MIDDLEWARE = [middleware for middleware in MIDDLEWARE if 'oauth2_provider' not in middleware]

# Remove OAuth2 authentication
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]

# Debug settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']

print("🔧 Using local development settings with SQLite database")
