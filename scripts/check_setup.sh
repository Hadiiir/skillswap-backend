#!/bin/bash

echo "🔍 SkillSwap Backend Status Check"
echo "================================"

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment: Active ($VIRTUAL_ENV)"
else
    echo "❌ Virtual environment: Not active"
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1)
echo "🐍 Python version: $PYTHON_VERSION"

# Check if Django is installed
if python -c "import django" 2>/dev/null; then
    DJANGO_VERSION=$(python -c "import django; print(django.get_version())")
    echo "✅ Django: $DJANGO_VERSION"
else
    echo "❌ Django: Not installed"
fi

# Check if database exists
if [ -f "db.sqlite3" ]; then
    echo "✅ SQLite database: Found"
else
    echo "❌ SQLite database: Not found"
fi

# Check if Docker is available
if command -v docker &> /dev/null; then
    echo "✅ Docker: Available"
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Docker containers: Running"
    else
        echo "❌ Docker containers: Not running"
    fi
else
    echo "❌ Docker: Not available"
fi

# Check if port 8000 is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null; then
    echo "⚠️  Port 8000: In use"
else
    echo "✅ Port 8000: Available"
fi

echo ""
echo "🚀 Quick Start Commands:"
echo "   Local development: bash scripts/run_local.sh"
echo "   Docker setup: bash scripts/setup_docker.sh"
echo "   Status check: bash scripts/check_setup.sh"
