#!/bin/bash

echo "📊 SkillSwap Project Status"
echo "=========================="

echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "📈 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo "🌐 Service Health:"
echo "- Web App: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/ || echo "DOWN")"
echo "- Swagger: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/swagger/ || echo "DOWN")"
echo "- Flower: $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5555 || echo "DOWN")"

echo ""
echo "💾 Volume Usage:"
docker system df -v | grep skillswap
