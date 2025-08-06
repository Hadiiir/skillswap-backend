#!/bin/bash

echo "🚀 Starting SkillSwap with Swagger..."

# Stop any running containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Install Swagger dependencies
echo "📦 Installing Swagger dependencies..."
pip install drf-yasg==1.21.7 packaging inflection ruamel.yaml coreapi coreschema

# Build and start containers
echo "🏗️ Building and starting containers..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Showing logs..."
docker-compose logs web

echo "✅ SkillSwap started with Swagger!"
echo "🌐 Available URLs:"
echo "   - Swagger UI: http://localhost:8000/swagger/"
echo "   - ReDoc: http://localhost:8000/redoc/"
echo "   - API Root: http://localhost:8000/api/"
echo "   - Admin: http://localhost:8000/admin/"
