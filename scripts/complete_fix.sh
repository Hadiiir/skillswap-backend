#!/bin/bash

echo "🚀 Complete Django Fix Process"
echo "=============================="

# Step 1: Fix environment
echo "Step 1: Fixing environment..."
chmod +x scripts/fix_environment.sh
./scripts/fix_environment.sh

# Step 2: Test minimal setup
echo "Step 2: Testing minimal setup..."
chmod +x scripts/test_minimal.sh
./scripts/test_minimal.sh

# Step 3: Test full setup
echo "Step 3: Testing full setup..."
source venv/bin/activate

# Check full settings
python manage.py check

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@skillswap.com').exists():
    User.objects.create_superuser(
        email='admin@skillswap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Test server
echo "Testing full server..."
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
python manage.py runserver
