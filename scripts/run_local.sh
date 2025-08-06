#!/bin/bash

echo "🚀 Starting SkillSwap Local Development Server"
echo "=============================================="

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "📦 Database not found. Running initial setup..."
    python scripts/setup_local_dev.py
fi

echo "🌐 Starting Django development server..."
echo "   Local server: http://127.0.0.1:8000/"
echo "   Admin panel: http://127.0.0.1:8000/admin/"
echo "   Admin credentials:"
echo "   Email: admin@skillswap.com"
echo "   Password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Set environment variable and run server
export DJANGO_SETTINGS_MODULE=skillswap.settings_local
python manage.py runserver 0.0.0.0:8000
