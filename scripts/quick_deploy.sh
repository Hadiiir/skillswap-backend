#!/bin/bash

# 🚀 Quick SkillSwap Deployment Script for Server
# Run this script directly on your server

echo "🚀 Quick SkillSwap Deployment"
echo "============================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Set variables
PROJECT_DIR="/opt/skillswap-backend"
DOMAIN="skillswap.example.com"  # Change this to your domain

echo "📁 Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "📦 Installing required packages..."
apt update
apt install -y curl wget git docker.io docker-compose nginx certbot python3-certbot-nginx ufw

echo "🐳 Starting Docker..."
systemctl enable docker
systemctl start docker

echo "📋 Creating docker-compose.production.yml..."
cat > docker-compose.production.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: skillswap_db_prod
    environment:
      POSTGRES_DB: skillswap_prod
      POSTGRES_USER: skillswap_user
      POSTGRES_PASSWORD: secure_password_123
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - skillswap-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: skillswap_redis_prod
    command: redis-server --requirepass redis_password_123
    networks:
      - skillswap-network
    restart: unless-stopped

  web:
    image: python:3.11-slim
    container_name: skillswap_web_prod
    working_dir: /app
    command: >
      sh -c "
        apt-get update && apt-get install -y gcc postgresql-client libpq-dev curl &&
        pip install django djangorestframework django-cors-headers psycopg2-binary redis django-redis celery gunicorn &&
        python manage.py migrate &&
        python manage.py collectstatic --noinput &&
        gunicorn skillswap.wsgi:application --bind 0.0.0.0:8000 --workers 3
      "
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    networks:
      - skillswap-network
    environment:
      - DJANGO_SETTINGS_MODULE=skillswap.settings
      - DEBUG=False
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  skillswap-network:
    driver: bridge
EOF

echo "⚙️ Creating basic Django project structure..."
mkdir -p skillswap accounts skills points chat payments reviews notifications
touch skillswap/__init__.py skillswap/settings.py skillswap/urls.py skillswap/wsgi.py
touch accounts/__init__.py skills/__init__.py points/__init__.py
touch chat/__init__.py payments/__init__.py reviews/__init__.py notifications/__init__.py
touch manage.py requirements.txt

echo "📝 Creating basic settings.py..."
cat > skillswap/settings.py << 'EOF'
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skillswap.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'skillswap.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skillswap_prod',
        'USER': 'skillswap_user',
        'PASSWORD': 'secure_password_123',
        'HOST': 'db',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

CORS_ALLOW_ALL_ORIGINS = True
EOF

echo "📝 Creating basic urls.py..."
cat > skillswap/urls.py << 'EOF'
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'SkillSwap API is running!',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('', api_root),
]
EOF

echo "📝 Creating basic wsgi.py..."
cat > skillswap/wsgi.py << 'EOF'
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')
application = get_wsgi_application()
EOF

echo "📝 Creating manage.py..."
cat > manage.py << 'EOF'
#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
EOF

chmod +x manage.py

echo "📝 Creating requirements.txt..."
cat > requirements.txt << 'EOF'
Django>=4.2.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
psycopg2-binary>=2.9.0
redis>=4.5.0
django-redis>=5.2.0
celery>=5.2.0
gunicorn>=20.1.0
EOF

echo "🐳 Starting containers..."
docker-compose -f docker-compose.production.yml up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🌐 Configuring Nginx..."
cat > /etc/nginx/sites-available/skillswap << 'EOF'
server {
    listen 80;
    server_name _;
    
    client_max_body_size 100M;
    
    location /static/ {
        alias /opt/skillswap-backend/staticfiles/;
        expires 1y;
    }
    
    location /media/ {
        alias /opt/skillswap-backend/media/;
        expires 1y;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/skillswap /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "🔥 Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 'Nginx Full'

echo "✅ Deployment completed!"
echo
echo "🌐 Your SkillSwap API is now accessible at:"
echo "   http://$(curl -s ifconfig.me)/"
echo "   http://$(hostname -I | awk '{print $1}')/"
echo
echo "📊 Check status with:"
echo "   docker-compose -f $PROJECT_DIR/docker-compose.production.yml ps"
echo
echo "📋 View logs with:"
echo "   docker-compose -f $PROJECT_DIR/docker-compose.production.yml logs -f"
echo
echo "🔧 To upload your full project, use:"
echo "   scp -r /path/to/your/project/* root@$(curl -s ifconfig.me):$PROJECT_DIR/"
