#!/bin/bash

echo "📋 Displaying SkillSwap Project Logs"
echo "============================="

echo "Select the service to view its logs:"
echo "1. Web Application"
echo "2. Database"
echo "3. All Services"

read -p "Enter a number (1-3): " choice

case $choice in
    1)
        echo "📋 Logs for Web Application:"
        docker-compose -f docker-compose.simple.yml logs -f web
        ;;
    2)
        echo "📋 Logs for Database:"
        docker-compose -f docker-compose.simple.yml logs -f db
        ;;
    3)
        echo "📋 Logs for All Services:"
        docker-compose -f docker-compose.simple.yml logs -f
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac
