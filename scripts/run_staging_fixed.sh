#!/bin/bash

echo "🚀 Starting Fixed Staging Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load staging environment variables
if [ -f .env.staging ]; then
    export $(grep -v '^#' .env.staging | grep -v '^$' | xargs)
    echo -e "${GREEN}✅ Loaded staging environment variables${NC}"
else
    echo -e "${RED}❌ .env.staging file not found${NC}"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    exit 1
fi

# Check if database tables exist
echo "🔍 Checking database state..."
DB_CHECK=$(PGPASSWORD=$STAGING_DB_PASSWORD psql -h $STAGING_DB_HOST -p $STAGING_DB_PORT -U $STAGING_DB_USER -d $STAGING_DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '%_category';" 2>/dev/null || echo "0")

if [ "$DB_CHECK" -eq "0" ]; then
    echo -e "${YELLOW}⚠️ Database tables not found. Running migration fix...${NC}"
    chmod +x scripts/fix_staging_migrations.sh
    ./scripts/fix_staging_migrations.sh
else
    echo -e "${GREEN}✅ Database tables exist${NC}"
fi

# Install requirements
pip install -q -r requirements.txt

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --settings=skillswap.settings

# Start the server
echo -e "${BLUE}🚀 Starting staging server on port 8001...${NC}"
echo -e "${GREEN}🌐 Swagger UI: http://localhost:8001/swagger/${NC}"
echo -e "${GREEN}📖 ReDoc: http://localhost:8001/redoc/${NC}"
echo -e "${GREEN}🔧 Admin: http://localhost:8001/admin/${NC}"
echo -e "${GREEN}📡 API: http://localhost:8001/api/${NC}"
echo ""
echo -e "${YELLOW}👤 Admin Login: staging_admin / staging123${NC}"
echo -e "${YELLOW}👥 Test Users: user1@staging.com to user5@staging.com / test123${NC}"
echo ""

python manage.py runserver 0.0.0.0:8001 --settings=skillswap.settings
