#!/bin/bash

echo "🔧 Setting Up and Testing Swagger for the Project"
echo "==============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}📦 1. Installing dependencies:${NC}"
pip install drf-yasg

echo ""
echo -e "${BLUE}🔄 2. Applying database migrations:${NC}"
python manage.py makemigrations
python manage.py migrate

echo ""
echo -e "${BLUE}🗂️ 3. Collecting static files:${NC}"
python manage.py collectstatic --noinput

echo ""
echo -e "${BLUE}🚀 4. Starting the server:${NC}"
echo -e "${YELLOW}The server will start on http://localhost:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server manually if needed${NC}"
echo ""

# Start the server in the background for testing
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

# Wait a few seconds for the server to fully start
sleep 5

echo ""
echo -e "${GREEN}✅ Server is now running!${NC}"
echo ""
echo -e "${BLUE}🔗 Available Links:${NC}"
echo "📚 Swagger UI: http://localhost:8000/swagger/"
echo "📖 ReDoc: http://localhost:8000/redoc/"
echo "🌐 Home Page: http://localhost:8000/"
echo "⚙️  Admin Panel: http://localhost:8000/admin/"

# Test the endpoints (optional script)
echo ""
echo -e "${BLUE}🧪 Running quick endpoint tests:${NC}"
./scripts/test_swagger_endpoints.sh

# Keep server running until user input
echo ""
echo -e "${YELLOW}The server is running... Press Enter to stop it${NC}"
read

# Stop the server
kill $SERVER_PID
echo -e "${GREEN}✅ Server has been stopped successfully${NC}"
