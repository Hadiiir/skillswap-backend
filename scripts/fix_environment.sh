#!/bin/bash

echo "🔧 Fixing Django environment..."

# Stop any running processes
pkill -f "python manage.py"
pkill -f "celery"

# Remove old virtual environment
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
echo "Creating fresh virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install fixed requirements
echo "Installing requirements..."
pip install -r requirements_fixed.txt

# Test Django
echo "Testing Django installation..."
python -c "import django; print(f'Django {django.get_version()} installed successfully')"

# Create simple settings test
echo "Testing Django settings..."
python manage.py check --settings=skillswap.settings_simple

echo "✅ Environment fixed! You can now run:"
echo "source venv/bin/activate"
echo "python manage.py runserver"
