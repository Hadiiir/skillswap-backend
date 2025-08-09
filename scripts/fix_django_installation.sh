#!/bin/bash

echo "🔧 Fixing Django Installation..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    exit 1
fi

echo "🗑️ Removing corrupted Django installation..."
pip uninstall -y django djangorestframework djangorestframework-simplejwt

echo "🧹 Cleaning pip cache..."
pip cache purge

echo "📦 Reinstalling Django and dependencies..."
pip install --no-cache-dir Django==5.1.4
pip install --no-cache-dir djangorestframework==3.15.2
pip install --no-cache-dir djangorestframework-simplejwt==5.3.0

echo "🔍 Verifying Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"
python -c "from django.db import migrations; print('✅ Django migrations module working')"

echo "📋 Installing remaining requirements..."
pip install --no-cache-dir -r requirements.txt

echo -e "${GREEN}✅ Django installation fixed!${NC}"
