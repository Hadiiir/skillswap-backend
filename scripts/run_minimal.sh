#!/bin/bash

echo "🚀 Starting SkillSwap with minimal configuration..."

# Install requirements first
chmod +x scripts/install_requirements.sh
./scripts/install_requirements.sh

# Use minimal settings
export DJANGO_SETTINGS_MODULE=skillswap.settings_minimal

# Create database and run migrations
echo "📊 Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@skillswap.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"

# Load sample data
echo "📝 Loading sample data..."
python create_sample_data.py

echo "🎉 Starting development server..."
python manage.py runserver
