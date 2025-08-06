#!/bin/bash

# SkillSwap Database Reset and Seed Script
# This script will reset the database and run all seeders

set -e

echo "🔄 SkillSwap Database Reset and Seed"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not detected. Activating..."
    if [ -f "env/bin/activate" ]; then
        source env/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment not found. Please create one first."
        exit 1
    fi
fi

# Confirmation prompt
read -p "⚠️  This will delete all existing data. Are you sure? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Operation cancelled."
    exit 0
fi

print_info "Stopping any running Django processes..."
pkill -f "python manage.py runserver" 2>/dev/null || true

print_info "Removing existing migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
find . -path "*/migrations/*.pyc" -delete 2>/dev/null || true

print_info "Removing database file if exists..."
rm -f db.sqlite3

print_info "Creating fresh migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations skills
python manage.py makemigrations points
python manage.py makemigrations chat
python manage.py makemigrations payments
python manage.py makemigrations reviews
python manage.py makemigrations notifications

print_info "Applying migrations..."
python manage.py migrate

print_info "Running all seeders..."
./scripts/run_seeders.sh all

print_success "Database reset and seeding completed!"
print_info "You can now start your Django server:"
print_info "  python manage.py runserver"
