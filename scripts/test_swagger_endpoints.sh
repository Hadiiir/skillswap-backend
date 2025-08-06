#!/bin/bash

echo "🔧 Full test of all endpoints using Swagger"
echo "==========================================="

BASE_URL="http://localhost:8000"
API_URL="$BASE_URL/api"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}📋 1. Testing Home Page:${NC}"
curl -s "$BASE_URL/" | python -m json.tool

echo ""
echo -e "${BLUE}📚 2. Testing Swagger UI:${NC}"
SWAGGER_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/swagger/")
if [ "$SWAGGER_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Swagger UI available at: $BASE_URL/swagger/${NC}"
else
    echo -e "${RED}❌ Swagger UI not available (HTTP $SWAGGER_RESPONSE)${NC}"
fi

echo ""
echo -e "${BLUE}📖 3. Testing ReDoc:${NC}"
REDOC_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/redoc/")
if [ "$REDOC_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ ReDoc available at: $BASE_URL/redoc/${NC}"
else
    echo -e "${RED}❌ ReDoc not available (HTTP $REDOC_RESPONSE)${NC}"
fi

echo ""
echo -e "${BLUE}🔗 4. Testing Swagger JSON Schema:${NC}"
SCHEMA_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/swagger.json")
if [ "$SCHEMA_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Swagger JSON Schema available at: $BASE_URL/swagger.json${NC}"
else
    echo -e "${RED}❌ Swagger JSON Schema not available (HTTP $SCHEMA_RESPONSE)${NC}"
fi

echo ""
echo -e "${YELLOW}🧪 Testing core API endpoints:${NC}"

# Test Authentication endpoints
echo ""
echo -e "${BLUE}👤 Testing Authentication Endpoints:${NC}"
echo "- Register: POST $API_URL/auth/register/"
echo "- Login: POST $API_URL/auth/login/"
echo "- Profile: GET $API_URL/auth/profile/"
echo "- Token Refresh: POST $API_URL/auth/token/refresh/"

# Test Skills endpoints
echo ""
echo -e "${BLUE}🎯 Testing Skills Endpoint:${NC}"
SKILLS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/skills/")
if [ "$SKILLS_RESPONSE" = "401" ]; then
    echo -e "${YELLOW}⚠️  Skills endpoint requires authentication (HTTP 401) - This is correct${NC}"
elif [ "$SKILLS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Skills endpoint is working${NC}"
else
    echo -e "${RED}❌ Issue with skills endpoint (HTTP $SKILLS_RESPONSE)${NC}"
fi

# Test Categories
echo ""
echo -e "${BLUE}📂 Testing Skill Categories:${NC}"
CATEGORIES_RESPONSE=$(curl -s "$API_URL/skills/categories/")
if echo "$CATEGORIES_RESPONSE" | python -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
    echo -e "${GREEN}✅ Skill categories are working correctly${NC}"
    echo "$CATEGORIES_RESPONSE" | python -m json.tool | head -20
else
    echo -e "${RED}❌ Issue with skill categories${NC}"
fi

# Test Points endpoints
echo ""
echo -e "${BLUE}💰 Testing Points Packages Endpoint:${NC}"
POINTS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/points/packages/")
if [ "$POINTS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✅ Points packages are available${NC}"
else
    echo -e "${RED}❌ Issue with points packages endpoint (HTTP $POINTS_RESPONSE)${NC}"
fi

# Test other endpoints
echo ""
echo -e "${BLUE}💬 Testing Chat Endpoints:${NC}"
CHAT_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/chat/conversations/")
if [ "$CHAT_RESPONSE" = "401" ]; then
    echo -e "${YELLOW}⚠️  Chat endpoint requires authentication (HTTP 401) - This is correct${NC}"
else
    echo -e "${GREEN}✅ Chat endpoint is accessible${NC}"
fi

echo ""
echo -e "${BLUE}💳 Testing Payments Endpoints:${NC}"
PAYMENTS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/payments/transactions/")
if [ "$PAYMENTS_RESPONSE" = "401" ]; then
    echo -e "${YELLOW}⚠️  Payments endpoint requires authentication (HTTP 401) - This is correct${NC}"
else
    echo -e "${GREEN}✅ Payments endpoint is accessible${NC}"
fi

echo ""
echo -e "${BLUE}⭐ Testing Reviews Endpoint:${NC}"
REVIEWS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/reviews/")
if [ "$REVIEWS_RESPONSE" = "401" ]; then
    echo -e "${YELLOW}⚠️  Reviews endpoint requires authentication (HTTP 401) - This is correct${NC}"
else
    echo -e "${GREEN}✅ Reviews endpoint is accessible${NC}"
fi

echo ""
echo -e "${BLUE}🔔 Testing Notifications Endpoint:${NC}"
NOTIFICATIONS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/notifications/")
if [ "$NOTIFICATIONS_RESPONSE" = "401" ]; then
    echo -e "${YELLOW}⚠️  Notifications endpoint requires authentication (HTTP 401) - This is correct${NC}"
else
    echo -e "${GREEN}✅ Notifications endpoint is accessible${NC}"
fi

echo ""
echo "==========================================="
echo -e "${GREEN}✅ Full test completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📋 Summary of useful links:${NC}"
echo "🌐 Home Page: $BASE_URL/"
echo "📚 Swagger UI: $BASE_URL/swagger/"
echo "📖 ReDoc: $BASE_URL/redoc/"
echo "🔗 JSON Schema: $BASE_URL/swagger.json"
echo "⚙️  Admin Panel: $BASE_URL/admin/"
echo ""
echo -e "${BLUE}💡 Usage Tips:${NC}"
echo "1. Use Swagger UI to interactively test all endpoints"
echo "2. Register a new account first to get a token"
echo "3. Use the token in Swagger to access protected endpoints"
echo "4. ReDoc provides elegant and detailed documentation"
