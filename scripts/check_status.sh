#!/bin/bash

echo "📊 SkillSwap Project Status"
echo "==========================="

echo ""
echo "🐳 Docker Containers Status:"
docker-compose -f docker-compose.simple.yml ps

echo ""
echo "🌐 Services Check:"

# Check API
if curl -s http://localhost:8000/api/skills/ > /dev/null; then
    echo "✅ API: Working properly"
else
    echo "❌ API: Not working"
fi

# Check Database
if docker-compose -f docker-compose.simple.yml exec db pg_isready -U skillswap > /dev/null 2>&1; then
    echo "✅ Database: Connected"
else
    echo "❌ Database: Not connected"
fi

# Check Admin Panel
if curl -s http://localhost:8000/admin/ > /dev/null; then
    echo "✅ Admin Panel: Available"
else
    echo "❌ Admin Panel: Unavailable"
fi

echo ""
echo "📈 Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "🔗 Links:"
echo "- API: http://localhost:8000/api/"
echo "- Admin: http://localhost:8000/admin/"
echo "- Database: localhost:5434"
