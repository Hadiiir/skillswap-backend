#!/bin/bash

echo "🛑 Stopping Complete SkillSwap Project..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_status "Stopping all services..."
docker-compose down

print_status "Removing unused containers and networks..."
docker system prune -f

print_success "✅ Project stopped successfully!"
echo ""
echo "💡 To start again, run: ./scripts/start_complete_project.sh"
echo "🗑️  To remove all data, run: docker-compose down -v"
