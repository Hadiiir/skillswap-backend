#!/bin/bash

echo "⚡ Quick Staging Test & Data Verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if server is running
if curl -s http://localhost:8001/api/ > /dev/null; then
    echo -e "${GREEN}✅ Server is running${NC}"
else
    echo -e "${RED}❌ Server not running. Starting staging environment...${NC}"
    chmod +x scripts/complete_staging_setup.sh
    ./scripts/complete_staging_setup.sh
    
    echo "🚀 Starting server..."
    python manage.py runserver 0.0.0.0:8001 --settings=skillswap.settings &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 5
    
    if curl -s http://localhost:8001/api/ > /dev/null; then
        echo -e "${GREEN}✅ Server started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start server${NC}"
        exit 1
    fi
fi

echo "📊 Data Summary:"

# Get categories count
CATEGORIES_RESPONSE=$(curl -s http://localhost:8001/api/skills/categories/)
if echo "$CATEGORIES_RESPONSE" | grep -q "البرمجة"; then
    CATEGORIES_COUNT=$(echo "$CATEGORIES_RESPONSE" | grep -o '"name"' | wc -l)
    echo -e "Categories: ${GREEN}$CATEGORIES_COUNT${NC}"
else
    echo -e "Categories: ${RED}Error${NC}"
fi

# Get skills count
SKILLS_RESPONSE=$(curl -s "http://localhost:8001/api/skills/")
if echo "$SKILLS_RESPONSE" | grep -q "count"; then
    SKILLS_COUNT=$(echo "$SKILLS_RESPONSE" | grep -o '"count":[0-9]*' | grep -o '[0-9]*')
    echo -e "Skills: ${GREEN}$SKILLS_COUNT${NC}"
else
    echo -e "Skills: ${RED}Error${NC}"
fi

# Get packages count
PACKAGES_RESPONSE=$(curl -s http://localhost:8001/api/points/packages/)
if echo "$PACKAGES_RESPONSE" | grep -q "حزمة"; then
    PACKAGES_COUNT=$(echo "$PACKAGES_RESPONSE" | grep -o '"name"' | wc -l)
    echo -e "Point Packages: ${GREEN}$PACKAGES_COUNT${NC}"
else
    echo -e "Point Packages: ${RED}Error${NC}"
fi

echo ""
echo -e "${GREEN}🌐 Open Swagger: http://localhost:8001/swagger/${NC}"
echo -e "${GREEN}🔧 Admin Panel: http://localhost:8001/admin/ (staging_admin/staging123)${NC}"
