#!/bin/bash

echo "🗑️ Deleting the database and recreating it..."

# Stop the services
docker-compose -f docker-compose.simple.yml down

# Remove stored data
docker volume rm skillswap-backend_postgres_data_simple 2>/dev/null || true

echo "✅ Old database has been deleted"

# Restart the services
docker-compose -f docker-compose.simple.yml up -d

echo "⏳ Waiting for the database to start..."
sleep 30

# Apply migrations
docker-compose -f docker-compose.simple.yml exec web python manage.py migrate

echo "🎉 The new database has been set up successfully!"
