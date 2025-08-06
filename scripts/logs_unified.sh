#!/bin/bash

echo "📋 SkillSwap Project Logs"
echo "========================"

if [ "$1" ]; then
    echo "📋 Showing logs for service: $1"
    docker-compose logs -f --tail=100 $1
else
    echo "📋 Showing logs for all services:"
    echo "Available services: web, db, redis, celery, celery-beat, flower"
    echo "Usage: $0 [service_name]"
    echo ""
    docker-compose logs --tail=50
fi
