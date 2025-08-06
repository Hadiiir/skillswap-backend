#!/bin/bash

echo "🚀 Starting Full SkillSwap Project (Backend + Frontend)"
echo "========================================================="

# Check for required tools
echo "🔍 Checking required tools..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ All required tools are available"

# Stop any running services
echo "🛑 Stopping previous services..."
docker-compose -f docker-compose.simple.yml down 2>/dev/null || true

# Start Backend
echo "🔧 Starting Backend (Django + PostgreSQL + Redis)..."
docker-compose -f docker-compose.simple.yml up -d

# Wait for DB to initialize
echo "⏳ Waiting for the database to initialize..."
sleep 20

# Check backend status
echo "📊 Checking backend status..."
docker-compose -f docker-compose.simple.yml ps

# Test Backend API
echo "🧪 Testing Backend API..."
max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:8000/api/skills/ > /dev/null; then
        echo "✅ Backend API is working!"
        break
    else
        echo "⏳ Attempt $attempt of $max_attempts - Waiting for Backend..."
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ Failed to start Backend API"
    echo "📋 Showing Backend logs:"
    docker-compose -f docker-compose.simple.yml logs web
    exit 1
fi

# Frontend Setup
echo "🎨 Setting up and running Frontend (React)..."

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Make sure you're in the frontend directory."
    exit 1
fi

# Install dependencies if node_modules does not exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << EOL
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws
EOL
fi

# Start Frontend in the background
echo "🚀 Starting Frontend..."
npm start &
FRONTEND_PID=$!

# Wait for Frontend to start
echo "⏳ Waiting for Frontend to initialize..."
sleep 15

# Test Frontend
echo "🧪 Testing Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running!"
else
    echo "⚠️ Frontend may need more time to start"
fi

# Success Message
echo ""
echo "🎉 Project Started Successfully!"
echo "========================================"
echo ""
echo "🌐 Access Links:"
echo "- Frontend (React): http://localhost:3000"
echo "- Backend API: http://localhost:8000/api/"
echo "- Admin Panel: http://localhost:8000/admin/"
echo "- PostgreSQL DB: localhost:5434"
echo ""
echo "👤 Test Users:"
echo "- ahmed@example.com : testpass123"
echo "- sara@example.com : testpass123"
echo ""
echo "🛠️ Useful Commands:"
echo "- Stop Backend: docker-compose -f docker-compose.simple.yml down"
echo "- Stop Frontend: kill $FRONTEND_PID"
echo "- Backend Logs: docker-compose -f docker-compose.simple.yml logs -f"
echo "- Restart Backend: docker-compose -f docker-compose.simple.yml restart"
echo ""
echo "📝 Notes:"
echo "- Frontend PID: $FRONTEND_PID"
echo "- To stop everything: press Ctrl+C then run ./scripts/stop_full_project.sh"

# Save frontend PID to file
echo $FRONTEND_PID > .frontend_pid

# Trap to stop on Ctrl+C
trap 'echo "🛑 Stopping project..."; kill $FRONTEND_PID 2>/dev/null; docker-compose -f docker-compose.simple.yml down; exit 0' INT

echo "⌨️ Press Ctrl+C to stop the project"
wait $FRONTEND_PID
