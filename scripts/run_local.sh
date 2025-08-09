#!/bin/bash

echo "🚀 Starting Local Environment..."

# Load local environment
export $(cat .env.local | xargs)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if not exists
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@skillswap.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Local environment ready!"
echo "🌐 Admin: http://localhost:8000/admin"
echo "📚 API: http://localhost:8000/api"
echo "📖 Swagger: http://localhost:8000/swagger"

# Start server
python manage.py runserver 0.0.0.0:8000
