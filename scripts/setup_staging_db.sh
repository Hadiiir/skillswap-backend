#!/bin/bash

echo "🗄️ Setting up Staging Database on Port 5434..."

# Check if PostgreSQL is running
if ! sudo systemctl is-active --quiet postgresql; then
    echo "Starting PostgreSQL service..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Check current PostgreSQL version
PG_VERSION=$(sudo -u postgres psql -t -c "SELECT version();" | grep -oP '\d+\.\d+' | head -1)
echo "PostgreSQL version: $PG_VERSION"

# Create staging database on existing PostgreSQL instance (port 5432)
# We'll use a different database name instead of different port
echo "Creating staging database and user on existing PostgreSQL instance..."

# Create staging database and user
sudo -u postgres psql -c "DROP DATABASE IF EXISTS skillswap_staging;" 2>/dev/null
sudo -u postgres psql -c "DROP USER IF EXISTS skillswap_staging;" 2>/dev/null

sudo -u postgres psql -c "CREATE DATABASE skillswap_staging;"
sudo -u postgres psql -c "CREATE USER skillswap_staging WITH PASSWORD 'staging_password_123';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE skillswap_staging TO skillswap_staging;"
sudo -u postgres psql -c "ALTER USER skillswap_staging CREATEDB;"
sudo -u postgres psql -c "ALTER DATABASE skillswap_staging OWNER TO skillswap_staging;"

echo "✅ Staging database setup complete!"
echo "📊 Database: skillswap_staging"
echo "🔌 Port: 5432 (same as local, but different database)"
echo "👤 User: skillswap_staging"
echo "🔑 Password: staging_password_123"

# Test connection
echo "Testing connection..."
PGPASSWORD=staging_password_123 psql -h localhost -p 5432 -U skillswap_staging -d skillswap_staging -c "SELECT 'Staging DB Connected Successfully!' as status;" && echo "✅ Connection successful!" || echo "❌ Connection failed!"

echo ""
echo "🎯 Now you can run staging environment with:"
echo "   ./scripts/run_staging.sh"
