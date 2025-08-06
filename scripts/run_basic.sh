#!/bin/bash

echo "🚀 Starting SkillSwap with basic configuration..."

# Fresh install
chmod +x scripts/fresh_install.sh
./scripts/fresh_install.sh

# Activate virtual environment
source venv/bin/activate

# Use basic settings
export DJANGO_SETTINGS_MODULE=skillswap.settings_basic

# Create database and run migrations
echo "📊 Setting up database..."
python manage.py makemigrations accounts
python manage.py makemigrations skills
python manage.py makemigrations points
python manage.py makemigrations reviews
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Superuser created: admin@skillswap.com/admin123')
else:
    print('✅ Superuser already exists')
"

# Load sample data
echo "📝 Loading sample data..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings_basic')
django.setup()

from django.contrib.auth import get_user_model
from skills.models import Category, Skill
from points.models import PointsPackage

User = get_user_model()

# Create categories
categories = [
    {'name': 'Programming', 'description': 'Web development, mobile apps'},
    {'name': 'Design', 'description': 'Graphic design, UI/UX'},
    {'name': 'Marketing', 'description': 'Digital marketing, SEO'},
]

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f'✅ Created category: {category.name}')

# Create points packages
packages = [
    {'name': 'Starter', 'points': 50, 'price': 50.00},
    {'name': 'Popular', 'points': 200, 'price': 170.00, 'is_popular': True},
    {'name': 'Premium', 'points': 500, 'price': 400.00},
]

for pkg_data in packages:
    package, created = PointsPackage.objects.get_or_create(
        name=pkg_data['name'],
        defaults=pkg_data
    )
    if created:
        print(f'✅ Created package: {package.name}')

print('🎉 Sample data loaded!')
"

echo "🎉 Starting development server..."
python manage.py runserver
