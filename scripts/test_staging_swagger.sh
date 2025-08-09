#!/bin/bash

echo "🧪 Testing Staging Environment with Swagger..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if server is running
echo "🔍 Checking if staging server is running..."
if curl -s http://localhost:8001/api/ > /dev/null; then
    echo -e "${GREEN}✅ Staging server is running${NC}"
else
    echo -e "${RED}❌ Staging server is not running on port 8001${NC}"
    echo "Please run: ./scripts/run_staging.sh"
    exit 1
fi

# Test API endpoints
echo "📊 Testing API Endpoints..."

# Test Categories
echo "🏷️ Categories API:"
CATEGORIES_RESPONSE=$(curl -s http://localhost:8001/api/skills/categories/)
if echo "$CATEGORIES_RESPONSE" | jq . > /dev/null 2>&1; then
    CATEGORIES_COUNT=$(echo "$CATEGORIES_RESPONSE" | jq length)
    echo -e "${GREEN}✅ Categories API working - Found $CATEGORIES_COUNT categories${NC}"
else
    echo -e "${RED}❌ Categories API failed${NC}"
    echo "$CATEGORIES_RESPONSE"
fi

# Test Skills
echo "🎯 Skills API:"
SKILLS_RESPONSE=$(curl -s "http://localhost:8001/api/skills/")
if echo "$SKILLS_RESPONSE" | jq . > /dev/null 2>&1; then
    SKILLS_COUNT=$(echo "$SKILLS_RESPONSE" | jq '.results | length')
    echo -e "${GREEN}✅ Skills API working - Found $SKILLS_COUNT skills${NC}"
else
    echo -e "${RED}❌ Skills API failed${NC}"
    echo "$SKILLS_RESPONSE"
fi

# Test Users (should require auth)
echo "👥 Users API:"
USERS_RESPONSE=$(curl -s http://localhost:8001/api/accounts/users/)
if echo "$USERS_RESPONSE" | jq . > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Users API responding${NC}"
else
    echo -e "${YELLOW}⚠️ Users API requires authentication (expected)${NC}"
fi

# Test Point Packages
echo "💰 Point Packages API:"
PACKAGES_RESPONSE=$(curl -s http://localhost:8001/api/points/packages/)
if echo "$PACKAGES_RESPONSE" | jq . > /dev/null 2>&1; then
    PACKAGES_COUNT=$(echo "$PACKAGES_RESPONSE" | jq length)
    echo -e "${GREEN}✅ Point Packages API working - Found $PACKAGES_COUNT packages${NC}"
else
    echo -e "${RED}❌ Point Packages API failed${NC}"
    echo "$PACKAGES_RESPONSE"
fi

# Summary
echo ""
echo "📈 API Statistics:"
CATEGORIES_COUNT=$(curl -s http://localhost:8001/api/skills/categories/ | jq length 2>/dev/null || echo "N/A")
SKILLS_COUNT=$(curl -s "http://localhost:8001/api/skills/" | jq '.count // .results | length' 2>/dev/null || echo "0")
USERS_COUNT=$(curl -s http://localhost:8001/api/accounts/users/ | jq length 2>/dev/null || echo "N/A")
PACKAGES_COUNT=$(curl -s http://localhost:8001/api/points/packages/ | jq length 2>/dev/null || echo "N/A")

echo "Categories: $CATEGORIES_COUNT"
echo "Skills: $SKILLS_COUNT"
echo "Users: $USERS_COUNT"
echo "Point Packages: $PACKAGES_COUNT"

echo ""
echo "🎯 Staging Environment Test Complete!"
echo ""
echo "🌐 Available URLs:"
echo "   Swagger UI: http://localhost:8001/swagger/"
echo "   ReDoc: http://localhost:8001/redoc/"
echo "   Admin Panel: http://localhost:8001/admin/"
echo "   API Root: http://localhost:8001/api/"
echo ""
echo "👤 Admin Credentials:"
echo "   Username: staging_admin"
echo "   Password: staging123"
echo ""
echo "👥 Test User Credentials:"
echo "   user1@staging.com / test123"
echo "   user2@staging.com / test123"
echo "   user3@staging.com / test123"
echo "   user4@staging.com / test123"
echo "   user5@staging.com / test123"
echo ""
echo "💡 Quick Test Commands:"
echo "   Test Login: curl -X POST http://localhost:8001/api/accounts/login/ -H 'Content-Type: application/json' -d '{\"username\":\"user1@staging.com\",\"password\":\"test123\"}'"
echo "   Get Skills: curl http://localhost:8001/api/skills/"
echo "   Get Categories: curl http://localhost:8001/api/skills/categories/"
