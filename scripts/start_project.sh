#!/bin/bash

echo "🚀 Fully Running the SkillSwap Project"
echo "=================================="

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first"
    exit 1
fi

echo "✅ Docker is available"

# Stop any old containers
echo "🛑 Stopping old containers..."
docker-compose -f docker-compose.simple.yml down

# Start the services
echo "🚀 Starting services..."
docker-compose -f docker-compose.simple.yml up -d

# Wait for the database to start
echo "⏳ Waiting for the database to start..."
sleep 15

# Check service status
echo "📊 Service status:"
docker-compose -f docker-compose.simple.yml ps

# Test connection to API
echo "🧪 Testing API connection..."
if curl -s http://localhost:8000/api/skills/ > /dev/null; then
    echo "✅ API is working correctly!"
else
    echo "❌ Issue connecting to the API"
fi

echo ""
echo "🌐 Access Links:"
echo "- API: http://localhost:8000/api/"
echo "- Admin Panel: http://localhost:8000/admin/"
echo "- Database: localhost:5434"

echo ""
echo "👤 Demo Accounts:"
echo "- ahmed@example.com : testpass123"
echo "- sara@example.com : testpass123"

echo ""
echo "🎉 The project is ready to use!"
