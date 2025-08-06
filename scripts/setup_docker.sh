#!/bin/bash

echo "🐳 Setting up SkillSwap with Docker"
echo "=================================="

# Stop any running containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove any existing volumes (optional - uncomment if you want fresh start)
# echo "🗑️ Removing existing volumes..."
# docker-compose down -v

# Build and start containers
echo "🔨 Building and starting containers..."
docker-compose up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 15

# Check if containers are running
echo "📋 Checking container status..."
docker-compose ps

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@skillswap.com / admin123')
else:
    print('✅ Superuser already exists')
"

# Create sample data
echo "📊 Creating sample data..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
from skills.models import Skill, Category

User = get_user_model()

# Create categories
categories_data = [
    {'name': 'Programming', 'description': 'Software development and programming skills'},
    {'name': 'Design', 'description': 'Graphic design, UI/UX, and creative skills'},
    {'name': 'Marketing', 'description': 'Digital marketing and business skills'},
    {'name': 'Languages', 'description': 'Language learning and translation'},
    {'name': 'Music', 'description': 'Musical instruments and music production'},
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f'   ✅ Created category: {category.name}')

# Create sample users
sample_users = [
    {
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Developer',
        'bio': 'Full-stack developer with 5 years experience'
    },
    {
        'email': 'sarah@example.com',
        'first_name': 'Sarah',
        'last_name': 'Designer',
        'bio': 'UI/UX designer passionate about user experience'
    }
]

for user_data in sample_users:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults={
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'bio': user_data['bio'],
            'points_balance': 150
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        print(f'   ✅ Created user: {user.first_name} {user.last_name}')

print('✅ Sample data created successfully!')
"

echo ""
echo "🎉 Docker setup complete!"
echo ""
echo "🌐 Application URLs:"
echo "   Main app: http://localhost:8000/"
echo "   Admin: http://localhost:8000/admin/"
echo ""
echo "👤 Admin credentials:"
echo "   Email: admin@skillswap.com"
echo "   Password: admin123"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Shell access: docker-compose exec web bash"
