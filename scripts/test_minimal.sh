#!/bin/bash

echo "🧪 Testing minimal Django setup..."

# Activate virtual environment
source venv/bin/activate

# Test minimal settings
echo "Testing minimal settings..."
python manage.py check --settings=skillswap.settings_minimal

# Create migrations
echo "Creating migrations..."
python manage.py makemigrations --settings=skillswap.settings_minimal

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --settings=skillswap.settings_minimal

# Test server startup
echo "Testing server startup..."
timeout 10s python manage.py runserver --settings=skillswap.settings_minimal 8001 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 3

# Test health endpoint
echo "Testing health endpoint..."
curl -s http://localhost:8001/api/health/ || echo "Health check failed"

# Stop server
kill $SERVER_PID 2>/dev/null

echo "✅ Minimal setup test completed!"
