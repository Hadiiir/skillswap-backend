#!/bin/bash

echo "🧹 Cleaning up old installation..."

# Remove old virtual environment
if [ -d "venv" ]; then
    rm -rf venv
    echo "✅ Removed old virtual environment"
fi

# Remove old migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
echo "✅ Removed old migrations"

# Remove database
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
    echo "✅ Removed old database"
fi

echo "🔧 Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing basic requirements..."
pip install --upgrade pip
pip install -r requirements_basic.txt

echo "✅ Fresh installation complete!"
