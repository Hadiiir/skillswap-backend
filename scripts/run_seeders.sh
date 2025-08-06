#!/bin/bash

# SkillSwap Database Seeders Runner
# Usage: ./scripts/run_seeders.sh [seeder_name|all]

set -e

echo "🌱 SkillSwap Database Seeders"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Django project exists
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run from project root."
    exit 1
fi

# Set Django settings module
export DJANGO_SETTINGS_MODULE=skillswap.settings

# Function to run individual seeder
run_seeder() {
    local seeder_name=$1
    local seeder_file="scripts/seeders/${seeder_name}_seeder.py"
    
    if [ -f "$seeder_file" ]; then
        print_info "Running $seeder_name seeder..."
        cd scripts/seeders
        python "${seeder_name}_seeder.py"
        cd ../..
        print_success "$seeder_name seeder completed!"
    else
        print_error "Seeder file not found: $seeder_file"
        return 1
    fi
}

# Function to run all seeders
run_all_seeders() {
    print_info "Checking Python path and Django setup..."
    
    # Check if all required packages are installed
    python -c "import django; import rest_framework; import celery" 2>/dev/null || {
        print_error "Required packages not installed. Run: pip install -r requirements.txt"
        exit 1
    }
    
    print_info "Running all seeders via master seeder..."
    cd scripts/seeders
    python master_seeder.py
    cd ../..
}

# Main logic
case "${1:-all}" in
    "all")
        run_all_seeders
        ;;
    "superuser")
        run_seeder "create_superuser"
        ;;
    "categories")
        run_seeder "categories"
        ;;
    "users")
        run_seeder "users"
        ;;
    "points")
        run_seeder "points"
        ;;
    "skills")
        run_seeder "skills"
        ;;
    "orders")
        run_seeder "orders"
        ;;
    "reviews")
        run_seeder "reviews"
        ;;
    "notifications")
        run_seeder "notifications"
        ;;
    "payments")
        run_seeder "payments"
        ;;
    *)
        echo "Usage: $0 [all|superuser|categories|users|points|skills|orders|reviews|notifications|payments]"
        echo ""
        echo "Available seeders:"
        echo "  all           - Run all seeders in correct order"
        echo "  superuser     - Create admin superuser"
        echo "  categories    - Seed skill categories"
        echo "  users         - Seed users and profiles"
        echo "  points        - Seed points packages"
        echo "  skills        - Seed skills and FAQs"
        echo "  orders        - Seed sample orders"
        echo "  reviews       - Seed reviews and ratings"
        echo "  notifications - Seed notifications"
        echo "  payments      - Seed payment records"
        exit 1
        ;;
esac

print_success "Seeding process completed!"
print_info "You can now start your Django server and check the admin panel."
