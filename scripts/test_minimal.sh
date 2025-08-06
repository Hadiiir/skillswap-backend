#!/bin/bash

echo "🧪 Testing SkillSwap with minimal configuration..."

# Set minimal settings
export DJANGO_SETTINGS_MODULE=skillswap.settings_minimal

# Test basic functionality
echo "📊 Testing database connection..."
python manage.py check --database default

echo "🔍 Testing API endpoints..."
python manage.py shell -c "
from django.test import Client
client = Client()

# Test basic endpoints
try:
    response = client.get('/api/skills/')
    print(f'✅ Skills API: {response.status_code}')
except Exception as e:
    print(f'❌ Skills API error: {e}')

try:
    response = client.get('/api/accounts/users/')
    print(f'✅ Users API: {response.status_code}')
except Exception as e:
    print(f'❌ Users API error: {e}')
"

echo "🎉 Basic tests completed!"
