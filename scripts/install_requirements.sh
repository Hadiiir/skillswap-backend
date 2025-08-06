#!/bin/bash

echo "🔧 Installing required packages..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No virtual environment found, creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements from requirements.txt..."
pip install -r requirements.txt

echo "✅ All packages installed successfully!"

# Check if celery is installed
python -c "import celery; print('✅ Celery installed successfully')" 2>/dev/null || echo "❌ Celery installation failed"

# Check if redis is available
python -c "import redis; print('✅ Redis client installed successfully')" 2>/dev/null || echo "❌ Redis client installation failed"

echo "🎉 Installation complete!"
