#!/bin/bash

echo "🚀 Starting Complete SkillSwap Project..."

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

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install it first."
    exit 1
fi

print_status "Stopping any existing containers..."
docker-compose down --remove-orphans

print_status "Removing old volumes (optional - comment out if you want to keep data)..."
# docker-compose down -v  # Uncomment to remove volumes

print_status "Building and starting all services..."
docker-compose up --build -d

print_status "Waiting for services to be ready..."
sleep 10

# Check service health
print_status "Checking service health..."

# Check database
if docker-compose exec -T db pg_isready -U skillswap -d skillswap > /dev/null 2>&1; then
    print_success "✅ Database is ready"
else
    print_error "❌ Database is not ready"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_success "✅ Redis is ready"
else
    print_error "❌ Redis is not ready"
fi

# Check web service
if curl -f http://localhost:8000 > /dev/null 2>&1; then
    print_success "✅ Web service is ready"
else
    print_warning "⚠️  Web service might still be starting..."
fi

print_status "Creating superuser (if needed)..."
docker-compose exec -T web python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("Superuser created: admin@skillswap.com / admin123")
else:
    print("Superuser already exists")
EOF

print_status "Loading sample data..."
docker-compose exec -T web python manage.py shell << EOF
exec(open('create_sample_data.py').read())
EOF

print_success "🎉 Project started successfully!"
echo ""
echo "📋 Service URLs:"
echo "   🌐 Web Application: http://localhost:8000"
echo "   🔧 Django Admin: http://localhost:8000/admin/"
echo "   📊 API Documentation: http://localhost:8000/api/"
echo "   🗄️  Database: localhost:5434"
echo "   🔴 Redis: localhost:6380"
echo ""
echo "👤 Admin Credentials:"
echo "   Email: admin@skillswap.com"
echo "   Password: admin123"
echo ""
echo "🔧 Useful Commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop project: docker-compose down"
echo "   Restart project: docker-compose restart"
echo "   Access web container: docker-compose exec web bash"
echo ""
print_status "Project is ready for development! 🚀"
