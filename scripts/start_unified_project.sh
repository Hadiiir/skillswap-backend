#!/bin/bash

echo "🚀 Starting SkillSwap Unified Project..."

echo "🛑 Stopping existing containers..."
docker-compose down

echo "🏗️ Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 15

echo "🔍 Checking service status..."
docker-compose ps

echo "📋 Showing logs..."
docker-compose logs --tail=50

echo "✅ SkillSwap Unified Project started!"
echo "🌐 Available URLs:"
echo "   - Django App: http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/swagger/"
echo "   - ReDoc: http://localhost:8000/redoc/"
echo "   - Admin Panel: http://localhost:8000/admin/"
echo "   - Flower Monitor: http://localhost:5555"
echo "   - PostgreSQL: localhost:5434"
echo "   - Redis: localhost:6380"
