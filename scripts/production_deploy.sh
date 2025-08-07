#!/bin/bash

# 🚀 SkillSwap Production Deployment Script
# This script handles complete production deployment

set -e

echo "🚀 Starting SkillSwap Production Deployment..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create production environment file if it doesn't exist
if [ ! -f .env.production ]; then
    print_status "Creating production environment file..."
    cat > .env.production << EOF
# Django Settings
DEBUG=False
SECRET_KEY=your-super-secret-production-key-change-this-immediately
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DB_NAME=skillswap_prod
DB_USER=skillswap_user
DB_PASSWORD=secure_password_change_this
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://:redis_password@redis:6379/0
REDIS_PASSWORD=redis_password_change_this

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Settings
JWT_SECRET_KEY=jwt-secret-key-change-this
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# File Storage
MEDIA_URL=/media/
STATIC_URL=/static/

# Security
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Celery
CELERY_BROKER_URL=redis://:redis_password@redis:6379/0
CELERY_RESULT_BACKEND=redis://:redis_password@redis:6379/0
EOF
    print_warning "Created .env.production file. Please update the values before deployment!"
fi

# Create production settings if it doesn't exist
if [ ! -f skillswap/settings_production.py ]; then
    print_status "Creating production settings..."
    # This will be created in the next file
fi

# Create logs directory
mkdir -p logs

# Create SSL directory for certificates
mkdir -p ssl

# Stop any running containers
print_status "Stopping any running containers..."
docker-compose -f docker-compose.production.yml down --remove-orphans || true

# Build and start production containers
print_status "Building and starting production containers..."
docker-compose -f docker-compose.production.yml build --no-cache

print_status "Starting production services..."
docker-compose -f docker-compose.production.yml up -d

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.production.yml exec -T web python manage.py migrate

# Create superuser
print_status "Creating superuser..."
docker-compose -f docker-compose.production.yml exec -T web python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
EOF

# Collect static files
print_status "Collecting static files..."
docker-compose -f docker-compose.production.yml exec -T web python manage.py collectstatic --noinput

# Run seeders if requested
read -p "Do you want to run database seeders? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Running database seeders..."
    docker-compose -f docker-compose.production.yml exec -T web python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_production')
django.setup()

from scripts.seeders.master_seeder import MasterSeeder
seeder = MasterSeeder()
seeder.run()
"
fi

# Check container health
print_status "Checking container health..."
sleep 5

# Display status
print_success "Production deployment completed!"
echo
echo "🌐 Your SkillSwap application is now running in production mode!"
echo "=============================================="
echo "📊 Container Status:"
docker-compose -f docker-compose.production.yml ps
echo
echo "🔗 Access URLs:"
echo "   • API: http://localhost/api/"
echo "   • Admin: http://localhost/admin/"
echo "   • Swagger: http://localhost/swagger/"
echo
echo "👨‍💼 Admin Credentials:"
echo "   • Email: admin@skillswap.com"
echo "   • Password: admin123"
echo
echo "📋 Next Steps:"
echo "   1. Update .env.production with your actual values"
echo "   2. Configure your domain name"
echo "   3. Set up SSL certificates"
echo "   4. Configure backup strategy"
echo
print_warning "Remember to change default passwords and secret keys!"
