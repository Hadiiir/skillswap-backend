#!/bin/bash

echo "📊 SkillSwap Project Status"
echo "=========================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if services are running
echo -e "\n🔍 Service Status:"
docker-compose ps

echo -e "\n🏥 Health Checks:"

# Database health
if docker-compose exec -T db pg_isready -U skillswap -d skillswap > /dev/null 2>&1; then
    echo -e "   Database: ${GREEN}✅ Healthy${NC}"
else
    echo -e "   Database: ${RED}❌ Unhealthy${NC}"
fi

# Redis health
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "   Redis: ${GREEN}✅ Healthy${NC}"
else
    echo -e "   Redis: ${RED}❌ Unhealthy${NC}"
fi

# Web service health
if curl -f http://localhost:8000 > /dev/null 2>&1; then
    echo -e "   Web Service: ${GREEN}✅ Healthy${NC}"
else
    echo -e "   Web Service: ${RED}❌ Unhealthy${NC}"
fi

echo -e "\n📈 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo -e "\n🔗 Service URLs:"
echo "   🌐 Web: http://localhost:8000"
echo "   🔧 Admin: http://localhost:8000/admin/"
echo "   📊 API: http://localhost:8000/api/"
