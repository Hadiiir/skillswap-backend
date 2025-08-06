#!/bin/bash

echo "🔄 Restarting SkillSwap Project"
echo "==============================="

# Stop services
echo "🛑 Stopping services..."
docker-compose -f docker-compose.simple.yml down

# Restart services
echo "🚀 Restarting services..."
docker-compose -f docker-compose.simple.yml up -d

# Wait for startup
echo "⏳ Waiting for startup..."
sleep 15

# Connection test
echo "🧪 Testing connection..."
curl -s http://localhost:8000/api/skills/ > /dev/null && echo "✅ API is working!" || echo "❌ API issue"

echo "🎉 Restart completed successfully!"
